# -*- coding: utf-8 -*-

import os
import copy
from io import BytesIO
from .. import CleoTestCase

from cleo.helpers.table import Table
from cleo.helpers.table_cell import TableCell
from cleo.helpers.table_separator import TableSeparator
from cleo.helpers.table_style import TableStyle
from cleo.outputs.stream_output import StreamOutput
from cleo._compat import decode


class TableTest(CleoTestCase):

    books = [
        ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
        ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens'],
        ['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'],
        ['80-902734-1-6', 'And Then There Were None', 'Agatha Christie'],
        ['9782070409341', 'Le Père Goriot', 'Honoré de Balzac']
    ]

    _render_data = [
        (
            ['ISBN', 'Title', 'Author'],
            books,
            'default',
'''+---------------+--------------------------+------------------+
| ISBN          | Title                    | Author           |
+---------------+--------------------------+------------------+
| 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
| 9971-5-0210-0 | A Tale of Two Cities     | Charles Dickens  |
| 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None | Agatha Christie  |
| 9782070409341 | Le Père Goriot           | Honoré de Balzac |
+---------------+--------------------------+------------------+
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            books,
            'compact',
''' ISBN          Title                    Author           
 99921-58-10-7 Divine Comedy            Dante Alighieri  
 9971-5-0210-0 A Tale of Two Cities     Charles Dickens  
 960-425-059-0 The Lord of the Rings    J. R. R. Tolkien 
 80-902734-1-6 And Then There Were None Agatha Christie  
 9782070409341 Le Père Goriot           Honoré de Balzac 
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            books,
            'borderless',
''' =============== ========================== ================== 
  ISBN            Title                      Author            
 =============== ========================== ================== 
  99921-58-10-7   Divine Comedy              Dante Alighieri   
  9971-5-0210-0   A Tale of Two Cities       Charles Dickens   
  960-425-059-0   The Lord of the Rings      J. R. R. Tolkien  
  80-902734-1-6   And Then There Were None   Agatha Christie   
  9782070409341   Le Père Goriot             Honoré de Balzac  
 =============== ========================== ================== 
'''
        ),
        (
            ['ISBN', 'Title'],
            [
                ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
                ['9971-5-0210-0'],
                ['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'],
                ['80-902734-1-6', 'And Then There Were None', 'Agatha Christie']
            ],
            'default',
'''+---------------+--------------------------+------------------+
| ISBN          | Title                    |                  |
+---------------+--------------------------+------------------+
| 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
| 9971-5-0210-0 |                          |                  |
| 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None | Agatha Christie  |
+---------------+--------------------------+------------------+
'''
        ),
        (
            [],
            [
                ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
                ['9971-5-0210-0'],
                ['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'],
                ['80-902734-1-6', 'And Then There Were None', 'Agatha Christie']
            ],
            'default',
'''+---------------+--------------------------+------------------+
| 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
| 9971-5-0210-0 |                          |                  |
| 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None | Agatha Christie  |
+---------------+--------------------------+------------------+
'''
        ),
        (
            ['ISBN', 'Title'],
            [],
            'default',
'''+------+-------+
| ISBN | Title |
+------+-------+
'''
        ),
        (
            [],
            [],
            'default',
            ''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            [
                ['99921-58-10-7', "Divine\nComedy", 'Dante Alighieri'],
                ['9971-5-0210-2', "Harry Potter\nand the Chamber of Secrets", "Rowling\nJoanne K."],
                ['9971-5-0210-2', "Harry Potter\nand the Chamber of Secrets", "Rowling\nJoanne K."],
                ['960-425-059-0', 'The Lord of the Rings', "J. R. R.\nTolkien"]
            ],
            'default',
'''+---------------+----------------------------+-----------------+
| ISBN          | Title                      | Author          |
+---------------+----------------------------+-----------------+
| 99921-58-10-7 | Divine                     | Dante Alighieri |
|               | Comedy                     |                 |
| 9971-5-0210-2 | Harry Potter               | Rowling         |
|               | and the Chamber of Secrets | Joanne K.       |
| 9971-5-0210-2 | Harry Potter               | Rowling         |
|               | and the Chamber of Secrets | Joanne K.       |
| 960-425-059-0 | The Lord of the Rings      | J. R. R.        |
|               |                            | Tolkien         |
+---------------+----------------------------+-----------------+
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            [
                ['<info>99921-58-10-7</info>', '<error>Divine Comedy</error>', '<fg=blue;bg=white>Dante Alighieri</fg=blue;bg=white>'],
                ['9971-5-0210-0', 'A Tale of Two Cities', '<info>Charles Dickens</>'],
            ],
            'default',
'''+---------------+----------------------+-----------------+
| ISBN          | Title                | Author          |
+---------------+----------------------+-----------------+
| 99921-58-10-7 | Divine Comedy        | Dante Alighieri |
| 9971-5-0210-0 | A Tale of Two Cities | Charles Dickens |
+---------------+----------------------+-----------------+
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            [
                ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
                TableSeparator(),
                [TableCell('Divine Comedy(Dante Alighieri)', colspan=3)],
                TableSeparator(),
                [TableCell('Arduino: A Quick-Start Guide', colspan=2), 'Mark Schmidt'],
                TableSeparator(),
                ['9971-5-0210-0', TableCell('A Tale of \nTwo Cities', colspan=2)]
            ],
            'default',
'''+----------------+---------------+-----------------+
| ISBN           | Title         | Author          |
+----------------+---------------+-----------------+
| 99921-58-10-7  | Divine Comedy | Dante Alighieri |
+----------------+---------------+-----------------+
| Divine Comedy(Dante Alighieri)                   |
+----------------+---------------+-----------------+
| Arduino: A Quick-Start Guide   | Mark Schmidt    |
+----------------+---------------+-----------------+
| 9971-5-0210-0  | A Tale of                       |
|                | Two Cities                      |
+----------------+---------------+-----------------+
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            [
                [TableCell('9971-5-0210-0', rowspan=3), 'Divine Comedy', 'Dante Alighieri'],
                ['A Tale of Two Cities', 'Charles Dickens'],
                ["The Lord of \nthe Rings", "J. R. \nR. Tolkien"],
                TableSeparator(),
                ['80-902734-1-6', TableCell("And Then \nThere \nWere None", rowspan=3), 'Agatha Christie'],
                ['80-902734-1-7', 'Test']
            ],
            'default',
'''+---------------+----------------------+-----------------+
| ISBN          | Title                | Author          |
+---------------+----------------------+-----------------+
| 9971-5-0210-0 | Divine Comedy        | Dante Alighieri |
|               | A Tale of Two Cities | Charles Dickens |
|               | The Lord of          | J. R.           |
|               | the Rings            | R. Tolkien      |
+---------------+----------------------+-----------------+
| 80-902734-1-6 | And Then             | Agatha Christie |
| 80-902734-1-7 | There                | Test            |
|               | Were None            |                 |
+---------------+----------------------+-----------------+
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            [
                [TableCell('9971-5-0210-0', rowspan=2, colspan=2), 'Dante Alighieri'],
                ['Charles Dickens'],
                TableSeparator(),
                ['Dante Alighieri', TableCell('9971-5-0210-0', rowspan=3, colspan=2)],
                ['J. R. R. Tolkien'],
                ['J. R. R']
            ],
            'default',
'''+------------------+--------+-----------------+
| ISBN             | Title  | Author          |
+------------------+--------+-----------------+
| 9971-5-0210-0             | Dante Alighieri |
|                           | Charles Dickens |
+------------------+--------+-----------------+
| Dante Alighieri  | 9971-5-0210-0            |
| J. R. R. Tolkien |                          |
| J. R. R          |                          |
+------------------+--------+-----------------+
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            [
                [TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2), 'Dante Alighieri'],
                ['Charles Dickens'],
                TableSeparator(),
                ['Dante Alighieri', TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2)],
                ['Charles Dickens'],
                TableSeparator(),
                [
                    TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2),
                    TableCell("Dante \nAlighieri", rowspan=2, colspan=1)
                ]
            ],
            'default',
'''+-----------------+-------+-----------------+
| ISBN            | Title | Author          |
+-----------------+-------+-----------------+
| 9971                    | Dante Alighieri |
| -5-                     | Charles Dickens |
| 021                     |                 |
| 0-0                     |                 |
+-----------------+-------+-----------------+
| Dante Alighieri | 9971                    |
| Charles Dickens | -5-                     |
|                 | 021                     |
|                 | 0-0                     |
+-----------------+-------+-----------------+
| 9971                    | Dante           |
| -5-                     | Alighieri       |
| 021                     |                 |
| 0-0                     |                 |
+-----------------+-------+-----------------+
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            [
                [TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2), 'Dante Alighieri'],
                ['Charles Dickens'],
                ['Dante Alighieri', TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2)],
                ['Charles Dickens']
            ],
            'default',
'''+-----------------+-------+-----------------+
| ISBN            | Title | Author          |
+-----------------+-------+-----------------+
| 9971                    | Dante Alighieri |
| -5-                     | Charles Dickens |
| 021                     |                 |
| 0-0                     |                 |
| Dante Alighieri | 9971                    |
| Charles Dickens | -5-                     |
|                 | 021                     |
|                 | 0-0                     |
+-----------------+-------+-----------------+
'''
        ),
        (
            ['ISBN', 'Author'],
            [
                [TableCell('9971-5-0210-0', rowspan=3, colspan=1), 'Dante Alighieri'],
                [TableSeparator()],
                ['Charles Dickens']
            ],
            'default',
'''+---------------+-----------------+
| ISBN          | Author          |
+---------------+-----------------+
| 9971-5-0210-0 | Dante Alighieri |
|               |-----------------|
|               | Charles Dickens |
+---------------+-----------------+
'''
        ),
        (
            [
                [TableCell('Main title', colspan=3)],
                ['ISBN', 'Title', 'Author']
            ],
            [],
            'default',
'''+------+-------+--------+
| Main title            |
+------+-------+--------+
| ISBN | Title | Author |
+------+-------+--------+
'''
        ),
        (
            [],
            [
                [
                    TableCell('1', colspan=3),
                    TableCell('2', colspan=2),
                    TableCell('3', colspan=2),
                    TableCell('4', colspan=2)
                ]
            ],
            'default',
'''+--+--+--+--+--+--+--+--+--+
| 1      | 2   | 3   | 4   |
+--+--+--+--+--+--+--+--+--+
'''
        )
    ]

    @property
    def render_data(self):
        return copy.deepcopy(self._render_data)

    def setUp(self):
        self.stream = BytesIO()

    def tearDown(self):
        self.stream.close()
        self.stream = None

    def test_render(self):
        """
        TableHelper.render() should behave properly
        """
        for data_set in self.render_data:
            headers, rows, layout, expected = data_set

            output = self.get_output_stream()
            table = Table(output)
            table.set_headers(headers)\
                .set_rows(rows)\
                .set_style(layout)

            table.render()

            self.assertEqual(decode(expected), self.get_output_content(output))

    def test_render_add_rows(self):
        """
        TableHelper.render() should behave properly after adding rows
        """
        for data_set in self.render_data:
            headers, rows, layout, expected = data_set

            output = self.get_output_stream()
            table = Table(output)
            table.set_headers(headers)\
                .add_rows(rows)\
                .set_style(layout)

            table.render()

            self.assertEqual(decode(expected), self.get_output_content(output))

    def test_render_add_rows_one_by_one(self):
        """
        TableHelper.render() should behave properly after adding rows one by one
        """
        for data_set in self.render_data:
            headers, rows, layout, expected = data_set

            output = self.get_output_stream()
            table = Table(output)
            table.set_headers(headers)\
                .set_style(layout)

            for row in rows:
                table.add_row(row)

            table.render()

            self.assertEqual(decode(expected), self.get_output_content(output))

    def test_style(self):
        style = TableStyle()
        style.set_horizontal_border_char('.')
        style.set_vertical_border_char('.')
        style.set_crossing_char('.')

        Table.set_style_definition('dotfull', style)
        output = self.get_output_stream()
        table = Table(output)
        table.set_headers(['Foo'])
        table.set_rows([['Bar']])
        table.set_style('dotfull')

        table.render()

        expected = '''.......
. Foo .
.......
. Bar .
.......
'''

        self.assertEqual(expected, self.get_output_content(output))

    def test_row_separator(self):
        output = self.get_output_stream()

        table = Table(output)
        table.set_headers(['Foo'])
        table.set_rows([
            ['Bar1'],
            TableSeparator(),
            ['Bar2'],
            TableSeparator(),
            ['Bar3']
        ])

        table.render()

        expected = '''+------+
| Foo  |
+------+
| Bar1 |
+------+
| Bar2 |
+------+
| Bar3 |
+------+
'''

        self.assertEqual(expected, self.get_output_content(output))

    def test_render_multi_calls(self):
        output = self.get_output_stream()

        table = Table(output)
        table.set_rows([
            [TableCell('foo', colspan=2)]
        ])
        table.render()
        table.render()
        table.render()

        expected = '''+---+--+
| foo  |
+---+--+
+---+--+
| foo  |
+---+--+
+---+--+
| foo  |
+---+--+
'''

        self.assertEqual(expected, self.get_output_content(output))

    def test_column_style(self):
        output = self.get_output_stream()

        table = Table(output)
        table.set_headers(['ISBN', 'Title', 'Author', 'Price'])
        table.set_rows([
            ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri', '9.95'],
            ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens', '139.25']
        ])

        style = TableStyle()
        style.set_pad_type('left')
        table.set_column_style(3, style)

        table.render()

        expected = '''+---------------+----------------------+-----------------+--------+
| ISBN          | Title                | Author          |  Price |
+---------------+----------------------+-----------------+--------+
| 99921-58-10-7 | Divine Comedy        | Dante Alighieri |   9.95 |
| 9971-5-0210-0 | A Tale of Two Cities | Charles Dickens | 139.25 |
+---------------+----------------------+-----------------+--------+
'''

        self.assertEqual(expected, self.get_output_content(output))

    def get_output_stream(self):
        stream = BytesIO()

        return StreamOutput(stream, StreamOutput.VERBOSITY_NORMAL, False)

    def get_output_content(self, output):
        output.get_stream().seek(0)

        value = output.get_stream().getvalue()

        return decode(value).replace(os.linesep, "\n")
