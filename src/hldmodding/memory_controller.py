import ctypes as c
import ctypes.wintypes as w
from typing import Type, Any
from platform import system


class MemoryControllerWindows:
    _user32 = None
    _kernel32 = None
    _hProcess = None
    _hWindow = None
    _pID = None
    base_addr = c.c_int(0)

    def __init__(self):
        self._user32: c.WinDLL = c.WinDLL('User32.dll')
        self._kernel32: c.WinDLL = c.WinDLL('Kernel32.dll')

        self._hWindow = self._user32.FindWindowW(None, 'Hyper Light Drifter')
        self._pID = c.c_int()
        self._user32.GetWindowThreadProcessId(
            self._hWindow, c.pointer(self._pID)
        )
        # 0x001F0FF is PROCESS_ALL_ACCESS TODO: CHANGE TO BETTER ONE
        self._hProcess = self._kernel32.OpenProcess(
            0x001F0FFF, False, self._pID
        )

        modules = (w.HMODULE * 1)(0)
        # 0x03 is LIST_MODULES_ALL
        self._kernel32.K32EnumProcessModulesEx(
            self._hProcess, c.pointer(modules), c.sizeof(w.HMODULE), None, 0x03
        )
        self.base_addr = modules[0]

    # TODO: MAYBE MAKE c_type DEFAULT TO c.c_double
    # BECAUSE ALMOST EVERY VALUE IN THE GAME IS A DOUBLE
    # WITH NOTABLE EXCEPTION BEING ROOMID WHICH IS c.c_int
    def read_from_addr(self, addr: int, c_type: Type) -> Any:
        output = c_type()
        self._kernel32.ReadProcessMemory(
            self._hProcess, addr, c.pointer(output), c.sizeof(c_type), None
        )
        return output

    # TODO: HANDLE WRONG TYPE OF VALUES
    # AND MAYBE TYPECAST TO c.c_double BY DEFAULT
    def write_to_addr(self, addr: int, value: Any) -> None:
        self._kernel32.WriteProcessMemory(
            self._hProcess, addr, c.pointer(value), c.sizeof(value), None
        )


class MemoryController:
    _systems = {
        'Windows': MemoryControllerWindows
    }

    base_addr = c.c_int(0)

    def __new__(cls):
        controller = super().__new__(cls._systems[system()])
        controller.__init__()
        return controller

    def read_from_addr(self, addr: int, c_type: Type) -> Any:
        raise NotImplementedError

    def write_to_addr(self, addr: int, value: Any) -> None:
        raise NotImplementedError
