#!/bin/bash

if [[ -n ${ZSH_VERSION-} ]]; then
    autoload -U +X bashcompinit && bashcompinit
fi

_complete_console() {
    local cur

    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"

    # Assume first word is the actual app/console command
    console="${COMP_WORDS[0]}"

    if [[ ${COMP_CWORD} == 1 ]] ; then
        # No command found, return the list of available commands
        cmds=` ${console} | sed -n -e '/^Available commands/,//p' | grep '^ ' | awk '{ print $1 }' `
    else
        # Commands found, parse options
        cmds=` ${console} ${COMP_WORDS[1]} --help | sed -n -e '/^Options/,/^$/p' | grep '^ ' | awk '{ print $1 }' `
    fi

    COMPREPLY=( $(compgen -W "${cmds}" -- ${cur}) )
    return 0
}

export COMP_WORDBREAKS="\ \"\\'><=;|&("

complete -F _complete_console console
