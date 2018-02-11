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
from tekuila.isp.teksavvy import Teksavvy

# Python 2 and 3 support
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class TestTekSavvy(TestCase):
    @mock.patch('http.client.HTTPResponse')
    @mock.patch('http.client.HTTPSConnection')
    def test_good_data(self, mock_conn, mock_response):
        '''Successfully parse some data.
        '''
        mock_conn.return_value.getresponse.return_value = mock_response.return_value
        mock_response.return_value.status = 200
        mock_response.return_value.read.return_value = '''
{
  "odata.metadata":"http://api.teksavvy.com/web/Usage/$metadata#UsageSummaryRecords","value":[
    {
      "StartDate":"2018-01-01T00:00:00","EndDate":"2018-01-31T00:00:00","OID":"999999","IsCurrent":true,"OnPeakDownload":226.75,"OnPeakUpload":8.82,"OffPeakDownload":36.24,"OffPeakUpload":1.58
    }
    ]
}'''
        tek = Teksavvy('NOT_A_KEY', 400, 0.75)
        self.assertEqual(True, tek.fetch_data())
        expected = '''On Peak Download: 226.75 GB
On Peak Upload: 8.82 GB
Off Peak Download: 36.24 GB
Off Peak Upload: 1.58 GB
Start Date: 2018-01-01T00:00:00
End Date: 2018-01-31T00:00:00
'''
        with mock.patch('sys.stdout', new=StringIO()) as fake_stdout:
            tek.verbose = True
            tek.print_data()
            self.assertEqual(fake_stdout.getvalue(), expected)

    @mock.patch('http.client.HTTPResponse')
    @mock.patch('http.client.HTTPSConnection')
    def test_bad_fetch(self, mock_conn, mock_response):
        mock_conn.return_value.getresponse.return_value = mock_response.return_value
        mock_response.return_value.status = 400

        tek = Teksavvy('NOT_A_KEY', 400, 0.75)
        self.assertEqual(False, tek.fetch_data())

    def test_no_key(self):
        tek = Teksavvy(None, 0, 0)
        self.assertEqual(False, tek.fetch_data())

    @mock.patch('http.client.HTTPResponse')
    @mock.patch('http.client.HTTPSConnection')
    def test_garbage_data(self, mock_conn, mock_response):
        '''Successfully parse some data.
        '''
        mock_conn.return_value.getresponse.return_value = mock_response.return_value
        mock_response.return_value.status = 200
        mock_response.return_value.read.return_value = "not json"
        tek = Teksavvy('NOT_A_KEY', 400, 0.75)
        self.assertEqual(False, tek.fetch_data())
