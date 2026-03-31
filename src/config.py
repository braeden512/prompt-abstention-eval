MODEL_NAME = "llama3:8b"

OLLAMA_OPTIONS = {
    "temperature": 0.0,
    "num_predict": 200,
}

# how many questions to sample per split (answerable / unanswerable)
SAMPLE_PER_SPLIT = 500

# random seed for reproducibility
RANDOM_SEED = 42

# output paths (relative to src/ directory where scripts are run from)
RESULTS_DIR = "../results"

# Explicit: Scripts the exact refusal phrase. Tests whether explicitly telling the model to say a specific phrase when it can't answer leads to better abstention behavior.
PROMPT_EXPLICIT = """You are a reading comprehension assistant. Answer the question using only the information in the passage below.
If the passage does not contain enough information to answer the question, you must respond with exactly: "The passage does not contain enough information to answer this question."
Do not use any outside knowledge.

Passage:
{context}

Question: {question}

Answer:"""


# Implicit: Constrains the model to the passage but doesn't script the refusal phrase. Tests whether passage-grounding alone is enough for the model to figure out abstention on its own.
PROMPT_IMPLICIT = """Answer the question using only the information in the passage below.
If the passage does not contain the answer, say so.
Do not use any outside knowledge.

Passage:
{context}

Question: {question}

Answer:"""

# map names to prompt templates
PROMPTS = {
    "explicit": PROMPT_EXPLICIT,
    "implicit": PROMPT_IMPLICIT,
}
