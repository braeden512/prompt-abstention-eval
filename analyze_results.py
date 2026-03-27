import os
import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
from config import RESULTS_DIR, PROMPTS
from evaluator import compute_metrics

# helper function to load the most recent results for all conditions
def load_latest_results():
    all_results = {}
    for condition in PROMPTS:
        files = sorted(glob.glob(os.path.join(RESULTS_DIR, f"{condition}_*.jsonl")))
        if not files:
            raise FileNotFoundError(
                f"No results for '{condition}'. Run `python run_experiment.py` first."
            )
        with open(files[-1]) as f:
            all_results[condition] = [json.loads(line) for line in f]
    return all_results

# function to generate bar charts comparing metrics across conditions
def plot_metrics(metrics_by_condition: dict, save_path="results/metrics_comparison.png"):
    conditions = list(metrics_by_condition.keys())
    metrics = [
        ("abstention_rate", "Abstention Rate\n(unanswerable)"),
        ("hallucination_rate", "Hallucination Rate\n(unanswerable)"),
        ("answer_attempt_rate", "Answer Attempt Rate\n(answerable)"),
    ]
    colors = ["#4C72B0", "#DD8452", "#55A868"]
    
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle(
        "Prompt Variation Study: LLaMA 3 8B on SQuAD2.0\n"
        "Explicit vs. Implicit vs. Baseline Abstention Instruction", fontsize=12
    )
    
    for ax, (key, label) in zip(axes, metrics):
        values = [metrics_by_condition[c][key] for c in conditions]
        bars = ax.bar([c.capitalize() for c in conditions], values, 
                      color=colors[:len(conditions)], width=0.5)
        ax.set_title(label, fontsize=11)
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("Rate")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
        
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                   f"{val:.1%}", ha="center", va="bottom", fontsize=11, fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"Plot saved to {save_path}")
    plt.show()

# function to export edge cases (where model output was flagged for review) to a CSV for manual analysis
def export_edge_cases(all_results: dict):
    edge_cases = [r for results in all_results.values() 
                    for r in results if r.get("needs_review")]
    if not edge_cases:
        print("No edge cases flagged for review.")
        return
    
    df = pd.DataFrame(edge_cases)[
        ["condition", "question", "model_output", "is_answerable", "abstained"]
    ]
    out_path = os.path.join(RESULTS_DIR, "edge_cases_for_review.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved {len(edge_cases)} edge cases to {out_path}")


# function to export a summary CSV comparing key metrics across conditions for easy reference and sharing
def export_summary_csv(metrics_by_condition: dict):
    rows = []
    for condition, m in metrics_by_condition.items():
        rows.append({
            "Condition": condition.capitalize(),
            "N (unanswerable)": m["n_unanswerable"],
            "N (answerable)": m["n_answerable"],
            "Abstention Rate": f"{m['abstention_rate']:.1%}",
            "Hallucination Rate": f"{m['hallucination_rate']:.1%}",
            "Answer Attempt Rate": f"{m['answer_attempt_rate']:.1%}",
        })
    df = pd.DataFrame(rows)
    out_path = os.path.join(RESULTS_DIR, "summary_table.csv")
    df.to_csv(out_path, index=False)
    print(f"\nSummary table saved to {out_path}")
    print("\n" + df.to_string(index=False))


if __name__ == "__main__":
    all_results = load_latest_results()

    metrics_by_condition = {}
    for condition, results in all_results.items():
        clean = [r for r in results if r.get("abstained") is not None]
        metrics_by_condition[condition] = compute_metrics(clean)

    plot_metrics(metrics_by_condition)
    export_summary_csv(metrics_by_condition)
    export_edge_cases(all_results)
