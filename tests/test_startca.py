"""
test_teksavvy.py
Fetch and act upon your ISPs quota limits.

Copyright (C) 2018  Mike O'Driscoll <mike@mikeodriscoll.ca>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
from unittest import TestCase
import mock
from tekuila.isp.startca import StartCA

# Python 2 and 3 support
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class TestStartCA(TestCase):
    def test_b_to_GB(self):
        '''Make sure the math doesn't change.
        '''
        self.assertEqual(239.743945534, StartCA.b_to_GB(239743945534))

    @mock.patch('http.client.HTTPResponse')
    @mock.patch('http.client.HTTPSConnection')
    def test_good_data(self, mock_conn, mock_response):
        '''Successfully parse some data.
        '''
        mock_conn.return_value.getresponse.return_value = mock_response.return_value
        mock_response.return_value.status = 200
        mock_response.return_value.read.return_value = '''<?xml version="1.0" encoding="ISO-8859-15"?>
<usage>
  <version>1.1</version>
  <total> <!-- total actual usage -->
    <download>239743945534</download>
    <upload>4528123013</upload>
  </total>
  <used> <!-- part of usage that counts against quota -->
    <download>0</download>
    <upload>0</upload>
  </used>
  <grace> <!-- part of usage that is free -->
    <download>239743945534</download>
    <upload>4528123013</upload>
  </grace>
</usage>
'''
        sca = StartCA('NOT_A_KEY', 400, 0.75)
        self.assertEqual(True, sca.fetch_data())

        expected = '''Used Download: 0.0 GB
Used Upload: 0.0 GB
Grace Download: 239.743945534 GB
Grace Upload: 4.528123013 GB
Total Download: 239.743945534 GB
Total Upload: 4.528123013 GB
'''
        with mock.patch('sys.stdout', new=StringIO()) as fake_stdout:
            sca.verbose = True
            sca.print_data()
            self.assertEqual(fake_stdout.getvalue(), expected)

    @mock.patch('http.client.HTTPResponse')
    @mock.patch('http.client.HTTPSConnection')
    def test_bad_fetch(self, mock_conn, mock_response):
        mock_conn.return_value.getresponse.return_value = mock_response.return_value
        mock_response.return_value.status = 400

        sca = StartCA('NOT_A_KEY', 400, 0.75)
        self.assertEqual(False, sca.fetch_data())

    def test_no_key(self):
        sca = StartCA(None, 0, 0)
        self.assertEqual(False, sca.fetch_data())

    @mock.patch('http.client.HTTPResponse')
    @mock.patch('http.client.HTTPSConnection')
    def test_garbage_data(self, mock_conn, mock_response):
        '''Successfully parse some data.
        '''
        mock_conn.return_value.getresponse.return_value = mock_response.return_value
        mock_response.return_value.status = 200
        mock_response.return_value.read.return_value = "not xml"
        sca = StartCA('NOT_A_KEY', 400, 0.75)
        self.assertEqual(False, sca.fetch_data())
