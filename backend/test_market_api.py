import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DATA_GOV_API_KEY")

url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

params = {
    "api-key": api_key,
    "format": "json",
    "limit": 1
}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

print("Testing data.gov.in from Python...")
print("API key loaded:", bool(api_key))

try:

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=(10, 60)
    )

    print("Status:", response.status_code)

    print("Response:")
    print(response.text)

except requests.exceptions.Timeout:

    print("❌ Request timed out.")

except requests.exceptions.RequestException as e:

    print("❌ Request failed:")
    print(e)