from hldmodding.memory_controller import getMemoryController, MemoryController
from typing import Callable, Any
import ctypes as c


class _MiniControllerMeta(type):
    def __new__(cls, name, bases, namespace):
        namespace['old'] = None
        namespace['new'] = None
        return super().__new__(cls, name, bases, namespace)


class MiniController(metaclass=_MiniControllerMeta):

    addr: int | Callable[[MemoryController], int] = 0
    c_type = c.c_int
    old: Any = None
    new: Any = None
    
    # TODO: IF WE .VALUE THIS THEN WE CAN'T WORK WITH COMPLEX THINGS
    # IF I DON'T: WE HAVE TO .VALUE MANUALLY EVERY TIME
    # AND WE CAN'T DO self.old = None
    # NOTE: MAYBE CHECK c_type AND .VALUE THE RESULT ACCORDINGLY
    @classmethod
    def read(cls) -> Any:
        return cls._mc.read_from_addr(cls.addr, cls.c_type)

    @classmethod
    def write(cls, value: Any) -> None:
        cls._mc.write_to_addr(cls.addr, cls.c_type(value))
    
    @classmethod
    def update(cls) -> None:
        cls.old = cls.new
        cls.new = cls.read().value
    
    @classmethod
    def init(cls) -> None:
        cls._mc = getMemoryController()
        if callable(cls.addr):
            cls.addr = cls.addr(cls._mc)