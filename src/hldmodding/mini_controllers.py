# TODO: THIS
# THESE ARE MEANT TO CONTROL ONE ADDR
# NAME SUBJECT TO CHANGE
# MINI CONTROLLERS MUST NOT BE INITTED ON LOAD
# OLD / NEW AND MORE IF NEEDED
# ADDR AND ADDR CHANGE

from hldmodding.memory_controller import getMemoryController, MemoryController
from typing import Type, Callable, Any


class MiniController:

    def __init__(self, addr: int | Callable[[MemoryController], int], c_type: Type) -> None:

        if callable(addr):
            self.addr = 0
            self._callable_addr = addr
        else:
            self.addr = addr
            self._callable_addr = None

        self.c_type = c_type
        self.old = None
        self.new = None
    
    # TODO: IF WE .VALUE THIS THEN WE CAN'T WORK WITH COMPLEX THINGS
    # IF I DON'T: WE HAVE TO .VALUE MANUALLY EVERY TIME
    # AND WE CAN'T DO self.old = None
    # NOTE: MAYBE CHECK c_type AND .VALUE THE RESULT ACCORDINGLY
    def read(self) -> Any:
        return self._mc.read_from_addr(self.addr, self.c_type).value

    def write(self, value: Any) -> None:
        self._mc.write_to_addr(self.addr, self.c_type(value))
    
    def update(self) -> None:
        self.old = self.new
        self.new = self.read()
        
    def init_mc(self) -> None:
        self._mc = getMemoryController()
        if self._callable_addr:
            self.addr: int = self._callable_addr(self._mc)