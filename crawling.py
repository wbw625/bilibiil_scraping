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
        'cookie' : r"buvid4=2048BC2C-D43E-E27A-10F8-D07A2E1CE49444643-024011402-UFC7YtxT%2Bx4AuetofCOgEg%3D%3D; is-2022-channel=1; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_BLACKGAP=0; DedeUserID=1683525074; DedeUserID__ckMd5=002e084d4aaa1ae9; buvid3=EDD3F1BF-5CE8-35C6-722F-D7A2FDD5718185396infoc; b_nut=1736736885; _uuid=710AE8A10C-3259-CC7C-B2A5-106A2E8CF8DC802512infoc; hit-dyn-v2=1; rpdid=|(JJmY)YRu~m0J'u~Jm~)l|ll; LIVE_BUVID=AUTO4217410661369507; buvid_fp=b0394cd9ce338cde1a2637ebb827f2c7; enable_feed_channel=ENABLE; CURRENT_QUALITY=80; home_feed_column=5; fingerprint=c330d8e9ea37dd963bb3c7dce0fa84ab; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDkyODY0MDAsImlhdCI6MTc0OTAyNzE0MCwicGx0IjotMX0.C__60Mw4KR-oxmAgYtaFNiH2eKPhIC0vG494V1H5Mgk; bili_ticket_expires=1749286340; SESSDATA=07d69450%2C1764640057%2C15386%2A62CjC-O2ghoasb974P5UKmaOfRdPysBoFPdono7EDSv_G8Sk-cQVn1_qbWCZgXVY_v0RcSVjVYUlotMTI2MmdYRUhvYnRnSm1pRkNQemtlVTRycW1XTkJKc1VLOW5PSnVaQXN2VFFMdG9aaU9Wb1VYUGZha3JxX1dBYWZuZHBYcEVMaHo1dmZuM2tRIIEC; bili_jct=296a796bd3f42923db1fd6daf3539dea; sid=6omyaf5x; browser_resolution=1552-852; bsource=search_bing; b_lsid=E8B6B1E8_1974019322C; bp_t_offset_1683525074=1074992716045090816; PVID=16; CURRENT_FNVAL=4048"
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


def get_homepage_bvids(ps=10):
    """
    获取B站首页推荐视频的BV号列表
    Args:
        ps (int): 获取的视频数量，最大20
    Returns:
        list: BV号列表
    """
    url = f'https://api.bilibili.com/x/web-interface/index/top/rcmd?fresh_type=3&ps={ps}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        # 'Host': 'api.bilibili.com',
        # 'Referer': f'https://www.bilibili.com/'
        'cookie' : r"buvid4=2048BC2C-D43E-E27A-10F8-D07A2E1CE49444643-024011402-UFC7YtxT%2Bx4AuetofCOgEg%3D%3D; is-2022-channel=1; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_BLACKGAP=0; DedeUserID=1683525074; DedeUserID__ckMd5=002e084d4aaa1ae9; buvid3=EDD3F1BF-5CE8-35C6-722F-D7A2FDD5718185396infoc; b_nut=1736736885; _uuid=710AE8A10C-3259-CC7C-B2A5-106A2E8CF8DC802512infoc; hit-dyn-v2=1; rpdid=|(JJmY)YRu~m0J'u~Jm~)l|ll; LIVE_BUVID=AUTO4217410661369507; buvid_fp=b0394cd9ce338cde1a2637ebb827f2c7; enable_feed_channel=ENABLE; CURRENT_QUALITY=80; home_feed_column=5; fingerprint=c330d8e9ea37dd963bb3c7dce0fa84ab; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDkyODY0MDAsImlhdCI6MTc0OTAyNzE0MCwicGx0IjotMX0.C__60Mw4KR-oxmAgYtaFNiH2eKPhIC0vG494V1H5Mgk; bili_ticket_expires=1749286340; SESSDATA=07d69450%2C1764640057%2C15386%2A62CjC-O2ghoasb974P5UKmaOfRdPysBoFPdono7EDSv_G8Sk-cQVn1_qbWCZgXVY_v0RcSVjVYUlotMTI2MmdYRUhvYnRnSm1pRkNQemtlVTRycW1XTkJKc1VLOW5PSnVaQXN2VFFMdG9aaU9Wb1VYUGZha3JxX1dBYWZuZHBYcEVMaHo1dmZuM2tRIIEC; bili_jct=296a796bd3f42923db1fd6daf3539dea; sid=6omyaf5x; browser_resolution=1552-852; bsource=search_bing; b_lsid=E8B6B1E8_1974019322C; bp_t_offset_1683525074=1074992716045090816; PVID=16; CURRENT_FNVAL=4048"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"请求失败: {resp.status_code}")
        return []
    data = resp.json()
    if data['code'] != 0:
        print(f"API错误: {data['message']}")
        return []
    bvids = [item['bvid'] for item in data['data']['item'] if 'bvid' in item]
    return bvids


def get_popular_video_ids(num_pages=5):
    """
    获取B站热门视频的BV号列表
    Args:
        num_pages (int): 获取的页数
    Returns:
        list: BV号列表
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        # 'Host': 'api.bilibili.com',
        # 'Referer': f'https://www.bilibili.com/'
        'cookie' : r"buvid4=2048BC2C-D43E-E27A-10F8-D07A2E1CE49444643-024011402-UFC7YtxT%2Bx4AuetofCOgEg%3D%3D; is-2022-channel=1; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_BLACKGAP=0; DedeUserID=1683525074; DedeUserID__ckMd5=002e084d4aaa1ae9; buvid3=EDD3F1BF-5CE8-35C6-722F-D7A2FDD5718185396infoc; b_nut=1736736885; _uuid=710AE8A10C-3259-CC7C-B2A5-106A2E8CF8DC802512infoc; hit-dyn-v2=1; rpdid=|(JJmY)YRu~m0J'u~Jm~)l|ll; LIVE_BUVID=AUTO4217410661369507; buvid_fp=b0394cd9ce338cde1a2637ebb827f2c7; enable_feed_channel=ENABLE; CURRENT_QUALITY=80; fingerprint=c330d8e9ea37dd963bb3c7dce0fa84ab; home_feed_column=5; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDk4MDQ3OTMsImlhdCI6MTc0OTU0NTUzMywicGx0IjotMX0.ojtbN-Q1m8NDsJqTcLkvyoYELL4MDA7B48fEnibaKJs; bili_ticket_expires=1749804733; browser_resolution=1552-852; PVID=2; b_lsid=61028EA77_197641F6789; SESSDATA=c167da32%2C1765283709%2C329d6%2A62CjCZ-6JqGUjgnIqK41z1zWSmVkNOnGdWrXOOsqqYw-Usdr9s3dkKoGB3lQK9MrCXXYASVklOR1JOQXpid0NsQU9ERTBBR1FnMVhRTnhYQnl3MHVySU1YUkpBa0VyWk80OFVBYkQyNWVBS1VNLUFqR0xmVExBWTJBTEw2Wm5MbEw1Sk1JT0VwMWt3IIEC; bili_jct=bbd9c70b16405af7577311846299ee79; sid=5dfe9mk9; bsource=search_bing; CURRENT_FNVAL=2000; bp_t_offset_1683525074=1077592180576485376"
    }
    video_ids = []
    start_page = 300
    for page in range(start_page, num_pages + start_page):
        url = f'https://api.bilibili.com/x/web-interface/popular/series/one?number={page}'
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"请求失败: {resp.status_code}")
            continue
        data = resp.json()
        if data['code'] != 0:
            print(f"API错误: {data['message']}")
            continue
        # 提取每个视频的bvid
        bvids = [item['bvid'] for item in data['data']['list'] if 'bvid' in item]
        print(f"第{page}期热门视频BV号：", bvids)
        video_ids.extend(bvids)
        time.sleep(10)
    return video_ids

def main():
    """
    Main function to scrape multiple Bilibili videos.
    """

    # Search for videos by name
    # search_name = '大东彦'
    # prefix = '【大东彦】'
    # pages = 20  # Number of pages to scrape
    # video_ids = get_video_ids(search_name, pages)

    # Recommended videos from Bilibili homepage
    # num_pages = 5
    # search_name = 'B站首页推荐'
    # num_bvids = 10
    # video_ids = []
    # for _ in range(num_pages):
    #     print(f"Fetching video IDs from page {_ + 1} of {num_pages}...")
    #     video_ids.extend(get_homepage_bvids(ps=num_bvids))
    #     time.sleep(10)

    # Popular videos from Bilibili homepage
    search_name = 'B站热门视频'
    prefix = ''
    num_pages = 5
    video_ids = []
    video_ids.extend(get_popular_video_ids(num_pages))
    time.sleep(10)


    print(f"Found {len(video_ids)} videos to scrape.")
    all_videos_data = []

    for video_id in video_ids:
        try:
            time.sleep(1)
            video_data = scrape_bilibili_video(video_id, prefix)
            if video_data is None:
                print(f"Video {video_id} does not match criteria, skipping.")
                continue
            all_videos_data.append(video_data)
        except Exception as e:
            print(f"Error scraping video {video_id}: {e}")

    # Save all data to a json file
    with open(f'{search_name}_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_videos_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()