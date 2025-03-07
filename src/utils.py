import xml.etree.ElementTree as ET

import requests


# Function to fetch latest blog posts from RSS feed
def get_latest_blog_posts(feed_url: str, max_posts: int = 5) -> list:
    """
    Fetch the latest blog posts from the provided RSS feed URL.

    Args:
        feed_url (str): The URL of the RSS/Atom feed.
        max_posts (int): The maximum number of posts to fetch (default is 5).

    Returns:
        list: A list of dictionaries with each dictionary containing:
              - title: The blog post title.
              - link: The URL to the blog post.
    """
    try:
        response = requests.get(feed_url)
        response.raise_for_status()  # Raise an error for bad status codes
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

    items = channel.findall("item")
    posts = []
    for item in items[:max_posts]:
        title_elem = item.find("title")
        link_elem = item.find("link")
        title = title_elem.text if title_elem is not None else "No Title"
        link = link_elem.text if link_elem is not None else "#"
        posts.append({"title": title, "link": link})
    return posts
