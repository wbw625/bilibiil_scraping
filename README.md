# bilibiil_scraping (B站视频信息爬取)

这部分包含用于从Bilibili（bilibili.com）抓取视频信息的Python脚本。

## 代码文件说明

这部分主要包含两个Python文件：
1.  `scraping.py`: 主要功能是根据给定的`BV ID`获取单个Bilibili视频的详细信息。
2.  `crawling.py`: 使用 `scraping.py` 来收集多个视频的数据。它可以通过关键词搜索、获取首页推荐或检索“每周必看”视频列表来查找视频`BV ID`。

## 运行方式

只需直接运行：

```bash
python crawling.py
```

你可以取消`crawling.py`中`main`函数相关部分的注释来启用所需的功能。

例如，要通过关键词搜索视频，你可以取消以下代码的注释：
```python
# Search for videos by name
search_name = '大东彦'
prefix = '【大东彦】'
pages = 32  # Number of pages to scrape
video_ids = get_video_ids(search_name, pages)
```

要获取“每周必看”视频，你可以取消以下代码的注释：
```python
# Popular videos from Bilibili homepage
search_name = 'B站每周必看'
prefix = ''
num_pages = 20
video_ids = []
video_ids.extend(get_popular_video_ids(num_pages))
time.sleep(5)
```

要从首页推荐中获取视频ID，你可以取消以下代码的注释：
```python
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
```
