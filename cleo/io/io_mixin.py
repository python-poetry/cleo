from clikit.ui.components import ChoiceQuestion
from clikit.ui.components import ConfirmationQuestion
from clikit.ui.components import ProgressBar
from clikit.ui.components import Question


class IOMixin(object):
    """
    Helpers for IO classes
    """

    def __init__(self, *args, **kwargs):
        super(IOMixin, self).__init__(*args, **kwargs)

        self._last_message = ""
        self._last_message_err = ""

    def progress_bar(self, max=0):  # type: (int) -> ProgressBar
        """
        Create a new progress bar
        """
        return ProgressBar(self, max)

    def ask(self, question, default=None):
        question = Question(question, default)

        return self.ask_question(question)

    def ask_hidden(self, question):
        question = Question(question)
        question.hide()

        return self.ask_question(question)

    def confirm(self, question, default=True, true_answer_regex="(?i)^y"):
        return self.ask_question(
            ConfirmationQuestion(question, default, true_answer_regex)
        )

    def choice(self, question, choices, default=None):
        if default is not None:
            default = choices[default]

        return self.ask_question(ChoiceQuestion(question, choices, default))

    def ask_question(self, question):
        """
        Asks a question.
        """
        answer = question.ask(self)

        return answer

    def write(self, string, flags=0):
        super(IOMixin, self).write(string, flags)

        self._last_message = string

    def error(self, string, flags=0):
        super(IOMixin, self).error(string, flags)

        self._last_message = string

    def write_line(self, string, flags=0):
        super(IOMixin, self).write_line(string, flags)

        self._last_message = string

    def error_line(self, string, flags=0):
        super(IOMixin, self).error_line(string, flags)

        self._last_message = string

    def overwrite(self, message, size=None):
        self._do_overwrite(message, size)

    def overwrite_error(self, message, size=None):
        self._do_overwrite(message, size, True)

    def _do_overwrite(self, message, size=None, stderr=False):
        output = self.output
        if stderr:
            output = self.error_output

        # since overwrite is supposed to overwrite last message...
        if size is None:
            # removing possible formatting of lastMessage with strip_tags
            if stderr:
                last_message = self._last_message_err
            else:
                last_message = self._last_message

            size = len(output.remove_format(last_message))

        # ...let's fill its length with backspaces
        output.write("\x08" * size)

        # write the new message
        output.write(message)

        fill = size - len(output.remove_format(message))

        if fill > 0:
            # whitespace whatever has left
            output.write(" " * fill)
            # move the cursor back
            output.write("\x08" * fill)

        if stderr:
            self._last_message_err = message
        else:
            self._last_message = message
