import requests
import time
import pandas as pd
import os
import glob

from quality_score import calculate_similarity
from hallucination import hallucination_score


def evaluate_prompt(prompt):

    start_time = time.time()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    response_text = response.json()["response"]

    latency = round(
        time.time() - start_time,
        2
    )

    word_count = len(
        response_text.split()
    )

    char_count = len(
        response_text
    )

    quality_score = calculate_similarity(
        prompt,
        response_text
    )

    hallucination_score_value, risk = hallucination_score(
        prompt,
        response_text
    )

    if quality_score >= 85:
        rating = "Excellent ⭐⭐⭐⭐⭐"
    elif quality_score >= 70:
        rating = "Good ⭐⭐⭐⭐"
    elif quality_score >= 50:
        rating = "Average ⭐⭐⭐"
    else:
        rating = "Poor ⭐⭐"

    result = {
        "Prompt": prompt,
        "Response": response_text,
        "Latency": latency,
        "Word_Count": word_count,
        "Char_Count": char_count,
        "Quality_Score": quality_score,
        "Hallucination_Score": hallucination_score_value,
        "Hallucination_Risk": risk,
        "Response_Rating": rating
    }

    csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "results.csv"
    )

    df = pd.DataFrame([result])
    header = not os.path.exists(csv_path)

    print("[DEBUG] Prompt:", prompt)
    print("[DEBUG] Response length:", len(response_text))
    print("[DEBUG] Word count:", word_count)
    print("[DEBUG] Character count:", char_count)
    print("[DEBUG] Quality score:", quality_score)
    print("[DEBUG] Hallucination score:", hallucination_score_value)

    # Count rows before save in all results files
    rows_before = 0
    all_results_files = glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results*.csv"))
    for file in all_results_files:
        try:
            rows_before += len(pd.read_csv(file))
        except Exception:
            pass

    path_written = csv_path
    try:
        df.to_csv(
            csv_path,
            mode="a",
            header=header,
            index=False,
            encoding="utf-8",
            lineterminator="\n"
        )
        print("[DEBUG] CSV row written:", csv_path)
    except PermissionError:
        fallback_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"results_locked_{int(time.time())}.csv"
        )
        df.to_csv(
            fallback_path,
            mode="a",
            header=not os.path.exists(fallback_path),
            index=False,
            encoding="utf-8",
            lineterminator="\n"
        )
        path_written = fallback_path
        print("[DEBUG] CSV row written (fallback):", fallback_path)

    # Count rows after save in all results files
    rows_after = 0
    all_results_files = glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results*.csv"))
    for file in all_results_files:
        try:
            rows_after += len(pd.read_csv(file))
        except Exception:
            pass

    print("[DEBUG] Rows before save:", rows_before)
    print("[DEBUG] Rows after save:", rows_after)
    print("[DEBUG] Current CSV row count:", rows_after)

    return {
        "response": response_text,
        "latency": latency,
        "word_count": word_count,
        "char_count": char_count,
        "quality_score": quality_score,
        "hallucination_score": hallucination_score_value,
        "hallucination_risk": risk,
        "rating": rating,
        "csv_path": path_written,
        "rows_before": rows_before,
        "rows_after": rows_after
    }