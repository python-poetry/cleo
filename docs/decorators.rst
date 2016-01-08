Declaring Commands via Decorators
#################################

.. versionchanged:: 0.4

    The signature of decorated functions has changed.
    In previous version, decorated functions should be in the form:

    .. code-block:: python

        def decorated(i, o):
            """
            :type i: Input
            :type o: Output
            """

    As of **0.4**, they should be in the form:

    .. code-block:: python

        def decorated(c):
            """
            :type c: Command
            """

    ``c`` being a ``Command`` instance giving you access to all helper methods.


Commands can also be simple functions decorated by special decorators.

.. code-block:: python

    from cleo import Application

    app = Application()

    @app.command('demo:greet', description='Greets someone')
    @app.argument('name', description='Who do you want to greet?', required=False)
    @app.option('yell', description='If set, the task will yell in uppercase letters',
                flag=True)
    def greet(c):
        name = c.argument('name')
        if name:
            text = 'Hello %s' % name
        else:
            text = 'Hello'

        if c.option('yell'):
            text = text.upper()

        c.line(text)


Using Arguments
===============

.. role:: python(code)
   :language: python

Here are all corresponding declaration of argument mode:

=========================== ==================================== ===============================================================================================================
Mode                        Notation                             Value
=========================== ==================================== ===============================================================================================================
``InputArgument.REQUIRED``  :python:`required=True`              The argument is required
``InputArgument.OPTIONAL``  :python:`required=False`             The argument is optional and therefore can be omitted
``InputArgument.IS_LIST``   :python:`is_list=True`               The argument can contain an indefinite number of arguments and must be used at the end of the argument list
=========================== ==================================== ===============================================================================================================


Using Options
=============

.. role:: python(code)
   :language: python

Here are all corresponding declaration of option mode:

===============================  =================================== ======================================================================================
Option                           Notation                            Value
===============================  =================================== ======================================================================================
``InputOption.VALUE_IS_LIST``    :python:`is_list=True`              This option accepts multiple values (e.g. ``--dir=/foo --dir=/bar``)
``InputOption.VALUE_NONE``       :python:`flag=True`                 Do not accept input for this option (e.g. ``--yell``)
``InputOption.VALUE_REQUIRED``   :python:`value_required=True`       This value is required (e.g. ``--iterations=5``), the option itself is still optional
``InputOption.VALUE_OPTIONAL``   :python:`value_required=False`      This option may or may not have a value (e.g. ``--yell`` or ``--yell=loud``)
===============================  =================================== ======================================================================================
