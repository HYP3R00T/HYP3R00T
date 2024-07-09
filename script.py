import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os
from jinja2 import Template

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")


# Function to fetch latest blog posts from RSS feed
def fetch_latest_blog_posts():
    rss_feed_url = "https://hyperoot.dev/rss.xml"
    response = requests.get(rss_feed_url)
    root = ET.fromstring(response.content)
    items = root.find("channel").findall("item")
    post_links = []
    for item in items[:3]:
        title = item.find("title").text
        link = item.find("link").text
        post_links.append((title, link))
    return post_links


# Function to fetch latest YouTube videos
def fetch_latest_youtube_videos(api_key, channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&order=date&part=snippet&type=video&maxResults=3"
    response = requests.get(url)
    items = response.json().get("items", [])
    video_links = []
    for item in items:
        title = item["snippet"]["title"]
        link = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        video_links.append((title, link))
    return video_links


def main():
    latest_blog_posts = fetch_latest_blog_posts()
    latest_videos = fetch_latest_youtube_videos(YOUTUBE_API_KEY, CHANNEL_ID)

    # Load Jinja2 template
    with open("README_template.md") as template_file:
        template = Template(template_file.read())

    # Render the README content
    readme_content = template.render(videos=latest_videos, blogs=latest_blog_posts)

    # Write the README content to README.md
    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)


if __name__ == "__main__":
    main()
