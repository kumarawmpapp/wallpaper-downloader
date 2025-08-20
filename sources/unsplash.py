import requests
import jmespath
import os

CONFIG = {
    "endpoint": "https://api.unsplash.com/photos/random",
    "params": {"query": "{query}", "count": "{count}", "orientation": "landscape", "content_filter": "high", "topics": "bo8jQKTaE0Y,6sMVjTLSkeQ,M8jVbLbTRws,tthdwfNPCcw,"},
    "response_map": "[].urls.full",
}


def get_image_urls(query, count, config_override=None):
    from deepmerge import always_merger
    config = always_merger.merge(CONFIG, (config_override or {}))
    # config = {**CONFIG, **(config_override or {})}
    params = {
        k: v.format(query=query, count=count) for k, v in config["params"].items()
    }
    params["client_id"] = os.getenv('UNSPLASH_API_KEY')

    response = requests.get(config["endpoint"], params=params).json()
    return jmespath.search(config["response_map"], response)


# https://api.unsplash.com/topics?per_page=100&order_by=featured&client_id=MBR8UbWLuZqGsSqvSlMmepScIXql7DMQvhuv2J8o6Io