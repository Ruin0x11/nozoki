import ctypes, win32ui, win32process, win32api, struct, array

rPM = ctypes.windll.kernel32.ReadProcessMemory
wPM = ctypes.windll.kernel32.WriteProcessMemory

def convertData(data, kind, signed=False, littleEndian=False):
    endian = ">" # big endian
    if littleEndian:
        endian = "<"
    if signed:
        kind = kind.upper()
    dataFormat = endian + kind
    return struct.unpack(dataFormat, data.raw)[0]

class ProcessHandle:
    def __init__(self, windowName):
        PROCESS_ALL_ACCESS = 0x1F0FFF
        self.window = win32ui.FindWindow(None, windowName)
        HWND = self.window.GetSafeHwnd()
        PID = win32process.GetWindowThreadProcessId(HWND)[1]
        self.process = win32api.OpenProcess(PROCESS_ALL_ACCESS,0,PID)

    def focus(self):
        self.window.SetForegroundWindow()
        self.window.SetFocus()

    def readMemory(self, address, size):
        result = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        rPM(self.process.handle,address,result,size,ctypes.byref(bytes_read))
        return result

    def readByte(self, address, signed=False):
        return convertData(self.readMemory(address, 1), 'b', signed)

    def readShort(self, address, signed=False, littleEndian=False):
        return convertData(self.readMemory(address, 2), 'h', signed, littleEndian)
    
    def readInt(self, address, signed=False, littleEndian=False):
        return convertData(self.readMemory(address, 4), 'i', signed, littleEndian)
    
    def readString(self, address, size, encoding='shift-jis'):
        buf = self.readMemory(address, size).raw
        arr = array.array('h', buf)
        arr.byteswap()
        return buf.decode(encoding).split("\u0000")[0]
