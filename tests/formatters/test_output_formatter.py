# -*- coding: utf-8 -*-

from cleo.formatters import Formatter

from .. import CleoTestCase


class OutputFormatterTest(CleoTestCase):
    def test_empty_tag(self):
        formatter = Formatter(True)
        self.assertEqual("foo<>bar", formatter.format("foo<>bar"))

    def test_lg_char_escaping(self):
        formatter = Formatter(True)

        self.assertEqual("foo<bar", formatter.format("foo\\<bar"))
        self.assertEqual(
            "<info>some info</info>", formatter.format("\\<info>some info\\</info>")
        )
        self.assertEqual(
            "\\<info>some info\\</info>", Formatter.escape("<info>some info</info>")
        )

    def test_bundled_styles(self):
        formatter = Formatter(True)

        self.assertTrue(formatter.has_style("error"))
        self.assertTrue(formatter.has_style("info"))
        self.assertTrue(formatter.has_style("comment"))
        self.assertTrue(formatter.has_style("question"))

        self.assertEqual(
            "\033[37;41msome error\033[0m",
            formatter.format("<error>some error</error>"),
        )
        self.assertEqual(
            "\033[32msome info\033[0m", formatter.format("<info>some info</info>")
        )
        self.assertEqual(
            "\033[33msome comment\033[0m",
            formatter.format("<comment>some comment</comment>"),
        )
        self.assertEqual(
            "\033[30;46msome question\033[0m",
            formatter.format("<question>some question</question>"),
        )

    def test_nested_styles(self):
        formatter = Formatter(True)

        self.assertEqual(
            "\033[37;41msome \033[0m\033[32msome info\033[0m\033[37;41m error\033[0m",
            formatter.format("<error>some <info>some info</info> error</error>"),
        )

    def test_adjacent_style(self):
        formatter = Formatter(True)

        self.assertEqual(
            "\033[37;41msome error\033[0m\033[32msome info\033[0m",
            formatter.format("<error>some error</error><info>some info</info>"),
        )

    def test_style_matching_non_greedy(self):
        formatter = Formatter(True)

        self.assertEqual(
            "(\033[32m>=2.0,<2.3\033[0m)", formatter.format("(<info>>=2.0,<2.3</info>)")
        )

    def test_style_escaping(self):
        formatter = Formatter(True)

        self.assertEqual(
            "(\033[32mz>=2.0,<a2.3\033[0m)",
            formatter.format("(<info>%s</info>)" % formatter.escape("z>=2.0,<a2.3")),
        )

    def test_deep_nested_style(self):
        formatter = Formatter(True)

        self.assertEqual(
            "\033[37;41merror\033[0m\033[32minfo\033[0m\033[33mcomment\033[0m\033[37;41merror\033[0m",
            formatter.format(
                "<error>error<info>info<comment>comment</comment></info>error</error>"
            ),
        )

    def test_new_style(self):
        formatter = Formatter(True)

        formatter.add_style("test", "blue", "white")
        formatter.add_style("b", "blue", "white")

        self.assertEqual(
            "\033[34;47msome \033[0m\033[34;47mcustom\033[0m\033[34;47m msg\033[0m",
            formatter.format("<test>some <b>custom</b> msg</test>"),
        )

    def test_redefined_style(self):
        formatter = Formatter(True)

        formatter.add_style("info", "blue", "white")

        self.assertEqual(
            "\033[34;47msome custom msg\033[0m",
            formatter.format("<info>some custom msg</info>"),
        )

    def test_inline_style(self):
        formatter = Formatter(True)

        self.assertEqual(
            "\033[34;41msome text\033[0m",
            formatter.format("<fg=blue;bg=red>some text</>"),
        )
        self.assertEqual(
            "\033[34;41msome text\033[0m",
            formatter.format("<fg=blue;bg=red>some text</fg=blue;bg=red>"),
        )
        self.assertEqual(
            "\033[34;41;1msome text\033[0m",
            formatter.format("<fg=blue;bg=red;options=bold>some text</>"),
        )

    def test_non_style_tag(self):
        formatter = Formatter(True)
        self.assertEqual(
            "\033[32msome \033[0m\033[32m<tag>\033[0m\033[32m \033[0m\033[32m<setting=value>\033[0m\033[32m"
            " styled \033[0m\033[32m<p>\033[0m\033[32msingle-char tag\033[0m\033[32m</p>\033[0m",
            formatter.format(
                "<info>some <tag> <setting=value> styled <p>single-char tag</p></info>"
            ),
        )

    def test_test_non_decorated_formatter(self):
        formatter = Formatter(False)

        self.assertTrue(formatter.has_style("error"))
        self.assertTrue(formatter.has_style("info"))
        self.assertTrue(formatter.has_style("comment"))
        self.assertTrue(formatter.has_style("question"))

        self.assertEqual("some error", formatter.format("<error>some error</error>"))
        self.assertEqual("some info", formatter.format("<info>some info</info>"))
        self.assertEqual(
            "some comment", formatter.format("<comment>some comment</comment>")
        )
        self.assertEqual(
            "some question", formatter.format("<question>some question</question>")
        )

        formatter.set_decorated(True)

        self.assertEqual(
            "\033[37;41msome error\033[0m",
            formatter.format("<error>some error</error>"),
        )
        self.assertEqual(
            "\033[32msome info\033[0m", formatter.format("<info>some info</info>")
        )
        self.assertEqual(
            "\033[33msome comment\033[0m",
            formatter.format("<comment>some comment</comment>"),
        )
        self.assertEqual(
            "\033[30;46msome question\033[0m",
            formatter.format("<question>some question</question>"),
        )

    def test_content_with_line_breaks(self):
        formatter = Formatter(True)

        for expected, message in self.provide_content_with_line_breaks():
            self.assertEqual(expected, formatter.format(message))

    def provide_content_with_line_breaks(self):
        return [
            (
                """\033[32m
some text\033[0m""",
                """<info>
some text</info>""",
            ),
            (
                """\033[32msome text
\033[0m""",
                """<info>some text
</info>""",
            ),
            (
                """\033[32m
some text
\033[0m""",
                """<info>
some text
</info>""",
            ),
            (
                """\033[32m
some text
more text
\033[0m""",
                """<info>
some text
more text
</info>""",
            ),
        ]
