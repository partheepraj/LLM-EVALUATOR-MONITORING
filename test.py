from evaluator import evaluate_prompt

prompt = input("Enter Prompt: ")

result = evaluate_prompt(prompt)

print("\n===== RESULT =====\n")

print(result["Response"])

print("\nLatency:", result["Latency"], "seconds")
print("Word Count:", result["Word_Count"])
print("Character Count:", result["Char_Count"])
print("Quality Score:", result["Quality_Score"], "%")
print("Hallucination Score:", result["Hallucination_Score"], "%")
print("Hallucination Risk:", result["Hallucination_Risk"])
print("Response Rating:", result["Response_Rating"])