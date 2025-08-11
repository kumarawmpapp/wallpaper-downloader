import subprocess
import json


def get_monitor_info():
    try:
        output = subprocess.check_output(["xrandr", "--listmonitors"]).decode()
        return int(output.split("\n")[0].split(":")[1].strip())
    except:
        return 1


def set_wallpaper(filepath, monitor_id=None):
    subprocess.run(
        [
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-uri",
            f"file://{filepath}",
        ]
    )


DEFAULT_CONFIG = {
    "default_source": "unsplash",
    "wallpaper_dir": "~/.local/share/wallpaper_changer",
}
