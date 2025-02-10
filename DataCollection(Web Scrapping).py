from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

# --------------------------
# Configuration
# --------------------------
CHANNEL_URL = "https://www.youtube.com/@MrBeast/videos"  # Test channel
SCROLL_COUNT = 6
SCROLL_DELAY = 5  # Increased delay

# --------------------------
# Browser Setup
# --------------------------
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
# options.add_argument('--headless')  # Uncomment for background run

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# --------------------------
# Scraping Logic
# --------------------------
try:
    driver.get(CHANNEL_URL)
    
    # Wait for initial content load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-rich-item-renderer"))
    )

    # Scroll to load videos
    for _ in range(SCROLL_COUNT):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(SCROLL_DELAY)
        print(f"Scrolled {_+1}/{SCROLL_COUNT} times")

    # Updated parsing logic
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # CURRENT YOUTUBE SELECTORS (July 2024)
    video_cards = soup.select('ytd-rich-item-renderer:has(a#video-title-link)')
    print(f"Found {len(video_cards)} video elements")

    data = []
    for video in video_cards[:20]:
        try:
            title = video.select_one('a#video-title-link').text.strip()
            
            # Metadata section
            metadata = video.select_one('#metadata-line')
            views = metadata.select('span')[0].text if metadata else "N/A"
            
            data.append({
                'title': title,
                'views': views
            })
        except Exception as e:
            print(f"Error processing video: {str(e)}")
            continue

    # Save results
    with open('youtube_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Success! Saved {len(data)} videos")

finally:
    driver.quit()