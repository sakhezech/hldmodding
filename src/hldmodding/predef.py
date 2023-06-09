from typing import Callable, Any
from hldlib import HLDLevelList
from hldmodding.hooks import Hook, Patch
from hldmodding.mini_controllers import MiniController
import ctypes as c

# MINI CONTROLLERS
# TODO: RENAME THIS
class controller:
    # TODO: WORKS FOR 7-21-2017 CHANGE TO SIG SCAN WHEN ITS READY
    class room_id(MiniController):
        addr = lambda x: x.resolve_pointer(x.base_addr + 0x255B1F10, [])
        c_type = c.c_int


# HOOKS
class on:

    class change:

        class room(Hook):
            @classmethod
            def dependency(cls) -> None:
                if controller.room_id.old != controller.room_id.new:
                    cls.fire()

    class patch:
        
        class pre(Patch):
            pass
        
        class post(Patch):
            pass
        
        class levels(Patch):
            @classmethod
            def sub(cls, func: Callable[[HLDLevelList], Any]) -> Callable[[HLDLevelList], Any]:
                cls._pending.append(func)
                return func

            @classmethod
            def fire(cls, levels: HLDLevelList, *args, **kwargs) -> None:
                for func in cls._subscribed:
                    func(levels, *args, **kwargs)
        
        class textures(Patch):
            pass