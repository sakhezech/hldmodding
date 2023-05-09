from typing import Callable, Any
from hldlib import HLDLevelList
from hldmodding.hooks import Hook, Patch
from hldmodding.mini_controllers import MiniController
import ctypes as c

# MINI CONTROLLERS
# TODO: RENAME THIS
class controller:
    # TODO: WORKS FOR 7-21-2017 CHANGE TO SIG SCAN WHEN ITS READY
    room_id = MiniController(
        lambda x: x.resolve_pointer(x.base_addr + 0x255B1F10, []),
        c.c_int
    )


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
            def fire(cls, levels: HLDLevelList) -> None:
                return super().fire(levels)

            @classmethod
            def sub(cls, func: Callable[[HLDLevelList], Any]) -> Callable[[HLDLevelList], Any]:
                return super().sub(func)
        
        class textures(Patch):
            pass