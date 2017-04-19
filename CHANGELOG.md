# Change Log

## [Unreleased]

### Added

- Added a new `completions` command to generate autocompletion scripts.

### Changed

- Removed the `_completion` command.


## [0.5.0] - 2016-09-21

### Added

- Improves terminal handling by adding the `Terminal` class.
- Adds methods to write to stderr.
- Adds `write()` and `overwrite()` method to commands.
- Adds ability to regress progress bar.
- Adds ability to choose when a command name is ambiguous.

### Changed

- Removes support for decorators and dictionaries declarations.
- Simplifies public API for creating arguments and options.
- Improves string formatting.
- Hides `_completion` command from list.
- Improves aliases display.
- Displays errors even in quiet mode
- Changes console header format
- Simplifies the way to create single command application.
- Simplifies command testing with user inputs.


## [0.4.1] - 2016-02-09

### Added

- Adding support for Windows


## [0.4] - 2016-01-11

This is a major release with some API changes.

### Added

- Commands definition can now be specified with the class docstring (support for string signature)
- Two other levels of verbosity (`-vv` and `-vvv`) have been added
- Commands description can now be output as json and markdown

### Changed

- The `Command` class is now more high-level with a single `handle()` method to override and useful helper methods
- The ``ProgressHelper`` has been removed and the ``ProgressBar`` class must be used
- The `TableHelper` has largely been improved
- `DialogHelper` has been replaced by a more robust `QuestionHelper`
- `Command.set_code()` logic has changed to accept a `Command` instance to be able to use the new helper methods
- Autocompletion has been improved

### Fixed

- Values are now properly cast by validators
- Fixing "flag" not being set properly
- Progress bar now behaves properly (Fixes [#37](https://github.com/sdispater/cleo/issues/37))
- The `-n|--no-interaction` option behaves properly (Fixes [#38](https://github.com/sdispater/cleo/issues/39) and [#39](https://github.com/sdispater/cleo/issues/39))



[Unreleased]: https://github.com/sdispater/cleo/compare/master...develop
[0.5.0]: https://github.com/sdispater/cleo/releases/tag/0.5.0
[0.4.1]: https://github.com/sdispater/cleo/releases/tag/0.4.1
[0.4]: https://github.com/sdispater/cleo/releases/tag/0.4
