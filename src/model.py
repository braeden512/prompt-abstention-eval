import ollama
# import constants from config file
from config import MODEL_NAME, OLLAMA_OPTIONS, PROMPTS

# query the model under a given condition (explicit or implicit)
def query(question: str, context: str, condition: str) -> str:
    if condition not in PROMPTS:
        raise ValueError(f"Unknown condition '{condition}'. "
                         f"Choose from: {list(PROMPTS.keys())}")

    prompt = PROMPTS[condition].format(question=question, context=context)
    # generate response from Ollama
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options=OLLAMA_OPTIONS,
    )
    # strip leading/trailing whitespace from the response
    return response["response"].strip()