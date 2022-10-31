from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cleo.ui.table import Table
from cleo.ui.table_cell import TableCell
from cleo.ui.table_separator import TableSeparator
from cleo.ui.table_style import TableStyle


if TYPE_CHECKING:
    from cleo.io.buffered_io import BufferedIO
    from cleo.ui.table import Rows

books = [
    ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
    ["9971-5-0210-0", "A Tale of Two Cities", "Charles Dickens"],
    ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
    ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
    ["9782070409341", "Le Père Goriot", "Honoré de Balzac"],
]


@pytest.mark.parametrize(
    ["headers", "rows", "style", "expected"],
    [
        (
            ["ISBN", "Title", "Author"],
            books,
            "default",
            """\
+---------------+--------------------------+------------------+
| ISBN          | Title                    | Author           |
+---------------+--------------------------+------------------+
| 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
| 9971-5-0210-0 | A Tale of Two Cities     | Charles Dickens  |
| 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None | Agatha Christie  |
| 9782070409341 | Le Père Goriot           | Honoré de Balzac |
+---------------+--------------------------+------------------+
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            books,
            "compact",
            """\
 ISBN          Title                    Author           
 99921-58-10-7 Divine Comedy            Dante Alighieri  
 9971-5-0210-0 A Tale of Two Cities     Charles Dickens  
 960-425-059-0 The Lord of the Rings    J. R. R. Tolkien 
 80-902734-1-6 And Then There Were None Agatha Christie  
 9782070409341 Le Père Goriot           Honoré de Balzac 
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            books,
            "borderless",
            """\
 =============== ========================== ================== 
  ISBN            Title                      Author            
 =============== ========================== ================== 
  99921-58-10-7   Divine Comedy              Dante Alighieri   
  9971-5-0210-0   A Tale of Two Cities       Charles Dickens   
  960-425-059-0   The Lord of the Rings      J. R. R. Tolkien  
  80-902734-1-6   And Then There Were None   Agatha Christie   
  9782070409341   Le Père Goriot             Honoré de Balzac  
 =============== ========================== ================== 
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            books,
            "box",
            """\
┌───────────────┬──────────────────────────┬──────────────────┐
│ ISBN          │ Title                    │ Author           │
├───────────────┼──────────────────────────┼──────────────────┤
│ 99921-58-10-7 │ Divine Comedy            │ Dante Alighieri  │
│ 9971-5-0210-0 │ A Tale of Two Cities     │ Charles Dickens  │
│ 960-425-059-0 │ The Lord of the Rings    │ J. R. R. Tolkien │
│ 80-902734-1-6 │ And Then There Were None │ Agatha Christie  │
│ 9782070409341 │ Le Père Goriot           │ Honoré de Balzac │
└───────────────┴──────────────────────────┴──────────────────┘
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            [
                ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
                ["9971-5-0210-0", "A Tale of Two Cities", "Charles Dickens"],
                TableSeparator(),
                ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
                ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
            ],
            "box-double",
            """\
╔═══════════════╤══════════════════════════╤══════════════════╗
║ ISBN          │ Title                    │ Author           ║
╠═══════════════╪══════════════════════════╪══════════════════╣
║ 99921-58-10-7 │ Divine Comedy            │ Dante Alighieri  ║
║ 9971-5-0210-0 │ A Tale of Two Cities     │ Charles Dickens  ║
╟───────────────┼──────────────────────────┼──────────────────╢
║ 960-425-059-0 │ The Lord of the Rings    │ J. R. R. Tolkien ║
║ 80-902734-1-6 │ And Then There Were None │ Agatha Christie  ║
╚═══════════════╧══════════════════════════╧══════════════════╝
""",
        ),
        (
            ["ISBN", "Title"],
            [
                ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
                ["9971-5-0210-0"],
                ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
                ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
            ],
            "default",
            """\
+---------------+--------------------------+------------------+
| ISBN          | Title                    |                  |
+---------------+--------------------------+------------------+
| 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
| 9971-5-0210-0 |                          |                  |
| 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None | Agatha Christie  |
+---------------+--------------------------+------------------+
""",
        ),
        (
            [],
            [
                ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
                ["9971-5-0210-0"],
                ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
                ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
            ],
            "default",
            """\
+---------------+--------------------------+------------------+
| 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
| 9971-5-0210-0 |                          |                  |
| 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None | Agatha Christie  |
+---------------+--------------------------+------------------+
""",
        ),
        (
            ["ISBN", "Title"],
            [],
            "default",
            """\
+------+-------+
| ISBN | Title |
+------+-------+
""",
        ),
        ([], [], "default", ""),
        (
            ["ISBN", "Title", "Author"],
            [
                ["99921-58-10-7", "Divine\nComedy", "Dante Alighieri"],
                [
                    "9971-5-0210-2",
                    "Harry Potter\nand the Chamber of Secrets",
                    "Rowling\nJoanne K.",
                ],
                [
                    "9971-5-0210-2",
                    "Harry Potter\nand the Chamber of Secrets",
                    "Rowling\nJoanne K.",
                ],
                ["960-425-059-0", "The Lord of the Rings", "J. R. R.\nTolkien"],
            ],
            "default",
            """\
+---------------+----------------------------+-----------------+
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
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            [
                [
                    "<info>99921-58-10-7</info>",
                    "<error>Divine Comedy</error>",
                    "<fg=blue;bg=white>Dante Alighieri</fg=blue;bg=white>",
                ],
                ["9971-5-0210-0", "A Tale of Two Cities", "<info>Charles Dickens</>"],
            ],
            "default",
            """\
+---------------+----------------------+-----------------+
| ISBN          | Title                | Author          |
+---------------+----------------------+-----------------+
| 99921-58-10-7 | Divine Comedy        | Dante Alighieri |
| 9971-5-0210-0 | A Tale of Two Cities | Charles Dickens |
+---------------+----------------------+-----------------+
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            [
                ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
                TableSeparator(),
                [TableCell("Divine Comedy(Dante Alighieri)", colspan=3)],
                TableSeparator(),
                [TableCell("Arduino: A Quick-Start Guide", colspan=2), "Mark Schmidt"],
                TableSeparator(),
                ["9971-5-0210-0", TableCell("A Tale of \nTwo Cities", colspan=2)],
            ],
            "default",
            """\
+----------------+----------------+-----------------+
| ISBN           | Title          | Author          |
+----------------+----------------+-----------------+
| 99921-58-10-7  | Divine Comedy  | Dante Alighieri |
+----------------+----------------+-----------------+
| Divine Comedy(Dante Alighieri)                    |
+----------------+----------------+-----------------+
| Arduino: A Quick-Start Guide    | Mark Schmidt    |
+----------------+----------------+-----------------+
| 9971-5-0210-0  | A Tale of                        |
|                | Two Cities                       |
+----------------+----------------+-----------------+
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            [
                [
                    TableCell("9971-5-0210-0", rowspan=3),
                    "Divine Comedy",
                    "Dante Alighieri",
                ],
                ["A Tale of Two Cities", "Charles Dickens"],
                ["The Lord of \nthe Rings", "J. R. \nR. Tolkien"],
                TableSeparator(),
                [
                    "80-902734-1-6",
                    TableCell("And Then \nThere \nWere None", rowspan=3),
                    "Agatha Christie",
                ],
                ["80-902734-1-7", "Test"],
            ],
            "default",
            """\
+---------------+----------------------+-----------------+
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
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            [
                [TableCell("9971-5-0210-0", rowspan=2, colspan=2), "Dante Alighieri"],
                ["Charles Dickens"],
                TableSeparator(),
                ["Dante Alighieri", TableCell("9971-5-0210-0", rowspan=3, colspan=2)],
                ["J. R. R. Tolkien"],
                ["J. R. R"],
            ],
            "default",
            """\
+------------------+---------+-----------------+
| ISBN             | Title   | Author          |
+------------------+---------+-----------------+
| 9971-5-0210-0              | Dante Alighieri |
|                            | Charles Dickens |
+------------------+---------+-----------------+
| Dante Alighieri  | 9971-5-0210-0             |
| J. R. R. Tolkien |                           |
| J. R. R          |                           |
+------------------+---------+-----------------+
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            [
                [
                    TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2),
                    "Dante Alighieri",
                ],
                ["Charles Dickens"],
                TableSeparator(),
                [
                    "Dante Alighieri",
                    TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2),
                ],
                ["Charles Dickens"],
                TableSeparator(),
                [
                    TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2),
                    TableCell("Dante \nAlighieri", rowspan=2, colspan=1),
                ],
            ],
            "default",
            """\
+-----------------+-------+-----------------+
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
""",
        ),
        (
            ["ISBN", "Title", "Author"],
            [
                [
                    TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2),
                    "Dante Alighieri",
                ],
                ["Charles Dickens"],
                [
                    "Dante Alighieri",
                    TableCell("9971\n-5-\n021\n0-0", rowspan=2, colspan=2),
                ],
                ["Charles Dickens"],
            ],
            "default",
            """\
+-----------------+-------+-----------------+
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
""",
        ),
        (
            ["ISBN", "Author"],
            [
                [TableCell("9971-5-0210-0", rowspan=3, colspan=1), "Dante Alighieri"],
                [TableSeparator()],
                ["Charles Dickens"],
            ],
            "default",
            """\
+---------------+-----------------+
| ISBN          | Author          |
+---------------+-----------------+
| 9971-5-0210-0 | Dante Alighieri |
|               |-----------------|
|               | Charles Dickens |
+---------------+-----------------+
""",
        ),
        (
            [[TableCell("Main title", colspan=3)], ["ISBN", "Title", "Author"]],
            [],
            "default",
            """\
+------+-------+--------+
| Main title            |
+------+-------+--------+
| ISBN | Title | Author |
+------+-------+--------+
""",
        ),
        (
            [],
            [
                [
                    TableCell("1", colspan=3),
                    TableCell("2", colspan=2),
                    TableCell("3", colspan=2),
                    TableCell("4", colspan=2),
                ]
            ],
            "default",
            """\
+---+--+--+---+--+---+--+---+--+
| 1       | 2    | 3    | 4    |
+---+--+--+---+--+---+--+---+--+
""",
        ),
    ],
)
def test_render(
    io: BufferedIO, headers: list[str], rows: Rows, style: str, expected: str
) -> None:
    table = Table(io, style=style)
    table.set_headers(headers)
    table.set_rows(rows)

    table.render()

    assert io.fetch_output() == expected


def test_column_style(io: BufferedIO) -> None:
    table = Table(io)
    table.set_headers(["ISBN", "Title", "Author", "Price"])
    table.set_rows(
        [
            ["99921-58-10-7", "Divine Comedy", "Dante Alighieri", "9.95"],
            ["9971-5-0210-0", "A Tale of Two Cities", "Charles Dickens", "139.25"],
        ]
    )

    style = TableStyle()
    style.set_pad_type("left")
    table.set_column_style(3, style)

    table.render()

    expected = """\
+---------------+----------------------+-----------------+--------+
| ISBN          | Title                | Author          |  Price |
+---------------+----------------------+-----------------+--------+
| 99921-58-10-7 | Divine Comedy        | Dante Alighieri |   9.95 |
| 9971-5-0210-0 | A Tale of Two Cities | Charles Dickens | 139.25 |
+---------------+----------------------+-----------------+--------+
"""

    assert io.fetch_output() == expected


def test_style_for_side_effects(io: BufferedIO) -> None:
    headers = ["Type", "Class", "Name"]
    rows: Rows = [
        ["GSV", "Range", "Bora Horza Gobuchul"],
        ["GSV", "Plate", "Sleeper Service"],
        ["GCU", "Ridge", "Grey Area"],
        ["PS", "Abominator", "Falling Outside the Normal Moral Constraints"],
    ]

    table1 = Table(io)
    table1.set_headers(headers)
    table1.set_rows(rows)
    table1.style.set_vertical_border_chars("x", "y")
    table1.render()

    output1 = io.fetch_output()

    table2 = Table(io)
    table2.set_headers(headers)
    table2.set_rows(rows)
    table2.render()

    output2 = io.fetch_output()

    assert output1 != output2
