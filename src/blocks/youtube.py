import os

import requests
from dotenv import load_dotenv


def process_youtube(channel_id: str, max_videos: int = 5):
    """
    Fetch the latest videos from a YouTube channel using the YouTube Data API.

    :param channel_id: YouTube Channel ID
    :param max_videos: Number of videos to fetch
    :return: List of (title, link) tuples
    """
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")  # Fetch API key from environment

    if not api_key:
        print("❌ Error: YOUTUBE_API_KEY is not set.")
        return []

    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={api_key}"
        f"&order=date"
        f"&channelId={channel_id}"
        f"&part=snippet"
        f"&type=video"
        f"&maxResults={max_videos}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        items = response.json().get("items", [])

        video_links = []
        for item in items:
            title = item["snippet"]["title"]
            link = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            video_links.append({"title": title, "link": link})

        return video_links

    except requests.RequestException as e:
        print(f"❌ Error fetching YouTube videos: {e}")
        return []
