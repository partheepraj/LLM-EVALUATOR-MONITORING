from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_similarity(prompt, response):

    prompt_embedding = model.encode([prompt])
    response_embedding = model.encode([response])

    score = cosine_similarity(
        prompt_embedding,
        response_embedding
    )[0][0]

    return round(score * 100, 2)