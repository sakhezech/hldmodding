from typing import Callable


class _HookMeta(type):
    def __new__(cls, name, bases, namespace):
        namespace['subscribed'] = []
        return super().__new__(cls, name, bases, namespace)


class Hook(metaclass=_HookMeta):
    """

    hooks are the thing that runs functions in a mod
    they are basically just pretty if statements

    on each cycle we are going to run dependency() which should run fire()

    so it should look something like

    class my_hook(Hook):
        @classmethod
        def dependency(cls):
            if something.old != something.new:
                cls.fire()

    and to subscribe a function to a hook do this

    @my_hook.sub
    def print_hello_on_hook():
        print('Hiii hello hi')

    """
    subscribed: list[Callable] = []

    @classmethod
    def sub(cls, func: Callable) -> Callable:
        cls.subscribed.append(func)
        return func

    @classmethod
    def fire(cls) -> None:
        for func in cls.subscribed:
            func()

    @classmethod
    def dependency(cls) -> None:
        raise NotImplementedError('No hook dependency implemented!')
