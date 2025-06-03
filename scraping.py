# scraping.py
# This is for scraping data from bilibili.

import requests
from bs4 import BeautifulSoup

def scrape_bilibili_video(video_url):
    """
    Scrape video title and description from a Bilibili video page.
    
    Args:
        video_url (str): The URL of the Bilibili video.
        
    Returns:
        dict: A dictionary containing data of the video.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(video_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # title = 
    # description = 
    # likes =
    # coins = 
    # favorites =
    # author_followers =

    # return {
    #     'title': title,
    #     'description': description,
    #     'likes': likes,
    #     'coins': coins,
    #     'favorites': favorites,
    #     'author_followers': author_followers,
    # }

# Example usage:
if __name__ == "__main__":
    video_url = 'https://www.bilibili.com/video/BV155j2z7Etd/'
    video_data = scrape_bilibili_video(video_url)
    print(video_data)