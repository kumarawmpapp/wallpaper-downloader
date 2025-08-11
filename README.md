# Wallpaper Downloader

A Python script to download wallpapers from various APIs (Unsplash, Pexels, Pixabay, Bing).

## Setup Instructions

### 1. Environment Variables

Create a `keys.env` file in the project root with the following API keys:

```ini
# API Keys for wallpaper services
UNSPLASH_API_KEY="your_unsplash_access_key_here"
PEXELS_API_KEY="your_pexels_api_key_here"
PIXABAY_API_KEY="your_pixabay_api_key_here"

# Optional: Bing doesn't typically require an API key
# BING_API_KEY="optional_bing_key_if_using_api"
```

### 2. Obtaining API Keys

Unsplash:
- Sign up at [Unsplash Developers](https://unsplash.com/developers)
- Create a new application to get your access key

Pexels:
- Register at [Pexels API](https://www.pexels.com/api)
- Get your API key from the dashboard

Pixabay:
- Get a key from [Pixabay API](https://pixabay.com/api/docs/)


### 3. Installation

```bash
# Clone the repository
git clone https://github.com/kumarawmpapp/wallpaper-downloader.git
cd wallpaper-downloader

# Install dependencies
pip install -r requirements.txt
```

### 4. Usage

Run individual services:
```bash
python main.py unsplash
python main.py pexels
python main.py pixabay
python main.py bing
```

Or run all services via batch file (Windows):
```bash
run.bat
```

## Configuration Options

You can modify these variables in config.json:
```ini
{
  "monitor_count": 2,
  "wallpaper_retention_count": 8,
  "query": "nature,landscape",
  "sources": ["pixabay", "pexels", "unsplash", "bing"],
  "source_configs": {
    "unsplash": {
      
    },
    "bing": {
      
    },
    "pexels": {
     
    },
    "pixabay": {
      
    }
  }
}
```

## Troubleshooting

If you get "API key not found" errors:
- Verify your keys.env file exists in the project root
- Check for typos in variable names
- Ensure keys are properly quoted
- Restart your terminal/IDE after adding keys

## License

This project is licensed under MIT License - see [LICENSE](./LICENSE) file for details.