import requests
import jmespath
import os

CONFIG = {
    "endpoint": "https://api.pexels.com/v1/search",
    "params": {"query": "{query}", "per_page": "{count}", "orientation": "landscape", "size": "medium"},
    "headers": {"Authorization": "{api_key}"},
    "response_map": "photos[].src.original",
}


def get_image_urls(query, count, config_override=None):
    from deepmerge import always_merger
    config = always_merger.merge(CONFIG, (config_override or {}))
    params = {
        k: v.format(query=query, count=count) for k, v in config["params"].items()
    }
    headers = {
        k: v.format(api_key=os.getenv('PEXELS_API_KEY')) for k, v in config["headers"].items()
    }

    response = requests.get(config["endpoint"], params=params, headers=headers).json()
    return jmespath.search(config["response_map"], response)
