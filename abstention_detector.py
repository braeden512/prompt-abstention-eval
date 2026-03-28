# phrases that clearly indicate abstention
ABSTENTION_PHRASES = [
    # generic uncertainty
    "i don't know",
    "i do not know",
    "i'm not sure",
    "i am not sure",
    "i cannot answer",
    "i can't answer",
    "i don't have enough information",
    "i do not have enough information",
    "i don't have information",
    "not enough information",
    "insufficient information",
    "no information",
    # passage-grounded style refusals
    "the passage does not",
    "the passage doesn't",
    "the context does not",
    "the context doesn't",
    "not mentioned in the passage",
    "not stated in the passage",
    "not provided in the passage",
    "not found in the passage",
    "not mentioned in the context",
    "cannot be determined from",
    "cannot be found in",
    "no answer can be found",
    "there is no information",
    "the text does not",
    "based on the passage, i cannot",
    "based on the provided",
    # direct refusals
    "cannot provide an answer",
    "unable to answer",
    "this question cannot be answered",
    "there is no answer",
    "no answer is provided",
]

# phrases that are more ambiguous
# flag these for manual review
EDGE_CASE_PHRASES = [
    "it is unclear",
    "it's unclear",
    "it is not clear",
    "unclear from",
    "it depends",
    "may or may not",
    "i would need more",
    "without more context",
    "without additional",
]


# returns a boolean indicating whether the text is an abstention, and a reason for the classification
def is_abstention(text: str) -> tuple[bool, str]:
    lowered = text.lower()

    for phrase in ABSTENTION_PHRASES:
        if phrase in lowered:
            return True, "rule_match"

    for phrase in EDGE_CASE_PHRASES:
        if phrase in lowered:
            # treat edge cases as abstentions, but flag them for review since they could be borderline
            return True, "edge_case"

    return False, "answered"

# returns a dict with full classification info for a given model output
def classify_output(text: str) -> dict:
    abstained, reason = is_abstention(text)
    return {
        "output": text,
        "abstained": abstained,
        "classification_reason": reason,
        "needs_review": reason == "edge_case",
    }