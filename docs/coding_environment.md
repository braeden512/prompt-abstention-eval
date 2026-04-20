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

### Install ollama via snap

`sudo snap install ollama`

### Pull the model

`ollama pull lama3:8b`

### Clone the project

`git clone https://github.com/braeden512/prompt-abstention-eval.git`

### Navigate to the project

`cd prompt-abstention-eval`

### Create and activate virtual environment

`python3 -m venv venv`

`source venv/bin/activate`

### Install dependencies

`cd src`

`pip install -r requirements.txt`

### Run the experiment

`python run_experiment.py`

### Analyze results

`python analyze_results.py`

---

A full list of installed packages is available in `requirements.txt`, located in the project source code repository.
