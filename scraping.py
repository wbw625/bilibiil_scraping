# scraping.py
# This is for scraping data from one Bilibili video.

import requests
from bs4 import BeautifulSoup

def scrape_bilibili_video(video_id):
    """
    Scrape video title and description from a Bilibili video page.

    Args:
        video_id (str): The BVID of the Bilibili video.

    Returns:
        dict: A dictionary containing data of the video.
    """

    url = f'https://api.bilibili.com/x/web-interface/view?bvid={video_id}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Host': 'api.bilibili.com',
        'Referer': f'https://www.bilibili.com/video/{video_id}/'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")

    data = response.json().get('data', {})

    # Extracting video information
    title = data.get('title', '')
    description = data.get('desc', '')
    ptime = data.get('pubdate', 0)
    danmaku = data.get('stat', {}).get('danmaku', 0)
    likes = data.get('stat', {}).get('like', 0)
    coins = data.get('stat', {}).get('coin', 0)
    favorites = data.get('stat', {}).get('favorite', 0)
    shares = data.get('stat', {}).get('share', 0)
    views = data.get('stat', {}).get('view', 0)

    # 获取 up 主粉丝数
    author_followers = None
    owner = data.get('owner', {})
    mid = owner.get('mid')
    if mid:
        follow_url = f'https://api.bilibili.com/x/relation/stat?vmid={mid}'
        follow_resp = requests.get(follow_url, headers=headers)
        if follow_resp.status_code == 200:
            follow_data = follow_resp.json().get('data', {})
            author_followers = follow_data.get('follower', None)

    return {
        'title': title,
        'description': description,
        'ptime': ptime,
        'danmaku': danmaku,
        'likes': likes,
        'coins': coins,
        'favorites': favorites,
        'shares': shares,
        'author_followers': author_followers,
        'views': views
    }


# Example usage:
if __name__ == "__main__":
    video_id = 'BV155j2z7Etd'
    video_data = scrape_bilibili_video(video_id)
    print(video_data)