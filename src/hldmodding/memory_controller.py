import ctypes as c
from typing import Type, Any
from platform import system


class MemoryController:
    def __new__(cls):
        if system() == 'Windows':
            a = super().__new__(MemoryControllerWindows)
            a.__init__()
            return a
        else:
            raise NotImplementedError

    def read_from_addr(self, addr: int, c_type: Type) -> Any:
        raise NotImplementedError

    def write_to_addr(self, addr: int, value: Any) -> None:
        raise NotImplementedError


class MemoryControllerWindows:
    def __init__(self):
        user32 = c.WinDLL('User32.dll')
        self.kernel32 = c.WinDLL('Kernel32.dll')

        hWind = user32.FindWindowW(None, 'Hyper Light Drifter')
        pID = c.c_int()
        user32.GetWindowThreadProcessId(hWind, c.pointer(pID))
        # 0x001F0FF is PROCESS_ALL_ACCESS TODO: CHANGE TO BETTER ONE
        self.pHandle = self.kernel32.OpenProcess(0x001F0FFF, False, pID)

    def read_from_addr(self, addr: int, c_type: Type) -> Any:
        output = c_type()
        self.kernel32.ReadProcessMemory(
            self.pHandle, addr, c.pointer(output), c.sizeof(c_type), None
        )
        return output

    def write_to_addr(self, addr: int, value: Any) -> None:
        self.kernel32.WriteProcessMemory(
            self.pHandle, addr, c.pointer(value), c.sizeof(value), None
        )
