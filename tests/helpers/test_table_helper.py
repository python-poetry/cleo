# -*- coding: utf-8 -*-

import os
from io import BytesIO
from unittest import TestCase

from cleo.helpers.table_helper import TableHelper
from cleo.outputs.stream_output import StreamOutput


class TableHelperTest(TestCase):

    books = [
        ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
        ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens'],
        ['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'],
        ['80-902734-1-6', 'And Then There Were None', 'Agatha Christie']
    ]

    render_data = (
        (
            ['ISBN', 'Title', 'Author'],
            books,
            TableHelper.LAYOUT_DEFAULT,
'''+---------------+--------------------------+------------------+
| ISBN          | Title                    | Author           |
+---------------+--------------------------+------------------+
| 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
| 9971-5-0210-0 | A Tale of Two Cities     | Charles Dickens  |
| 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None | Agatha Christie  |
+---------------+--------------------------+------------------+
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            books,
            TableHelper.LAYOUT_COMPACT,
''' ISBN          Title                    Author           
 99921-58-10-7 Divine Comedy            Dante Alighieri  
 9971-5-0210-0 A Tale of Two Cities     Charles Dickens  
 960-425-059-0 The Lord of the Rings    J. R. R. Tolkien 
 80-902734-1-6 And Then There Were None Agatha Christie  
'''
        ),
        (
            ['ISBN', 'Title', 'Author'],
            books,
            TableHelper.LAYOUT_BORDERLESS,
''' =============== ========================== ================== 
  ISBN            Title                      Author            
 =============== ========================== ================== 
  99921-58-10-7   Divine Comedy              Dante Alighieri   
  9971-5-0210-0   A Tale of Two Cities       Charles Dickens   
  960-425-059-0   The Lord of the Rings      J. R. R. Tolkien  
  80-902734-1-6   And Then There Were None   Agatha Christie   
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
            TableHelper.LAYOUT_DEFAULT,
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
            TableHelper.LAYOUT_DEFAULT,
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
            TableHelper.LAYOUT_DEFAULT,
'''+------+-------+
| ISBN | Title |
+------+-------+
'''
        ),
        (
            [],
            [],
            TableHelper.LAYOUT_DEFAULT,
            ''
        ),
    )

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

            table = TableHelper()
            table.set_headers(headers)\
                .set_rows(rows)\
                .set_layout(layout)

            output_ = self.get_output_stream()
            table.render(output_)

            self.assertEqual(expected, self.get_output_content(output_))

    def test_render_add_rows(self):
        """
        TableHelper.render() should behave properly after adding rows
        """
        for data_set in self.render_data:
            headers, rows, layout, expected = data_set

            table = TableHelper()
            table.set_headers(headers)\
                .add_rows(rows)\
                .set_layout(layout)

            output_ = self.get_output_stream()
            table.render(output_)

            self.assertEqual(expected, self.get_output_content(output_))

    def test_render_add_rows_one_by_one(self):
        """
        TableHelper.render() should behave properly after adding rows one by one
        """
        for data_set in self.render_data:
            headers, rows, layout, expected = data_set

            table = TableHelper()
            table.set_headers(headers)\
                .set_layout(layout)

            for row in rows:
                table.add_row(row)

            output_ = self.get_output_stream()
            table.render(output_)

            self.assertEqual(expected, self.get_output_content(output_))

    def get_output_stream(self):
        stream = BytesIO()

        return StreamOutput(stream, StreamOutput.VERBOSITY_NORMAL, False)

    def get_output_content(self, output_):
        output_.get_stream().seek(0)

        return output_.get_stream().getvalue().decode('utf-8').replace(os.linesep, "\n")
