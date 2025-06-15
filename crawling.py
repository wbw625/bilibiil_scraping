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
        'cookie' : r"buvid3=E3CB765A-FE67-1247-F41C-E5018C120CC929624infoc; b_nut=1749887529; _uuid=F5E1B1013-C87C-D9510-537A-6B5CC6E14610128418infoc; enable_web_push=DISABLE; enable_feed_channel=ENABLE; buvid4=C963FF0F-F4EC-1E1E-4747-E2D2E99CD2C430487-025061415-YU%2B9YZAoJVPN4WCDFW3keA%3D%3D; buvid_fp=c330d8e9ea37dd963bb3c7dce0fa84ab; SESSDATA=b031cd0b%2C1765439558%2C62b83%2A62CjC0Wpv-3G4gDXW-sUfRDC3hMOYN3skYEN8BjwwEfeZxg19Ry63r9i89xbZqClBPSVgSVmIxeG1XRFYwRTZVMGZGLVY3clQzVm1vNnBvVzk1em16dHUtR0diSkx5WW00ZTBHWmRvSVFFUGNpN3k5YkJQWGV2MEoxbUU3THllUkx2QWtkV3pwblhnIIEC; bili_jct=b1de9fec08368e3e7b24e66b19a651b1; DedeUserID=1683525074; DedeUserID__ckMd5=002e084d4aaa1ae9; theme-tip-show=SHOWED; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1552-852; rpdid=|(JJmY)YRu~m0J'u~Rm)m~JYR; hit-dyn-v2=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTAxNjE4NTAsImlhdCI6MTc0OTkwMjU5MCwicGx0IjotMX0.fn-YN5Fr8RIrrJ5AcsYYxnKP_dnSfhVCFwOfJw1NwrA; bili_ticket_expires=1750161790; CURRENT_QUALITY=80; sid=817imscu; CURRENT_FNVAL=4048; b_lsid=4A175957_197735E192B; PVID=5; bp_t_offset_1683525074=1078679503087075328"
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
        time.sleep(5)
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
        'cookie' : r"buvid3=E3CB765A-FE67-1247-F41C-E5018C120CC929624infoc; b_nut=1749887529; _uuid=F5E1B1013-C87C-D9510-537A-6B5CC6E14610128418infoc; enable_web_push=DISABLE; enable_feed_channel=ENABLE; buvid4=C963FF0F-F4EC-1E1E-4747-E2D2E99CD2C430487-025061415-YU%2B9YZAoJVPN4WCDFW3keA%3D%3D; buvid_fp=c330d8e9ea37dd963bb3c7dce0fa84ab; SESSDATA=b031cd0b%2C1765439558%2C62b83%2A62CjC0Wpv-3G4gDXW-sUfRDC3hMOYN3skYEN8BjwwEfeZxg19Ry63r9i89xbZqClBPSVgSVmIxeG1XRFYwRTZVMGZGLVY3clQzVm1vNnBvVzk1em16dHUtR0diSkx5WW00ZTBHWmRvSVFFUGNpN3k5YkJQWGV2MEoxbUU3THllUkx2QWtkV3pwblhnIIEC; bili_jct=b1de9fec08368e3e7b24e66b19a651b1; DedeUserID=1683525074; DedeUserID__ckMd5=002e084d4aaa1ae9; theme-tip-show=SHOWED; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1552-852; rpdid=|(JJmY)YRu~m0J'u~Rm)m~JYR; hit-dyn-v2=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTAxNjE4NTAsImlhdCI6MTc0OTkwMjU5MCwicGx0IjotMX0.fn-YN5Fr8RIrrJ5AcsYYxnKP_dnSfhVCFwOfJw1NwrA; bili_ticket_expires=1750161790; CURRENT_QUALITY=80; sid=817imscu; CURRENT_FNVAL=4048; b_lsid=4A175957_197735E192B; PVID=5; bp_t_offset_1683525074=1078679503087075328"
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
        'cookie' : r"buvid3=E3CB765A-FE67-1247-F41C-E5018C120CC929624infoc; b_nut=1749887529; _uuid=F5E1B1013-C87C-D9510-537A-6B5CC6E14610128418infoc; enable_web_push=DISABLE; enable_feed_channel=ENABLE; buvid4=C963FF0F-F4EC-1E1E-4747-E2D2E99CD2C430487-025061415-YU%2B9YZAoJVPN4WCDFW3keA%3D%3D; buvid_fp=c330d8e9ea37dd963bb3c7dce0fa84ab; SESSDATA=b031cd0b%2C1765439558%2C62b83%2A62CjC0Wpv-3G4gDXW-sUfRDC3hMOYN3skYEN8BjwwEfeZxg19Ry63r9i89xbZqClBPSVgSVmIxeG1XRFYwRTZVMGZGLVY3clQzVm1vNnBvVzk1em16dHUtR0diSkx5WW00ZTBHWmRvSVFFUGNpN3k5YkJQWGV2MEoxbUU3THllUkx2QWtkV3pwblhnIIEC; bili_jct=b1de9fec08368e3e7b24e66b19a651b1; DedeUserID=1683525074; DedeUserID__ckMd5=002e084d4aaa1ae9; theme-tip-show=SHOWED; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1552-852; rpdid=|(JJmY)YRu~m0J'u~Rm)m~JYR; hit-dyn-v2=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTAxNjE4NTAsImlhdCI6MTc0OTkwMjU5MCwicGx0IjotMX0.fn-YN5Fr8RIrrJ5AcsYYxnKP_dnSfhVCFwOfJw1NwrA; bili_ticket_expires=1750161790; CURRENT_QUALITY=80; sid=817imscu; CURRENT_FNVAL=4048; b_lsid=4A175957_197735E192B; PVID=5; bp_t_offset_1683525074=1078679503087075328"
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
    # pages = 32  # Number of pages to scrape
    # video_ids = get_video_ids(search_name, pages)

    # Recommended videos from Bilibili homepage
    num_pages = 60
    search_name = 'B站首页推荐'
    prefix = ''
    num_bvids = 10
    video_ids = []
    for _ in range(num_pages):
        print(f"Fetching video IDs from page {_ + 1} of {num_pages}...")
        # 如果重复，跳过
        new_video_ids = get_homepage_bvids(ps=num_bvids)
        for video_id in new_video_ids:
            if video_id not in video_ids:
                video_ids.append(video_id)
                print(f"Added new video ID: {video_id}")
        print(f"Fetched {len(new_video_ids)} new video IDs.")
        time.sleep(5)

    # Popular videos from Bilibili homepage
    # search_name = 'B站每周必看'
    # prefix = ''
    # num_pages = 20
    # video_ids = []
    # video_ids.extend(get_popular_video_ids(num_pages))
    # time.sleep(5)


    print(f"Found {len(video_ids)} videos to scrape.")
    all_videos_data = []

    for video_id in video_ids:
        try:
            time.sleep(0.5)
            video_data = scrape_bilibili_video(video_id, prefix)
            if video_data is None:
                print(f"Video {video_id} does not match criteria, skipping.")
                continue
            if video_data in all_videos_data:
                print(f"Video {video_id} is a duplicate, skipping.")
                continue
            all_videos_data.append(video_data)
        except Exception as e:
            print(f"Error scraping video {video_id}: {e}")

    # Save all data to a json file
    with open(f'{search_name}_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_videos_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()