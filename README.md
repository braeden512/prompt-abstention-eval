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

## Project Structure

```
RAG_Prompt_Style_Study/
- README.md
- requirements.txt
- config.py               # All settings and two prompt templates
- data_loader.py          # Load and partition SQuAD2.0
- model.py                # Ollama model interface
- abstention_detector.py  # Detect abstentions in outputs
- evaluator.py            # Compute metrics
- run_experiment.py       # Main script
- analyze_results.py      # Generate summary stats & plots
- results/                # Output saved here
```

## Setup

### 1. Install Ollama and pull the model

`ollama pull llama3:8b-instruct`

### 2. Install Python dependencies

`pip install -r requirements.txt`

### 3. Run the experiment

```bash
# quick test with 10 questions per split (recommended first run)
python run_experiment.py --sample 10

# medium run
python run_experiment.py --sample 250

# full run
python run_experiment.py --sample 500

# use default sample size from experiment
python run_experiment.py

# analyze results after run completes
python analyze_results.py
```

## Metrics

- **Abstention Rate** - % of unanswerable questions where model abstained
- **Hallucination Rate** - % of unanswerable questions where model gave an answer
- **Answer Attempt Rate** - % of answerable questions where model tried to answer

## Reproducing Results

1. Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Ensure Ollama is running with `llama3:8b-instruct` model
3. Run experiment: `python run_experiment.py`
4. Results will be saved to `results/` directory
5. Generate plots: `python analyze_results.py`
