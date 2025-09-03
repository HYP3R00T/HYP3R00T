import xml.etree.ElementTree as ET

import requests


# Function to fetch latest blog posts from RSS feed
def process_blog(rss_url: str, max_posts: int = 5) -> list:
    """
    Fetch the latest blog posts from the provided RSS feed URL.

    Args:
        rss_url (str): The URL of the RSS/Atom feed.
        max_posts (int): The maximum number of posts to fetch (default is 5).

    Returns:
        list: A list of dictionaries with each dictionary containing:
              - title: The blog post title.
              - link: The URL to the blog post.
    """
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.0 Safari/537.36",
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "Accept-Language": "en-US,en;q=0.9",
                  "Referer": "https://hyperoot.substack.com/"
   }
    try:
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return []

    try:
        root = ET.fromstring(response.content)
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return []

    channel = root.find("channel")
    if channel is None:
        print("Error: No channel element found in the RSS feed")
        return []

    posts = []
    for item in channel.findall("item")[:max_posts]:
        title = item.findtext("title", "No Title")
        link = item.findtext("link", "#")
        posts.append({"title": title, "link": link})
    return posts