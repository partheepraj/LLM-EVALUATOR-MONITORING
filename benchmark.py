import requests
import time
import pandas as pd

MODELS = [
    "llama3.2",
    "mistral",
    "gemma3"
]

prompt = input("Enter Prompt: ")

results = []

for model in MODELS:

    start = time.time()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    end = time.time()

    text = response.json()["response"]

    results.append({
        "Model": model,
        "Latency": round(end-start,2),
        "Words": len(text.split()),
        "Characters": len(text)
    })

df = pd.DataFrame(results)

print(df)

df.to_csv(
    "model_benchmark.csv",
    index=False
)