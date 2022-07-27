from crashtest.contracts.base_solution import BaseSolution
from crashtest.contracts.provides_solution import ProvidesSolution


# mypy fails here because crashtest is not typed.
class CustomError(ProvidesSolution, Exception):  # type: ignore
    @property
    def solution(self) -> BaseSolution:
        solution = BaseSolution("Solution Title.", "Solution Description")
        solution.documentation_links.append("https://example.com")
        solution.documentation_links.append("https://example2.com")

        return solution


def call() -> None:
    raise CustomError("Error with solution")
