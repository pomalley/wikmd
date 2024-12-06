#!/usr/bin/python3

import unittest
from quick_links import process_md

class TestQuickLinks(unittest.TestCase):
    def test_noop(self):
        self.assertEqual(process_md(''), '')
        self.assertEqual(process_md('nothing'), 'nothing')
        self.assertEqual(process_md('[reg link]()'), '[reg link]()')
        self.assertEqual(process_md('[[double]]'), '[[double]]')
        self.assertEqual(process_md('[]'), '[]')
        self.assertEqual(process_md('[[]]'), '[[]]')
        self.assertEqual(process_md('`verbatim`'), '`verbatim`')
        
    def test_replace(self):
        self.assertEqual(process_md('[test]'), '[test](test)')
        self.assertEqual(process_md('[test] [not](this)'),
                         '[test](test) [not](this)')
        self.assertEqual(process_md('[1][2]'), '[1](1)[2](2)')

    def test_multiline(self):
        self.assertEqual(process_md(' first line\n'
                                    '[test]\n'
                                    'last [line](line)\n'),
                         ' first line\n'
                         '[test](test)\n'
                         'last [line](line)\n')

    def test_inline(self):
        self.assertEqual(process_md('`[link]`'), '`[link]`')
        self.assertEqual(process_md('[1]`[2]`[3]'), '[1](1)`[2]`[3](3)')
        self.assertEqual(process_md('` [1]'), '` [1](1)')
        self.assertEqual(process_md('` `` [1]` [2]'), '` `` [1]` [2](2)')

    def test_block(self):
        self.assertEqual(process_md('    [1]'), '    [1]')
        self.assertEqual(process_md('>[1]'), '>[1]')
        self.assertEqual(process_md(' > [1]'), ' > [1]')

    def test_fenced(self):
        self.assertEqual(process_md('first [a]\n'
                                    '```code \n'
                                    '[1]`[2]`[3]\n'
                                    '```\n'
                                    '[4]\n'
                                    '  ````\n'
                                    '```\n'
                                    '[5]\n'
                                    '  ````\n'
                                    '[6]\n'),
                         'first [a](a)\n'
                         '```code \n'
                         '[1]`[2]`[3]\n'
                         '```\n'
                         '[4](4)\n'
                         '  ````\n'
                         '```\n'
                         '[5]\n'
                         '  ````\n'
                         '[6](6)\n')
        


if __name__ == '__main__':
    unittest.main()
