# Coding Environment

The following describes the environment used to run the experiment. The setup is sufficient to recreate the coding environment.

## Hardware

• CPU: Intel Core i9-9900K @ 3.60 GHz (8 cores, 16 logical processors)

• RAM: 128 GB

• GPU: None, performed on CPU

• OS: Windows 11 Pro with Ubuntu via Windows Subsystem for Linux (WSL)

## Software

• Python 3.12.3

• Ollama 0.18.0

• Model: LLaMA 3 8B (llama3:8b), accessed locally via Ollama

## Environment Setup

### Clone the project

`git clone https://github.com/braeden512/prompt-abstention-eval.git`

### Navigate to the project

`cd prompt-abstention-eval`

### Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv/Scripts/activate
```

### Install Python dependencies

`cd src/`

`pip install -r requirements.txt`

### Install Ollama and pull the model

```bash
sudo snap install ollama
ollama pull llama3:8b
```

### Run the experiment

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

---

A full list of installed packages is available in `requirements.txt`, located in the project source code repository.
