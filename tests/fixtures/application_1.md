UNKNOWN
=======

* help
* list

help
----

* Description: Displays help for a command
* Usage:

  * `help [--format FORMAT] [--raw] [--] [<command_name>]`

The <info>help</info> command displays help for a given command:

  <info>python app/console help list</info>

You can also output the help in other formats by using the <comment>--format</comment> option:

  <info>python app/console help --format=json list</info>

To display the list of available commands, please use the <info>list</info> command.

### Arguments:

**command_name:**

* Name: command_name
* Is required: no
* Is list: no
* Description: The command name
* Default: `help`

### Options:

**format:**

* Name: `--format`
* Shortcut: <none>
* Accept value: yes
* Is value required: yes
* Is multiple: no
* Description: The output format (txt, json, or md)
* Default: `txt`

**raw:**

* Name: `--raw`
* Shortcut: <none>
* Accept value: no
* Is value required: no
* Is multiple: no
* Description: To output raw command help
* Default: `False`

**help:**

* Name: `--help`
* Shortcut: `-h`
* Accept value: no
* Is value required: no
* Is multiple: no
* Description: Display this help message
* Default: `False`

**quiet:**

* Name: `--quiet`
* Shortcut: `-q`
* Accept value: no
* Is value required: no
* Is multiple: no
* Description: Do not output any message
* Default: `False`

**verbose:**

* Name: `--verbose`
* Shortcut: `-v|-vv|-vvv`
* Accept value: no
* Is value required: no
* Is multiple: no
* Description: Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug
* Default: `False`

**version:**

* Name: `--version`
* Shortcut: `-V`
* Accept value: no
* Is value required: no
* Is multiple: no
* Description: Display this application version
* Default: `False`

**ansi:**

* Name: `--ansi`
* Shortcut: <none>
* Accept value: no
* Is value required: no
* Is multiple: no
* Description: Force ANSI output
* Default: `False`

**no-ansi:**

* Name: `--no-ansi`
* Shortcut: <none>
* Accept value: no
* Is value required: no
* Is multiple: no
* Description: Disable ANSI output
* Default: `False`

**no-interaction:**

* Name: `--no-interaction`
* Shortcut: `-n`
* Accept value: no
* Is value required: no
* Is multiple: no
* Description: Do not ask any interactive question
* Default: `False`

list
----

* Description: Lists commands
* Usage:

  * `list [--raw] [--format FORMAT] [--] [<namespace>]`

The <info>list</info> command lists all commands:

  <info>python app/console list</info>

You can also display the commands for a specific namespace:

  <info>python app/console list test</info>

You can also output the information in other formats by using the <comment>--format</comment> option:

  <info>python app/console list --format=json</info>

It's also possible to get raw list of commands (useful for embedding command runner):

  <info>python app/console list --raw</info>

### Arguments:

**namespace:**

* Name: namespace
* Is required: no
* Is list: no
* Description: The namespace name
* Default: `None`

### Options:

**raw:**

* Name: `--raw`
* Shortcut: <none>
* Accept value: no
* Is value required: no
* Is multiple: no
* Description: To output raw command list
* Default: `False`

**format:**

* Name: `--format`
* Shortcut: <none>
* Accept value: yes
* Is value required: yes
* Is multiple: no
* Description: The output format (txt, json, or md)
* Default: `txt`
