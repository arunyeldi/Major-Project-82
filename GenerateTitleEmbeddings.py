import pandas as pd
import json
from openai import OpenAI
import numpy as np

# --------------------------
# Load Data
# --------------------------
with open('youtube_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)  # Now df is defined!

# --------------------------
# Generate Embeddings
# --------------------------
client = OpenAI(api_key="YOUR_API_KEY")  # Replace with your key

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

df['title_embedding'] = df['title'].apply(get_embedding)

# Save embeddings for clustering
df.to_pickle('embeddings.pkl')
print("Embeddings generated successfully!")