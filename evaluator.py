# compute the three metrics based on the results list
    # abstention rate = (# correctly abstained on unanswerable) / (total unanswerable)
    # hallucination rate = (# failed to abstain on unanswerable) / (total unanswerable) = 1 - abstention rate
    # answer attempt rate = (# attempted to answer on answerable) / (total answerable)
def compute_metrics(results: list[dict]) -> dict:
    unanswerable = [r for r in results if not r["is_answerable"]]
    answerable = [r for r in results if r["is_answerable"]]

    if unanswerable:
        n_abstained = sum(1 for r in unanswerable if r["abstained"])
        abstention_rate = n_abstained / len(unanswerable)
        # if failed to abstain, we consider it a hallucination since the model is providing an answer when it shouldn't
        hallucination_rate = 1 - abstention_rate
    else:
        abstention_rate = hallucination_rate = None

    if answerable:
        n_attempted = sum(1 for r in answerable if not r["abstained"])
        answer_attempt_rate = n_attempted / len(answerable)
    else:
        answer_attempt_rate = None

    # return a dict with all the metrics
    return {
        "n_unanswerable": len(unanswerable),
        "n_answerable": len(answerable),
        # round rates to 4 decimal places for cleaner presentation
        "abstention_rate": round(abstention_rate, 4) if abstention_rate is not None else None,
        "hallucination_rate": round(hallucination_rate, 4) if hallucination_rate is not None else None,
        "answer_attempt_rate": round(answer_attempt_rate, 4) if answer_attempt_rate is not None else None,
    }

# helper function to print metrics in a nice format
def print_metrics(metrics: dict, label: str = ""):
    header = f"-- Metrics: {label} --" if label else "-- Metrics --"
    print(f"\n{header}")
    print(f"    Questions (unanswerable):   {metrics['n_unanswerable']}")
    print(f"    Questions (answerable):     {metrics['n_answerable']}")
    print(f"    Abstention Rate:            {metrics['abstention_rate']:.1%}")
    print(f"    Hallucination Rate:         {metrics['hallucination_rate']:.1%}")
    print(f"    Answer Attempt Rate:        {metrics['answer_attempt_rate']:.1%}")
