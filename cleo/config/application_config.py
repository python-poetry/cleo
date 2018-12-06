from clikit.config import DefaultApplicationConfig

from cleo.io import ConsoleIO


class ApplicationConfig(DefaultApplicationConfig):
    """
    Cleo's default application configuration.
    """

    def configure(self):  # type: () -> None
        super(ApplicationConfig, self).configure()

    @property
    def io_class(self):
        return ConsoleIO
