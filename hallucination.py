from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def hallucination_score(prompt, response):

    prompt_emb = model.encode([prompt])
    response_emb = model.encode([response])

    similarity = cosine_similarity(
        prompt_emb,
        response_emb
    )[0][0]

    score = round(similarity * 100, 2)

    if score >= 80:
        risk = "Low"
    elif score >= 60:
        risk = "Medium"
    else:
        risk = "High"

    return score, risk