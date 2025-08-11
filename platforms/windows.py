import os
import ctypes
import win32api
import win32con
import win32gui
from pathlib import Path

def get_monitor_count():
    """Get number of connected monitors"""
    import logging
    count = len(win32api.EnumDisplayMonitors())
    logging.debug(f"Monitors detected: {count}")
    return count

def set_wallpaper(image_path, monitor_id=None):
    """
    Set wallpaper for specific monitor (Windows 8.1 compatible)
    Args:
        image_path: Path to image file
        monitor_id: Monitor number (1-based index)
    """
    return # do not execute this method since desktop wallpaper slideshow theme will refresh images
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    abs_path = str(Path(image_path).absolute())
    
    if monitor_id is None or monitor_id == 1:
        # Primary monitor or all monitors
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER,
            abs_path,
            win32con.SPIF_SENDCHANGE
        )

    # Windows 8.1 requires registry tweaks for multi-monitor
    if monitor_id is not None:
        set_multi_monitor_wallpaper(abs_path, monitor_id)

def set_multi_monitor_wallpaper(image_path, monitor_id):
    """Windows 8.1 multi-monitor workaround"""
    try:
        import winreg
        # Open registry key
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Control Panel\Desktop",
            0,
            winreg.KEY_WRITE
        )
        
        # Set wallpaper style (10 = Fill, 6 = Fit, 2 = Stretch)
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        
        # Set monitor-specific wallpaper
        value_name = "Wallpaper" if monitor_id == 1 else f"Wallpaper{monitor_id}"
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, image_path)
        
        # Refresh
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER,
            image_path,
            win32con.SPIF_SENDCHANGE
        )
    except Exception as e:
        print(f"Multi-monitor setting failed: {e}")
    finally:
        if 'key' in locals():
            winreg.CloseKey(key)


def debug_monitors():
    """Display monitor info during debugging"""
    from win32api import EnumDisplayMonitors, GetMonitorInfo
    print("\n[DEBUG] Monitor Configuration:")
    for i, monitor in enumerate(EnumDisplayMonitors(), 1):
        info = GetMonitorInfo(monitor[0])
        print(f"Monitor {i}: {info['Device']} @ {info['Work']}")


def debug_registry():
    """Check current wallpaper registry values"""
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop") as key:
        for i in range(10):
            try:
                name, value, _ = winreg.EnumValue(key, i)
                if "Wallpaper" in name:
                    print(f"{name}: {value}")
            except OSError:
                break


DEFAULT_CONFIG = {
    "default_source": "bing",
    "wallpaper_dir": str(Path(os.environ["USERPROFILE"]) / "Pictures" / "wallpapers")
}