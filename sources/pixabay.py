import os
import requests
from urllib.parse import urlencode
from pathlib import Path
import logging
from typing import List


CONFIG = {
    "endpoint": "https://pixabay.com/api",
    "params": {
        "image_type": "photo",
        "orientation": "horizontal",
        "category": "backgrounds, nature, places, animals",
        "min_width": 1920,
        "min_height": 1080,
        "editors_choice": "true",
        "safesearch": "true",
        "order": "latest"
      }
}


def get_image_urls(query, count, config_override=None):
    from deepmerge import always_merger
    config = always_merger.merge(CONFIG, (config_override or {}))
    try:
        # Prepare API parameters
        params = {
            **config['params'],
            'q': query,
            'per_page': max(count, 3),  # Ensure at least 3 images, pixabay requirement
            'key': os.getenv('PIXABAY_API_KEY')
        }
        
        response = requests.get(
            config['endpoint'],
            params=params,
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Extract high-quality image URLs
        return [hit['largeImageURL'] for hit in data.get('hits', [])[:count]]
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Pixabay API request failed: {e}")
        return []
    except (KeyError, ValueError) as e:
        logging.error(f"Failed to parse Pixabay response: {e}")
        return []

def download_image(url: str, save_path: Path) -> bool:
    """Download individual image from Pixabay"""
    try:
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    except Exception as e:
        logging.error(f"Failed to download {url}: {e}")
        return False