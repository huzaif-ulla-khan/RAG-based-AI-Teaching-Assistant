import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib 
import requests


def create_embedding(text_list):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "nomic-embed-text",
        "input": text_list
    })

    embedding = r.json()["embeddings"] 
    return embedding

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        # "model": "deepseek-r1",
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False
    })

    response = r.json()
    print(response)
    return response

df = joblib.load('embeddings.joblib')


incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0] 

# Find similarities of question_embedding with other embeddings
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding']).shape)
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
# print(similarities)
top_results = 5
max_indx = similarities.argsort()[::-1][0:top_results]
# print(max_indx)
new_df = df.loc[max_indx] 
# print(new_df[["title", "number", "text"]])

prompt = f"""
You are an AI Teaching Assistant.

You are ONLY allowed to answer using the information provided in the video subtitle chunks below.
DO NOT use outside knowledge.
DO NOT guess video names or timestamps.
If the answer is not clearly present in the chunks, say:
"I could not find this topic clearly explained in the provided videos."

Each chunk contains:
- video number
- video title
- start time (seconds)
- end time (seconds)
- spoken text

Video Chunks:
{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

--------------------

User Question:
"{incoming_query}"

Instructions:
1. Identify which video(s) explain the topic.
2. Mention the video number and title.
3. Mention the exact timestamp range (start–end) from the chunks.
4. Explain briefly what is taught at that timestamp.
5. If multiple videos cover it, list them clearly.

Answer format:
- Video <number>: <title>
  Timestamp: <start>–<end> seconds
  Explanation: <short explanation>
"""

with open("prompt.txt", "w") as f:
    f.write(prompt)

response = inference(prompt)["response"]
print(response)

with open("response.txt", "w") as f:
    f.write(response)
# for index, item in new_df.iterrows():
#     print(index, item["title"], item["number"], item["text"], item["start"], item["end"])