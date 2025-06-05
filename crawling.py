# scraping.py
# This is for crawling data from multiple Bilibili videos.

from scraping import scrape_bilibili_video
import json
import requests
import re
import time
import urllib.parse

# get video IDs list
def get_video_ids(search_name, pages):
    """
    Get a list of Bilibili video IDs based on search name and number of pages.
    Args:
        search_name (str): The name to search for videos.
        pages (int): The number of pages to scrape.
    Returns:
        list: A list of BVIDs (Bilibili video IDs).
    """

    bvid_lst = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        # 'Host': 'api.bilibili.com',
        # 'Referer': f'https://www.bilibili.com'
    }
    for page in range(1, pages):
        print(f'正在获取第{page}页的视频ID')
        url = (
            'https://api.bilibili.com/x/web-interface/search/type'
            f'?search_type=video&keyword={urllib.parse.quote(search_name)}&page={page}'
        )
        req = requests.get(url, headers=headers)
        if req.status_code != 200:
            print(f"Error fetching page {page}: {req.status_code}")
            continue
        data = req.json()
        if data['code'] != 0:
            print(f"API error on page {page}: {data['message']}")
            continue
        result = data['data']['result']
        lst_add = [item['bvid'] for item in result if 'bvid' in item]
        print(f'第{page}页', lst_add)
        bvid_lst.extend(lst_add)
        time.sleep(10)
    return bvid_lst


def main():
    """
    Main function to scrape multiple Bilibili videos.
    """
    search_name = 'Python爬虫'
    pages = 5  # Number of pages to scrape
    video_ids = get_video_ids(search_name, pages)
    print(f"Found {len(video_ids)} videos to scrape.")
    all_videos_data = []

    for video_id in video_ids:
        try:
            video_data = scrape_bilibili_video(video_id)
            all_videos_data.append(video_data)
        except Exception as e:
            print(f"Error scraping video {video_id}: {e}")

    # Save all data to a json file
    with open(f'{search_name}_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_videos_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()