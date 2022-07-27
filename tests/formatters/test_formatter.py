from __future__ import annotations

import pytest

from cleo.formatters.formatter import Formatter


@pytest.mark.parametrize(
    ["text", "width", "expected"],
    [
        (
            "foo<error>bar</error> baz",
            2,
            "fo\no\x1b[31;1mb\x1b[39;22m\n\x1b[31;1mar\x1b[39;22m\nba\nz",
        ),
        (
            "pre <error>foo bar baz</error> post",
            2,
            (
                "pr\ne \x1b[31;1m\x1b[39;22m\n\x1b[31;1mfo\x1b[39;22m\n\x1b[31;1mo "
                "\x1b[39;22m\n\x1b[31;1mba\x1b[39;22m\n\x1b[31;1mr "
                "\x1b[39;22m\n\x1b[31;1mba"
                "\x1b[39;22m\n\x1b[31;1mz\x1b[39;22m \npo\nst"
            ),
        ),
        (
            "pre <error>foo bar baz</error> post",
            3,
            (
                "pre\x1b[31;1m\x1b[39;22m\n\x1b[31;1mfoo\x1b[39;22m\n\x1b"
                "[31;1mbar\x1b[39;22m\n\x1b[31;1mbaz\x1b[39;22m\npos\nt"
            ),
        ),
        (
            "pre <error>foo bar baz</error> post",
            4,
            (
                "pre \x1b[31;1m\x1b[39;22m\n\x1b[31;1mfoo \x1b[39;22m\n\x1b"
                "[31;1mbar \x1b[39;22m\n\x1b[31;1mbaz\x1b[39;22m \npost"
            ),
        ),
        (
            "pre <error>foo bar baz</error> post",
            5,
            (
                "pre \x1b[31;1mf\x1b[39;22m\n\x1b[31;1moo ba\x1b"
                "[39;22m\n\x1b[31;1mr baz\x1b[39;22m\npost"
            ),
        ),
        (
            "Lorem <error>ipsum</error> dolor <info>sit</info> amet",
            4,
            (
                "Lore\nm \x1b[31;1mip\x1b[39;22m\n\x1b[31;1msum\x1b[39;22m "
                "\ndolo\nr \x1b[34msi\x1b[39m\n\x1b[34mt\x1b[39m am\net"
            ),
        ),
        (
            "Lorem <error>ipsum</error> dolor <info>sit</info> amet",
            8,
            (
                "Lorem \x1b[31;1mip\x1b[39;22m\n\x1b[31;1msum\x1b"
                "[39;22m dolo\nr \x1b[34msit\x1b[39m am\net"
            ),
        ),
        (
            (
                "Lorem <error>ipsum</error> dolor <info>sit</info>, "
                "<error>amet</error> et <info>laudantium</info> architecto"
            ),
            18,
            (
                "Lorem \x1b[31;1mipsum\x1b[39;22m dolor \x1b[34m\x1b[39m\n\x1b"
                "[34msit\x1b[39m, \x1b[31;1mamet\x1b[39;22m et \x1b[34mlauda\x1b"
                "[39m\n\x1b[34mntium\x1b[39m architecto"
            ),
        ),
    ],
)
def test_format_and_wrap(text: str, width: int, expected: str) -> None:
    formatter = Formatter(True)

    assert formatter.format_and_wrap(text, width) == expected


@pytest.mark.parametrize(
    ["text", "width", "expected"],
    [
        ("foo<error>bar</error> baz", 2, "fo\nob\nar\nba\nz"),
        (
            "pre <error>foo bar baz</error> post",
            2,
            "pr\ne \nfo\no \nba\nr \nba\nz \npo\nst",
        ),
        ("pre <error>foo bar baz</error> post", 3, "pre\nfoo\nbar\nbaz\npos\nt"),
        ("pre <error>foo bar baz</error> post", 4, "pre \nfoo \nbar \nbaz \npost"),
        ("pre <error>foo bar baz</error> post", 5, "pre f\noo ba\nr baz\npost"),
    ],
)
def test_format_and_wrap_undecorated(text: str, width: int, expected: str) -> None:
    formatter = Formatter(False)

    assert formatter.format_and_wrap(text, width) == expected
