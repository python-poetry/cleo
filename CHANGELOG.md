### 0.4.0

This a major release with some API changes.

##### Improvements

- The `Command` class is now more high-level with a single `handle()` method to override and useful helper methods
- Commands definition can now be defined with the class docstring
- The ``ProgressHelper`` has been removed and the ``ProgressBar`` class must be used
- The `TableHelper` has largely been improved
- `DialogHelper` has been replaced by a more robust `QuestionHelper`
- Two other levels of verbosity (`-vv` and `-vvv`) have been added
- Commands description can now be output as json and markdown
- `Command.set_code()` method has changed to accept a `Command` instance to be able to use the new helper methods
- Autocompletion has been improved


##### Fixes

* Values are now properly casted by validators
* Fixing "flag" not being set properly
* Progress bar now behave properly (Fixes [#37](https://github.com/sdispater/cleo/issues/37))
* The `-n|--no-interaction` option behaves properly (Fixes [#38](https://github.com/sdispater/cleo/issues/39) and [#39](https://github.com/sdispater/cleo/issues/39))
