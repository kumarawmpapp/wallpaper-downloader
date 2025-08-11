import requests
import jmespath

CONFIG = {
    "endpoint": "https://www.bing.com/HPImageArchive.aspx",
    "params": {"format": "js", "idx": "0", "n": "{count}", "mkt": "en-US"},
    "response_map": "images[].url",
    "base_url": "https://www.bing.com",
}


def get_image_urls(query, count, config_override=None):
    config = {**CONFIG, **(config_override or {})}
    params = {k: v.format(count=count) for k, v in config["params"].items()}

    response = requests.get(config["endpoint"], params=params).json()
    urls = jmespath.search(config["response_map"], response)
    return [config["base_url"] + url for url in urls]
