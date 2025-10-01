
def raiser_with_suppressed_context() -> None:
    try:
        raise ValueError("This error should be suppressed.")
    except ValueError:
        raise RuntimeError("This error should be displayed.") from None
