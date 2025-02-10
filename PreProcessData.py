import pandas as pd
import numpy as np
import json

# Load the scraped JSON data
with open('youtube_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Function to parse views (e.g., "1.2M views" → 1200000)
def parse_views(views_str):
    if 'views' in views_str:
        views_str = views_str.replace('views', '').strip()
    multipliers = {'K': 1e3, 'M': 1e6, 'B': 1e9}
    for suffix, multiplier in multipliers.items():
        if suffix in views_str:
            number = float(views_str.replace(suffix, '').strip())
            return int(number * multiplier)
    return int(views_str.replace(',', ''))

df['views'] = df['views'].apply(parse_views)

# Add placeholder columns (replace with actual scraped likes/comments if available)
df['likes'] = np.random.randint(100, 10000, len(df))  # Mock data
df['comments'] = np.random.randint(10, 1000, len(df))  # Mock data

# Calculate engagement ratios
df['likes_per_view'] = df['likes'] / df['views']
df['comments_per_view'] = df['comments'] / df['views']