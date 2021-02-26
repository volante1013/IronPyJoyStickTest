import clr
from generate import Generate

unmanaged_code = """
using System;
using System.Runtime.InteropServices;

namespace UnmanagedCode
{
	public class JoyStick
	{
		[DllImport("winmm.dll")]
		public static extern int joyGetNumDevs();

		[DllImport("winmm.dll")]
		public static extern int joyGetDevCaps(int uJoyID, ref JOYCAPS pjc, int cbjc);

		[DllImport("winmm.dll")]
		public static extern int joyGetPosEx(int uJoyID, ref JOYINFOEX pji);

		public static bool IsPressButton(int uJoyID, int buttonID)
		{
			var info = new JOYINFOEX();
			info.dwSize = (uint)Marshal.SizeOf(info);
			info.dwFlags = 0x0FF;
			var ret = joyGetPosEx(uJoyID, ref info);
			if (ret == 0 && info.dwButtons != 0 && (1 << buttonID & info.dwButtons) != 0)
			{
				return true;
			}
			return false;
		}
	}

	[StructLayout(LayoutKind.Sequential, Pack = 1)]
	public struct JOYINFOEX
	{
		public uint dwSize;
		public uint dwFlags;
		public uint dwXpos;
		public uint dwYpos;
		public uint dwZpos;
		public uint dwRpos;
		public uint dwUpos;
		public uint dwVpos;
		public uint dwButtons;
		public uint dwButtonNumber;
		public uint dwPOV;
		public uint dwReserved1;
		public uint dwReserved2;
	}

	[StructLayout(LayoutKind.Sequential, Pack = 1)]
	public struct JOYCAPS
	{
		public ushort wMid;
		public ushort wPid;
		[MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
		public string szPname;
		public uint wXmin;
		public uint wXmax;
		public uint wYmin;
		public uint wYmax;
		public uint wZmin;
		public uint wZmax;
		public uint wNumButtons;
		public uint wPeriodMin;
		public uint wPeriodMax;
		public uint wRmin;
		public uint wRmax;
		public uint wUmin;
		public uint wUmax;
		public uint wVmin;
		public uint wVmax;
		public uint wCaps;
		public uint wMaxAxes;
		public uint wNumAxes;
		public uint wMaxButtons;
		[MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
		public string szRegKey;
		[MarshalAs(UnmanagedType.ByValTStr, SizeConst = 260)]
		public string szOEMVxD;
	}
}
"""

assembly = Generate(unmanaged_code, "UnmanagedCode", inMemory=True)

clr.AddReference(assembly)

from UnmanagedCode import JoyStick, JOYINFOEX, JOYCAPS

num = JoyStick.joyGetNumDevs()
print(num)
for id in range(num):
	caps = JOYCAPS()
	ret, caps = JoyStick.joyGetDevCaps(id, caps, 404)
	print("[{}] {} ({})".format(id, caps.szPname, ret))
	if ret == 0:
		print(caps.szPname)
		break

while True:
	btns = [JoyStick.IsPressButton(id, i) for i in range(caps.wNumButtons)]
	print("buttons: ", btns)
