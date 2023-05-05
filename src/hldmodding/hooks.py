from typing import Callable


class _SubscriberMeta(type):
    def __new__(cls, name, bases, namespace):
        namespace['subscribed'] = []
        return super().__new__(cls, name, bases, namespace)


class _Subscriber(metaclass=_SubscriberMeta):

    subscribed: list[Callable] = []

    @classmethod
    def sub(cls, func: Callable) -> Callable:
        cls.subscribed.append(func)
        return func

    @classmethod
    def fire(cls) -> None:
        for func in cls.subscribed:
            func()


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


class Patch(_Subscriber):
    """

    patch hooks are hooks that are run before running the game
    so things like changing levels and patching new textures in go here

    """

    pass
