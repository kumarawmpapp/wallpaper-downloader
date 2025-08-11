import logging
import sys
import json
import importlib
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load configurations
config_path = Path(__file__).parent / "config.json"
config = json.loads(config_path.read_text(encoding="utf-8"))

keys_path = Path(__file__).parent / "keys.env"
load_dotenv(keys_path)


# Dynamic platform detection
def get_platform_module():
    platform_map = {"win32": "windows", "darwin": "macos", "linux": "linux"}
    platform_key = sys.platform
    module_name = platform_map.get(platform_key, "none")

    try:
        return importlib.import_module(f"platforms.{module_name}")
    except ImportError:
        raise ImportError(f"Platform {module_name} not supported")


def get_image_urls(source, query, count):
    try:
        source_module = importlib.import_module(f"sources.{source}")
        source_config = config.get("source_configs", {}).get(source, {})
        return source_module.get_image_urls(query, count, source_config)
    except ImportError:
        print(f"Source {source} not implemented")
        return []


def cleanup_wallpapers(wallpaper_dir, keep_count):
    """Keep only the most recent N wallpapers"""
    import os

    try:
        # Get all wallpaper files sorted by modification time (newest first)
        files = sorted(
            Path(wallpaper_dir).glob("*.jpg"), key=os.path.getmtime, reverse=False
        )

        # Delete older files beyond retention count
        for old_file in files[keep_count:]:
            old_file.unlink()
            print(f"Removed old wallpaper: {old_file.name}")

    except Exception as e:
        print(f"Cleanup failed: {e}")


def main():
    import time

    this_platform = get_platform_module()
    # Parse CLI args
    args = sys.argv[1:]
    cli_source = args[0] if len(args) > 0 else None
    cli_query = args[1] if len(args) > 1 else config["query"]

    # Determine sources to try
    sources = config["sources"].copy()
    if cli_source:
        sources.insert(0, cli_source)

    # Get monitor count
    monitor_count = config.get("monitor_count") or this_platform.get_monitor_count()
    try:
        monitor_count = (
            this_platform.get_monitor_count() or config.get("monitor_count") or 1
        )
        logging.debug(f"Detected {monitor_count} monitor(s)")
    except Exception as e:
        logging.error(f"Monitor detection failed: {e}")
        monitor_count = 1

    # Prepare wallpaper directory
    wallpaper_dir = Path(this_platform.DEFAULT_CONFIG["wallpaper_dir"]).expanduser()
    wallpaper_dir.mkdir(parents=True, exist_ok=True)

    wallpapers = []

    for source in sources:
        try:
            # Get URLs for all monitors at once
            urls = get_image_urls(source, cli_query, monitor_count)
            if not urls:
                continue

            # Download all images for this source
            downloaded = []
            for i, url in enumerate(urls[:monitor_count]):
                try:
                    img_path = wallpaper_dir / f"{source}_{i+1}.jpg"
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()  # Raise HTTP errors
                    img_path.write_bytes(response.content)
                    downloaded.append(img_path)
                    logging.info(f"Downloaded {url} to {img_path}")
                except Exception as e:
                    logging.error(f"Failed to download {url}: {e}")
                    break  # Skip this source if any download fails

            if len(downloaded) == monitor_count:
                wallpapers = downloaded  # Use this source's images
                break  # Exit source loop after first successful download set

        except Exception as e:
            logging.error(f"Source {source} failed completely: {e}")

    # 2. Set wallpapers if we got enough images
    if len(wallpapers) >= monitor_count:
        for i in range(monitor_count):
            try:
                # Add 1 to make monitor IDs 1-based
                this_platform.set_wallpaper(str(wallpapers[i]), i + 1)
                logging.info(f"Set wallpaper for monitor {i+1}: {wallpapers[i].name}")
                time.sleep(0.5)  # Brief pause between monitor updates
            except Exception as e:
                logging.error(f"Failed to set monitor {i+1}: {e}")
    else:
        logging.error("Insufficient wallpapers downloaded")

    cleanup_wallpapers(wallpaper_dir, config.get("wallpaper_retention_count"))


if __name__ == "__main__":
    main()
