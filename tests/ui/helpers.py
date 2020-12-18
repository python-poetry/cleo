def outer():
    def inner():
        raise Exception("Foo")

    inner()
