from __future__ import annotations

from cleo.commands.command import Command


class HelloCommand(Command):
    """
    Complete me please.

    hello
        { --dangerous-option= : This $hould be `escaped`. }
        { --option-without-description }
    """
