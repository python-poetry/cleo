# -*- coding: utf-8 -*-

import re
import os
import hashlib
from ..._compat import encode


BASH_HOOK = '''# BASH completion for %%program_path%%
function %(function_name)s {

    # Copy BASH's completion variables to the ones the completion command expects
    # These line up exactly as the library was originally designed for BASH
    local CMDLINE_CONTENTS="$COMP_LINE"
    local CMDLINE_CURSOR_INDEX="$COMP_POINT"
    local CMDLINE_WORDBREAKS="$COMP_WORDBREAKS";

    export CMDLINE_CONTENTS CMDLINE_CURSOR_INDEX CMDLINE_WORDBREAKS

    local RESULT STATUS;

    RESULT="$(%(completion_command)s </dev/null)";
    STATUS=$?;

    local cur mail_check_backup;

    mail_check_backup=$MAILCHECK;
    MAILCHECK=-1;

    _get_comp_words_by_ref -n : cur;

    # Check if shell provided path completion is requested
    # @see Completion\ShellPathCompletion
    if [ $STATUS -eq 200 ]; then
        _filedir;
        return 0;

    # Bail out if PHP didn't exit cleanly
    elif [ $STATUS -ne 0 ]; then
        echo -e "$RESULT";
        return $?;
    fi;

    COMPREPLY=(`compgen -W "$RESULT" -- $cur`);

    __ltrim_colon_completions "$cur";

    MAILCHECK=mail_check_backup;
};

if [ "$(type -t _get_comp_words_by_ref)" == "function" ]; then
    complete -F %(function_name)s "%(program_name)s";
else
    >&2 echo "Completion was not registered for %(program_name)s:";
    >&2 echo "The 'bash-completion' package is required but doesn't appear to be installed.";
fi
'''

ZSH_HOOK = '''# ZSH completion for %%program_path%%
function %(function_name)s {
    local -x CMDLINE_CONTENTS="$words"
    local -x CMDLINE_CURSOR_INDEX
    (( CMDLINE_CURSOR_INDEX = ${#${(j. .)words[1,CURRENT]}} ))

    local RESULT STATUS
    RESULT=("${(@f)$( %(completion_command)s )}")
    STATUS=$?;

    # Check if shell provided path completion is requested
    # @see Completion\ShellPathCompletion
    if [ $STATUS -eq 200 ]; then
        _path_files;
        return 0;

    # Bail out if PHP didn't exit cleanly
    elif [ $STATUS -ne 0 ]; then
        echo -e "$RESULT";
        return $?;
    fi;

    compadd -- $RESULT
};

compdef %(function_name)s "%(program_name)s";
'''

class HookFactory(object):
    """
    Hook scripts

    These are shell-specific scripts that pass required information from that shell's
    completion system to the interface of the completion command in this module.
    """

    hooks = {
        'bash': BASH_HOOK,
        'zsh': ZSH_HOOK
    }

    def generate_hook(self, type, program_path, program_name=None, multiple=False):
        """
        Return a completion hook for the specified shell type

        :type type: str
        :type program_path: str
        :type program_name: str or None
        :type multiple: bool

        :rtype: str
        """
        if type not in self.hooks:
            raise RuntimeError(
                'Cannot generate hook for unknown shell type "%s". '
                'Available hooks are: %s'
                % (type, ', '.join(list(self.hooks.keys())))
            )

        # Use the program path if an alias/name is not given
        if not program_name:
            program_name = program_path

        if multiple:
            completion_command = '$1 _completion'
        else:
            completion_command = '%s _completion' % program_path

        hook = self._strip_comments(self.hooks[type])

        return hook % {
            'function_name': self._generate_function_name(program_path, program_name),
            'program_name': program_name,
            'program_path': program_path,
            'completion_command': completion_command
        }

    def _generate_function_name(self, program_path, program_name):
        return '_%s_%s_complete' % (
            self._sanitize_for_function_name(os.path.basename(program_name)),
            hashlib.md5(encode(program_path)).hexdigest()[0:16]
        )

    def _sanitize_for_function_name(self, name):
        name = name.replace('-', '_')

        return re.sub('[^A-Za-z0-9_]+', '', name)

    def _strip_comments(self, script):
        """
        :rtype: str
        """
        return re.sub('(?m)(^\s*\#.*$)', '', script)
