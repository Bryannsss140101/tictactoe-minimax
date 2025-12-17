import os
import sys
import time
import subprocess
import tkinter as tk
from pathlib import Path

try:
    import winsound
except Exception:
    winsound = None

EASTER_FLAG = Path(".easter_seen")


def _beep(root, ms=2000):
    if winsound is not None:
        try:
            winsound.Beep(800, int(ms))
            return
        except Exception:
            pass
    try:
        root.bell()
    except Exception:
        pass


def _open_video(video_path: str):
    video_path = os.path.abspath(video_path)

    if sys.platform.startswith("win"):
        os.startfile(video_path)
        return

    if sys.platform == "darwin":
        subprocess.Popen(["open", video_path])
        return

    subprocess.Popen(["xdg-open", video_path])


def _show_desktop():
    plat = sys.platform
    try:
        if plat.startswith("win"):
            import ctypes

            user32 = ctypes.windll.user32
            VK_LWIN = 0x5B
            VK_D = 0x44
            KEYEVENTF_KEYUP = 0x0002

            user32.keybd_event(VK_LWIN, 0, 0, 0)
            user32.keybd_event(VK_D, 0, 0, 0)
            user32.keybd_event(VK_D, 0, KEYEVENTF_KEYUP, 0)
            user32.keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0)
            return

        if plat == "darwin":
            subprocess.Popen(
                [
                    "osascript",
                    "-e",
                    'tell application "System Events" to key code 103 using {command down}',
                ]
            )
            return

        try:
            subprocess.Popen(["xdotool", "key", "super+d"])
            return
        except Exception:
            pass

        try:
            subprocess.Popen(["wmctrl", "-k", "on"])
            return
        except Exception:
            pass

    except Exception:
        pass


def _volume_up(steps=10):
    plat = sys.platform
    try:
        if plat.startswith("win"):
            import ctypes

            user32 = ctypes.windll.user32
            VK_VOLUME_UP = 0xAF
            KEYEVENTF_KEYUP = 0x0002
            for _ in range(int(steps)):
                user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
                user32.keybd_event(VK_VOLUME_UP, 0, KEYEVENTF_KEYUP, 0)
            return

        if plat == "darwin":
            subprocess.Popen(["osascript", "-e", "set volume output volume 80"])
            return

        try:
            subprocess.Popen(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+20%"])
            return
        except Exception:
            pass

        try:
            subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", "20%+"])
            return
        except Exception:
            pass

    except Exception:
        pass


def _brightness_set(percent=80):
    plat = sys.platform
    p = int(max(0, min(100, percent)))

    try:
        if plat == "darwin":
            subprocess.Popen(["brightness", f"{p/100:.2f}"])
            return

        if plat.startswith("linux"):
            try:
                subprocess.Popen(["brightnessctl", "set", f"{p}%"])
                return
            except Exception:
                pass
            try:
                subprocess.Popen(["xbacklight", "-set", str(p)])
                return
            except Exception:
                pass

    except Exception:
        pass


def run(
    root: tk.Tk,
    video_path: str,
    seconds: int = 130,
    beep_ms: int = 2500,
    volume_steps: int = 12,
    brightness_percent: int | None = None,
):
    if EASTER_FLAG.exists():
        return

    if getattr(root, "_easter_running", False):
        return
    root._easter_running = True

    video_path = os.path.abspath(video_path)

    try:
        EASTER_FLAG.touch()
    except Exception:
        pass

    _show_desktop()
    _volume_up(volume_steps)

    if brightness_percent is not None:
        _brightness_set(brightness_percent)

    try:
        root.withdraw()
    except Exception:
        pass

    _beep(root, ms=beep_ms)

    try:
        _open_video(video_path)
    except Exception:
        pass

    overlay = tk.Toplevel(root)
    overlay.configure(bg="black")
    overlay.attributes("-fullscreen", True)
    overlay.attributes("-topmost", True)

    try:
        overlay.attributes("-alpha", 0.1)
    except Exception:
        pass

    overlay.protocol("WM_DELETE_WINDOW", lambda: None)

    try:
        overlay.grab_set()
    except Exception:
        pass

    overlay.bind("<Key>", lambda e: "break")
    overlay.bind("<Button>", lambda e: "break")

    start = time.monotonic()

    def tick():
        if (time.monotonic() - start) >= seconds:
            try:
                overlay.grab_release()
            except Exception:
                pass
            try:
                overlay.destroy()
            except Exception:
                pass
            root.destroy()
            return

        overlay.after(100, tick)

    tick()
