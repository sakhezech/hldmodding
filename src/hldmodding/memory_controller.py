import ctypes as c
import ctypes.wintypes as w
from typing import Type, Any


class MemoryController:

    base_addr = c.c_int(0)

    def read_from_addr(self, addr: int, c_type: Type) -> Any:
        raise NotImplementedError

    def write_to_addr(self, addr: int, value: Any) -> None:
        raise NotImplementedError

    def resolve_pointer(self, addr: int, offsets: list[int]) -> int:
        raise NotImplementedError

    def sig_scan(self, byte_array: bytes | str, mask: str | None) -> int:
        raise NotImplementedError


class MemoryControllerWindows(MemoryController):
    def __init__(self):
        self._user32 = c.WinDLL('User32.dll')  # type: ignore
        self._kernel32 = c.WinDLL('Kernel32.dll')  # type: ignore
        self._psapi = c.WinDLL('Psapi.dll')  # type: ignore

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

        module_info = (c.c_ulong * 3)(0)
        self._psapi.GetModuleInformation(
            self._hProcess, self.base_addr, c.pointer(module_info)
        )
        self._end_addr = module_info[2]

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

    def resolve_pointer(self, addr: int, offsets: list[int]) -> int:
        raise NotImplementedError

    def sig_scan(self, byte_array: bytes | str, mask: str | None) -> int:
        raise NotImplementedError


def getMemoryController(controller_type: str) -> MemoryController:
    controllers = {
        'Windows': MemoryControllerWindows,
    }
    return controllers[controller_type]()
