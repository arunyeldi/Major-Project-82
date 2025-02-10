from ollama import Client
import pandas as pd
import json

# Load your data
with open('youtube_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Initialize Ollama client
client = Client(host='http://localhost:11434')  # Default Ollama port

# Generate embeddings
def get_embedding(text):
    response = client.embeddings(model='nomic-embed-text', prompt=text)
    return response['embedding']

df['title_embedding'] = df['title'].apply(get_embedding)
print("Embeddings generated successfully!")