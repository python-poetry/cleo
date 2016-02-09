### 0.4.1

##### Improvements

(February 9th, 2016)

- Adding support for Windows


### 0.4.0

(January 11th, 2016)

This a major release with some API changes.

##### Improvements

- The `Command` class is now more high-level with a single `handle()` method to override and useful helper methods
- Commands definition can now be specified with the class docstring (support for string signature)
- The ``ProgressHelper`` has been removed and the ``ProgressBar`` class must be used
- The `TableHelper` has largely been improved
- `DialogHelper` has been replaced by a more robust `QuestionHelper`
- Two other levels of verbosity (`-vv` and `-vvv`) have been added
- Commands description can now be output as json and markdown
- `Command.set_code()` logic has changed to accept a `Command` instance to be able to use the new helper methods
- Autocompletion has been improved


##### Fixes

* Values are now properly cast by validators
* Fixing "flag" not being set properly
* Progress bar now behaves properly (Fixes [#37](https://github.com/sdispater/cleo/issues/37))
* The `-n|--no-interaction` option behaves properly (Fixes [#38](https://github.com/sdispater/cleo/issues/39) and [#39](https://github.com/sdispater/cleo/issues/39))
