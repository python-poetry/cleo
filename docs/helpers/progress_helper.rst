Progress Helper
===============

When executing longer-running commands, it may be helpful to show progress
information, which updates as your command runs.

To display progress details, use the ``ProgressHelper`` class,
pass it a total number of units, and advance the progress as your command executes:

.. code-block:: python

    progress = self.get_helper_set().get('progress')

    progress.start(output_, 50)

    for _ in range(50)
        # ... do some work

        # advance the progress bar 1 unit
        progress.advance()
    }

    progress.finish()

.. tip::

    You can also set the current progress by calling the ``ProgressHelper.set_current()``
    method.

If you want to output something while the progress bar is running,
call ``ProgressHelper.clear()`` first.
After you're done, call ``ProgressHelper.display()``
to show the progress bar again.

The appearance of the progress output can be customized as well, with a number
of different levels of verbosity. Each of these displays different possible
items - like percentage completion, a moving progress bar, or current/total
information (e.g. 10/50):

.. code-block:: python

    progress.set_format(ProgressHelper.FORMAT_QUIET)
    progress.set_format(ProgressHelper.FORMAT_NORMAL)
    progress.set_format(ProgressHelper.FORMAT_VERBOSE)
    progress.set_format(ProgressHelper.FORMAT_QUIET_NOMAX)
    # the default value
    progress.set_format(ProgressHelper.FORMAT_NORMAL_NOMAX)
    progress.set_format(ProgressHelper.FORMAT_VERBOSE_NOMAX)

You can also control the different characters and the width used for the
progress bar:

.. code-block:: python

    # the finished part of the bar
    progress.set_bar_character('<comment>=</comment>')
    # the unfinished part of the bar
    progress.set_empty_bar_character(' ')
    progress.set_progress_character('|')
    progress.set_bar_width(50)

.. caution::

    For performance reasons, be careful if you set the total number of steps
    to a high number. For example, if you're iterating over a large number of
    items, consider setting the redraw frequency to a higher value by calling
    ``ProgressHelper.set_redraw_frequency()``, so it updates on only some iterations:

    .. code-block:: python

        progress.start(output_, 50000)

        # update every 100 iterations
        progress.set_redraw_frequency(100)

        for _ in range(50000)
            # ... do some work

            progress.advance()
