import os
import json
import argparse
# import constants from config file
from config import RESULTS_DIR, SAMPLE_PER_SPLIT, PROMPTS
from data_loader import load_squad2
from model import query
from abstention_detector import classify_output
from evaluator import compute_metrics, print_metrics

# run one condition over all questions, save results to a list of dicts, and return it
def run_condition(questions: list[dict], condition: str) -> list[dict]:
    results = []
    total = len(questions)
    for idx, item in enumerate(questions, 1):
        # print progress with condition name and percentage, overwrite the same line each time
        print(f"\rRunning [{condition}]: {idx}/{total} ({idx*100//total}%)", end="", flush=True)
        try:
            output = query(item["question"], item["context"], condition)
            classification = classify_output(output)

            results.append({
                "id": item["id"],
                "condition": condition,
                "question": item["question"],
                "context": item["context"],
                "gold_answers": item["answers"],
                "is_answerable": item["is_answerable"],
                "model_output": output,
                "abstained": classification["abstained"],
                "classification_reason": classification["classification_reason"],
                "needs_review": classification["needs_review"],
            })

        except Exception as e:
            print(f"\nERROR on question {item['id']}: {e}")
            results.append({
                "id": item["id"],
                "condition": condition,
                "question": item["question"],
                "is_answerable": item["is_answerable"],
                "model_output": None,
                "abstained": None,
                "error": str(e),
            })

    print()
    return results

def save_results(results: list[dict], filename: str):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

def load_results(filename: str) -> list[dict]:
    path = os.path.join(RESULTS_DIR, filename)
    with open(path) as f:
        return [json.loads(line) for line in f]

def main():
    parser = argparse.ArgumentParser()
    # default is 500 per split
    parser.add_argument("--sample", type=int, default=SAMPLE_PER_SPLIT)
    args = parser.parse_args()

    # load data
    print(f"\nLoading SQuAD2.0 (sample={args.sample} per split)...")
    answerable, unanswerable = load_squad2(sample_per_split=args.sample)
    all_questions = answerable + unanswerable
    print(f"Total questions: {len(all_questions)}")

    # run both conditions
    all_results = {}
    conditions = list(PROMPTS.keys())

    for i, condition in enumerate(conditions, 1):
        filename = f"{condition}_n{args.sample}.jsonl"
        print(f"\n{'='*50}")
        print(f"CONDITION {i}/{len(conditions)}: {condition.upper()}")
        print(f"{'='*50}")

        all_results[condition] = run_condition(all_questions, condition)
        save_results(all_results[condition], filename)

    # compute and print metrics for each condition, and save a summary json with all metrics for easy comparison later
    print(f"\n{'='*50}")
    print("RESULTS SUMMARY")
    print(f"{'='*50}")

    summary = {"sample_size": args.sample}
    for condition, results in all_results.items():
        clean = [r for r in results if r.get("abstained") is not None]
        metrics = compute_metrics(clean)
        print_metrics(metrics, condition.upper())
        summary[condition] = metrics

    summary_path = os.path.join(RESULTS_DIR, f"summary_n{args.sample}.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to {summary_path}")
    print("\nComplete. Run `python analyze_results.py` to generate plots.")


if __name__ == "__main__":
    main()