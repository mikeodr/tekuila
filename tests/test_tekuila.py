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
import os
import mock
from tekuila.tekuila import Tekuila

# Python 2 and 3 support
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class TestTekuila(TestCase):
    def test_not_impl(self):
        '''Check not implemented functions error.
        '''
        t = Tekuila()
        with self.assertRaises(NotImplementedError):
            t.fetch_data()
        with self.assertRaises(NotImplementedError):
            t.print_data()

    def test_caps(self):
        '''Test over caps.
        '''
        t = Tekuila()

        # Check a over cap
        t.cap = 100
        t._download_total = 300
        t.verbose = True
        with mock.patch('sys.stdout', new=StringIO()) as fake_stdout:
            self.assertEqual(True, t.check_cap())
            self.assertEqual(fake_stdout.getvalue().strip(), 'Cap exceeded 300 / 100')

        t.cap = 400
        self.assertEqual(False, t.check_cap())

    def test_warn(self):
        '''Test over warn level.
        '''
        t = Tekuila()
        # Check over a warn
        t.cap = 400
        t.warn_ratio = 0.75
        t._download_total = 300.1
        t.verbose = True
        with mock.patch('sys.stdout', new=StringIO()) as fake_stdout:
            self.assertEqual(True, t.check_warn())
            self.assertEqual(fake_stdout.getvalue().strip(), 'Warn level exceeded.')

        t.warn_ratio = 0.9
        self.assertEqual(False, t.check_warn())

    def test_config_load(self):
        '''Test loading of config file.
        '''
        t = Tekuila()
        conf_path = os.path.abspath('tests/conf_file')
        t.load_config(conf_path)
        self.assertEqual('NOTAKEY', t.api_key)
        self.assertEqual(303.3, t.cap)
        self.assertEqual(0.75, t.warn_ratio)
