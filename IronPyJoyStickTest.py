import ctypes

def throwException(e, str):
	import traceback
	print("[Exception]{0}".format(str))
	print(traceback.format_exc())
	print(e)

try:
	winmmdll = ctypes.WinDLL('winmm.dll')

	# [joyGetNumDevs](https://docs.microsoft.com/en-us/windows/win32/api/joystickapi/nf-joystickapi-joygetnumdevs)
	"""
	UINT joyGetNumDevs();
	"""
	joyGetNumDevs_proto = ctypes.WINFUNCTYPE(ctypes.c_uint)
	# joyGetNumDevs_func  = joyGetNumDevs_proto(("joyGetNumDevs", winmmdll))
	joyGetNumDevs_func  = winmmdll.joyGetNumDevs

	# [joyGetDevCaps](https://docs.microsoft.com/en-us/windows/win32/api/joystickapi/nf-joystickapi-joygetdevcaps)
	"""
	MMRESULT joyGetDevCaps(UINT uJoyID, LPJOYCAPS pjc, UINT cbjc);

	32 bit: joyGetDevCapsA
	64 bit: joyGetDevCapsW

	sizeof(JOYCAPS): 728
	"""
	joyGetDevCaps_proto = ctypes.WINFUNCTYPE(ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint)
	joyGetDevCaps_param = (1, "uJoyID", 0), (1, "pjc", None), (1, "cbjc", 0)
	# joyGetDevCaps_func  = joyGetDevCaps_proto(("joyGetDevCapsW", winmmdll), joyGetDevCaps_param)
	joyGetDevCaps_func  = winmmdll.joyGetDevCapsW

	# [joyGetPosEx](https://docs.microsoft.com/en-us/windows/win32/api/joystickapi/nf-joystickapi-joygetposex)
	"""
	MMRESULT joyGetPosEx(UINT uJoyID, LPJOYINFOEX pji);
	sizeof(JOYINFOEX): 52
	"""
	joyGetPosEx_proto = ctypes.WINFUNCTYPE(ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p)
	joyGetPosEx_param = (1, "uJoyID", 0), (1, "pji", None)
	# joyGetPosEx_func  = joyGetPosEx_proto(("joyGetPosEx", winmmdll), joyGetPosEx_param)
	joyGetPosEx_func  = winmmdll.joyGetPosEx
except Exception as e:
	throwException(e, "JoyInit")
	winmmdll = None

# joystickapi - joyGetNumDevs
def joyGetNumDevs():
	try:
		num = joyGetNumDevs_func()
	except Exception as e:
		throwException(e, "JoyInit")
		num = 0
	return num

# joystickapi - joyGetDevCaps
def joyGetDevCaps(uJoyID):
	try:
		buffer = (ctypes.c_ubyte * JOYCAPS.SIZE_W)()
		p1 = ctypes.c_uint(uJoyID)
		p2 = ctypes.cast(buffer, ctypes.c_void_p)
		p3 = ctypes.c_uint(JOYCAPS.SIZE_W)
		ret_val = joyGetDevCaps_func(p1, p2, p3)
		ret = (False, None) if ret_val != JOYERR_NOERROR else (True, JOYCAPS(buffer))   
	except Exception as e:
		throwException(e, "joyGetDevCaps")
		ret = False, None
	return ret 

# joystickapi - joyGetPosEx
def joyGetPosEx(uJoyID):
	try:
		buffer = (ctypes.c_uint32 * (JOYINFOEX.SIZE // 4))()
		buffer[0] = JOYINFOEX.SIZE
		buffer[1] = JOY_RETURNALL
		p1 = ctypes.c_uint(uJoyID)
		p2 = ctypes.cast(buffer, ctypes.c_void_p)
		ret_val = joyGetPosEx_func(p1, p2)
		ret = (False, None) if ret_val != JOYERR_NOERROR else (True, JOYINFOEX(buffer))   
	except Exception as e:
		throwException(e, "joyGetPosEx")
		ret = False, None
	return ret 

JOYERR_NOERROR = 0
JOY_RETURNX = 0x00000001
JOY_RETURNY = 0x00000002
JOY_RETURNZ = 0x00000004
JOY_RETURNR = 0x00000008
JOY_RETURNU = 0x00000010
JOY_RETURNV = 0x00000020
JOY_RETURNPOV = 0x00000040
JOY_RETURNBUTTONS = 0x00000080
JOY_RETURNRAWDATA = 0x00000100
JOY_RETURNPOVCTS = 0x00000200
JOY_RETURNCENTERED = 0x00000400
JOY_USEDEADZONE = 0x00000800
JOY_RETURNALL = (JOY_RETURNX | JOY_RETURNY | JOY_RETURNZ | \
				 JOY_RETURNR | JOY_RETURNU | JOY_RETURNV | \
				 JOY_RETURNPOV | JOY_RETURNBUTTONS)

# joystickapi - JOYCAPS
class JOYCAPS:
	SIZE_W = 728
	OFFSET_V = 4 + 32*2
	def __init__(self, buffer):
		self.wMid = (ctypes.c_uint16).from_buffer(buffer)
		#ushort_array = (ctypes.c_uint16 * 2).from_buffer(buffer)
		#self.wMid, self.wPid = ushort_array  

		wchar_array = (ctypes.c_wchar * 32).from_buffer(buffer, 4)
		self.szPname = ctypes.cast(wchar_array, ctypes.c_wchar_p).value
		
		uint_array = (ctypes.c_uint32 * 19).from_buffer(buffer, JOYCAPS.OFFSET_V) 
		self.wXmin, self.wXmax, self.wYmin, self.wYmax, self.wZmin, self.wZmax, \
		self.wNumButtons, self.wPeriodMin, self.wPeriodMax, \
		self.wRmin, self.wRmax, self.wUmin, self.wUmax, self.wVmin, self.wVmax, \
		self.wCaps, self.wMaxAxes, self.wNumAxes, self.wMaxButtons = uint_array

# joystickapi - JOYINFOEX
class JOYINFOEX:
	SIZE = 52
	def __init__(self, buffer):
		uint_array = (ctypes.c_uint32 * (JOYINFOEX.SIZE // 4)).from_buffer(buffer) 
		self.dwSize, self.dwFlags, \
		self.dwXpos, self.dwYpos, self.dwZpos, self.dwRpos, self.dwUpos, self.dwVpos, \
		self.dwButtons, self.dwButtonNumber, self.dwPOV, self.dwReserved1, self.dwReserved2 = uint_array

import msvcrt
import time

print("start")

num = joyGetNumDevs()
ret, caps, startinfo = False, None, None
for id in range(num):
	ret, caps = joyGetDevCaps(id)
	if ret:
		print("gamepad detected: " + caps.szPname)
		ret, startinfo = joyGetPosEx(id)
		break
else:
	print("no gamepad detected")

run = ret
while run:
	time.sleep(0.1)
	if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode(): # detect ESC
		run = False

	ret, info = joyGetPosEx(id)
	if ret:
		btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
		axisXYZ = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos]
		axisRUV = [info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]
		if info.dwButtons:
			print("buttons: ", btns)
		if any([abs(v) > 10 for v in axisXYZ]):
			print("axis:", axisXYZ)
		if any([abs(v) > 10 for v in axisRUV]):
			print("roation axis:", axisRUV)

print("end")