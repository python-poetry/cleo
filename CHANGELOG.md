# Change Log

## [0.6.7] - 2018-06-25

### Fixed

- Fixed verbosity option behavior.


## [0.6.6] - 2018-05-21

### Fixed

- Fixed an error for choice questions with only one choice.


## [0.6.5] - 2018-04-04

### Fixed

- Fixed handling of KeyboardInterrupt.


## [0.6.4] - 2018-03-15

### Fixed

- Fixed bad python version requirements.


## [0.6.3] - 2018-03-15

### Fixed

- Fixed bad python version requirements.


## [0.6.2] - 2018-03-15

### Changed

- Removed the memory formatter in progress bars and indicators

### Fixed

- Fixed an error in the `call()` method.


## [0.6.1] - 2017-08-07

### Changed

- `psutil` is now opt-in to avoid failed compilations.


## [0.6.0] - 2017-04-21

### Added

- Added a new `completions` command to generate autocompletion scripts.
- Added support for command signature inheritance.
- Added a new `spin()` helper to display a spinner.

### Changed

- Removed the `_completion` command.
- Removes ability to choose when a command name is ambiguous.


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



[Unreleased]: https://github.com/sdispater/cleo/compare/0.6.7...master
[0.6.7]: https://github.com/sdispater/cleo/releases/tag/0.6.7
[0.6.6]: https://github.com/sdispater/cleo/releases/tag/0.6.6
[0.6.5]: https://github.com/sdispater/cleo/releases/tag/0.6.5
[0.6.4]: https://github.com/sdispater/cleo/releases/tag/0.6.4
[0.6.3]: https://github.com/sdispater/cleo/releases/tag/0.6.3
[0.6.2]: https://github.com/sdispater/cleo/releases/tag/0.6.2
[0.6.1]: https://github.com/sdispater/cleo/releases/tag/0.6.1
[0.6.0]: https://github.com/sdispater/cleo/releases/tag/0.6.0
[0.5.0]: https://github.com/sdispater/cleo/releases/tag/0.5.0
[0.4.1]: https://github.com/sdispater/cleo/releases/tag/0.4.1
[0.4]: https://github.com/sdispater/cleo/releases/tag/0.4
