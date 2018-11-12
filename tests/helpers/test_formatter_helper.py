# -*- coding: utf-8 -*-

from cleo.helpers import FormatterHelper

from .. import CleoTestCase


class FormatterHelperTest(CleoTestCase):
    def test_format_section(self):
        formatter = FormatterHelper()

        self.assertEqual(
            "<info>[cli]</info> Some text to display",
            formatter.format_section("cli", "Some text to display"),
        )

    def test_format_block(self):
        formatter = FormatterHelper()

        self.assertEqual(
            "<error> Some text to display </error>",
            formatter.format_block("Some text to display", "error"),
        )

        self.assertEqual(
            "<error> Some text to display </error>\n"
            "<error> foo bar              </error>",
            formatter.format_block(["Some text to display", "foo bar"], "error"),
        )

        self.assertEqual(
            "<error>                        </error>\n"
            "<error>  Some text to display  </error>\n"
            "<error>                        </error>",
            formatter.format_block("Some text to display", "error", True),
        )
