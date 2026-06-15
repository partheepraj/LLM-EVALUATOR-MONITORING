from evaluator import evaluate_prompt

print("=== Prompt A ===")
prompt_a = input("Enter Prompt A: ")

print("\n=== Prompt B ===")
prompt_b = input("Enter Prompt B: ")

result_a = evaluate_prompt(prompt_a)
result_b = evaluate_prompt(prompt_b)

print("\n========== COMPARISON ==========")

print("\nPROMPT A")
print("Latency:", result_a["Latency"])
print("Words:", result_a["Word_Count"])
print("Characters:", result_a["Char_Count"])

print("\nPROMPT B")
print("Latency:", result_b["Latency"])
print("Words:", result_b["Word_Count"])
print("Characters:", result_b["Char_Count"])

print("\n===== WINNER =====")

if result_a["Word_Count"] > result_b["Word_Count"]:
    print("Prompt A generated more detailed output")
else:
    print("Prompt B generated more detailed output")