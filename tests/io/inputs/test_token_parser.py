from __future__ import annotations

import pytest

from cleo.io.inputs.token_parser import TokenParser


@pytest.mark.parametrize(
    "string, tokens",
    [
        ("", []),
        ("foo", ["foo"]),
        ("  foo  bar  ", ["foo", "bar"]),
        ('"quoted"', ["quoted"]),
        ("'quoted'", ["quoted"]),
        ("'a\rb\nc\td'", ["a\rb\nc\td"]),
        ("'a'\r'b'\n'c'\t'd'", ["a", "b", "c", "d"]),
        ("\"quoted 'twice'\"", ["quoted 'twice'"]),
        ("'quoted \"twice\"'", ['quoted "twice"']),
        ("\\'escaped\\'", ["'escaped'"]),
        ('\\"escaped\\"', ['"escaped"']),
        ("\\'escaped more\\'", ["'escaped", "more'"]),
        ('\\"escaped more\\"', ['"escaped', 'more"']),
        ("-a", ["-a"]),
        ("-azc", ["-azc"]),
        ("-awithavalue", ["-awithavalue"]),
        ('-a"foo bar"', ["-afoo bar"]),
        ('-a"foo bar""foo bar"', ["-afoo barfoo bar"]),
        ("-a'foo bar'", ["-afoo bar"]),
        ("-a'foo bar''foo bar'", ["-afoo barfoo bar"]),
        ("-a'foo bar'\"foo bar\"", ["-afoo barfoo bar"]),
        ("--long-option", ["--long-option"]),
        ("--long-option=foo", ["--long-option=foo"]),
        ('--long-option="foo bar"', ["--long-option=foo bar"]),
        ('--long-option="foo bar""another"', ["--long-option=foo baranother"]),
        ("--long-option='foo bar'", ["--long-option=foo bar"]),
        ("--long-option='foo bar''another'", ["--long-option=foo baranother"]),
        ("--long-option='foo bar'\"another\"", ["--long-option=foo baranother"]),
        ("foo -a -ffoo --long bar", ["foo", "-a", "-ffoo", "--long", "bar"]),
        ("\\' \\\"", ["'", '"']),
    ],
)
def test_create(string: str, tokens: list[str]) -> None:
    assert TokenParser().parse(string) == tokens
