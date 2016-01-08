Question Helper
###############

The ``QuestionHelper`` provides functions to ask the user for more information.
It is included in the default helper set and can be used either directly or via helper methods.


Asking the User for Confirmation
================================

Suppose you want to confirm an action before actually executing it. Add the following to your command:

.. code-block:: python

    def handle(self):
        if not self.confirm('Continue with this action?', False):
            return

In this case, the user will be asked "Continue with this action?".
If the user answers with ``y`` it returns ``True`` or ``False`` if they answer with ``n``.
The second argument to ``confirm()`` is the default value to return if the user doesn't enter any valid input.
If the second argument is not provided, ``True`` is assumed.

.. tip::

    You can customize the regex used to check if the answer means "yes" in the third argument of the ``customize()`` method.
    For instance, to allow anything that starts with either ``y`` or ``j``, you would set it to:

    .. code-block:: python

        self.confirm('Continue with this action?', False, '(?i)^(y|j)')

    The regex defaults to ``(?i)^y``.


Asking the User for Information
===============================

You can also ask a question with more than a simple yes/no answer.
For instance, if you want to know a user name, you can add this to your command:

.. code-block:: python

    def handle(self):
        name = self.ask('Please enter your name', 'John Doe')

The user will be asked "Please enter your name".
They can type some name which will be returned by the ``ask()`` method.
If they leave it empty, the default value (``John Doe`` here) is returned.
