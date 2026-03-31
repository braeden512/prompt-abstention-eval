# LLM Abstention Study: Prompt Style Effects in Passage-Grounded Generation

NLP Research Project: LLaMA 3 8B Instruct on SQuAD2.0

## Research Question

Does explicit abstention instruction drive abstention behavior in passage-grounded generation, or is passage grounding alone sufficient? We compare two prompt styles with varying levels of abstention guidance.

## Experimental Design

Two conditions, both using passage-grounded generation (passage + question):

1. **EXPLICIT** - Scripts exact refusal phrase: "The passage does not contain enough information..."
2. **IMPLICIT** - Tells model to use only passage info, say so if not present

Both conditions receive identical passages and questions. Only the prompt template differs.

Note: This is passage-grounded generation, not full RAG with retrieval. Passages are supplied directly in the prompt rather than retrieved from a document store. This design isolates prompt-level abstention instruction as the sole independent variable.

## Setup

### 1. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv/Scripts/activate
```

### 2. Install Python dependencies

`pip install -r requirements.txt`

### 3. Install Ollama and pull the model

```bash
sudo snap install ollama
ollama pull llama3:8b
```

### 3. Run the experiment

Navigate to the `src/` directory and run the experiment:

```bash
cd src

# quick test with 10 questions per split (recommended first run)
python run_experiment.py --sample 10

# medium run
python run_experiment.py --sample 250

# full run
python run_experiment.py --sample 500

# use default sample size from experiment
python run_experiment.py

# analyze results / generate plots after run completes
python analyze_results.py
```

Results will be saved to the `results/` directory in the project root.

## Metrics

- **Abstention Rate** - % of unanswerable questions where model abstained
- **Hallucination Rate** - % of unanswerable questions where model gave an answer
- **Answer Attempt Rate** - % of answerable questions where model tried to answer
