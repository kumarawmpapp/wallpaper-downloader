import subprocess
from pathlib import Path
import json


# Monitor info
def get_monitor_count():
    try:
        cmd = "system_profiler SPDisplaysDataType | grep Resolution"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return len(result.stdout.strip().split("\n"))
    except:
        return 1


def set_wallpaper(filepath: str | Path, monitor_id: int | None = None) -> None:
    """
    Set wallpaper on macOS (supports multiple monitors)

    Args:
        filepath: Path to the image file
        monitor_id: Desktop number (1-based index). None = all monitors.
    """

    return  # do not execute this method since desktop wallpaper   will refresh images

    # Convert Path object to string if needed
    abs_path = str(Path(filepath).absolute())

    # Verify file exists
    if not Path(abs_path).exists():
        raise FileNotFoundError(f"Wallpaper image not found: {abs_path}")

    # AppleScript for single monitor
    if monitor_id is not None:
        script = f"""
        tell application "System Events"
            set picture of desktop {monitor_id} to "{abs_path}"
        end tell
        """
    # AppleScript for all monitors
    else:
        script = f"""
        tell application "System Events"
            set theDesktops to every desktop
            repeat with theDesktop in theDesktops
                set picture of theDesktop to "{abs_path}"
            end repeat
        end tell
        """

    # Execute with error handling
    try:
        subprocess.run(
            ["osascript", "-e", script], check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to set wallpaper:\n" f"Error: {e.stderr}\n" f"Script: {script}"
        ) from e


# Config defaults
DEFAULT_CONFIG = {
    "default_source": "unsplash",
    "wallpaper_dir": "~/Pictures/wallpaper_changer",
}
