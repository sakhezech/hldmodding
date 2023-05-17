from typing import Callable, Any
from pathlib import Path


class _SubscriberMeta(type):
    def __new__(cls, name, bases, namespace):
        namespace['_subscribed'] = []
        namespace['_pending'] = []
        return super().__new__(cls, name, bases, namespace)


class _Subscriber(metaclass=_SubscriberMeta):

    _subscribed: list[Callable] = []
    _pending: list[Callable] = []

    @classmethod
    def sub(cls, func: Callable) -> Callable:
        cls._pending.append(func)
        return func

    @classmethod
    def fire(cls, *args, **kwargs) -> None:
        for func in cls._subscribed:
            func(*args, **kwargs)


# TODO: RENAME DEPENDENCY TO SOMETHING ELSE
# OR TURN IT INTO DEPENDENCY ARRAY LIKE IN REACT
class Hook(_Subscriber):
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

    @classmethod
    def dependency(cls) -> None:
        raise NotImplementedError('No hook dependency implemented!')


# HOOKS SHOULD BE ABLE TO CREATE CUSTOM HOOKS FOR YOUR NEEDS
# BUT PATCHES SHOULD NOT BE
class Patch(_Subscriber):
    """

    patch hooks are hooks that are run before running the game
    so things like changing levels and patching new textures in go here

    """
    
    @classmethod
    def sub(cls, func: Callable[[str | Path], Any]) -> Callable[[str | Path], Any]:
        cls._pending.append(func)
        return func

    @classmethod
    def fire(cls, path: str | Path, *args, **kwargs) -> None:
        for func in cls._subscribed:
            func(path, *args, **kwargs)