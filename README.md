# The Pipeline Creators

Welcome to **The Pipeline Creators**, a robust and modular framework for designing, implementing, and testing data engineering pipelines. This project leverages the power of **Pandas**, **Pydantic**, and **Pytest** to create reliable, validated, and production-ready pipelines for processing datasets.

## 🚀 Features

- **Dynamic Pipeline Design**: Automatically generate a detailed pipeline design document with stages, validation rules, and best practices.
- **Code Generation**: Transform the design into clean, type-hinted Python code with modular functions and classes.
- **Comprehensive Testing**: Generate Pytest scripts to ensure the pipeline's correctness, covering edge cases and validation scenarios.
- **Error Handling & Logging**: Built-in mechanisms for logging and handling validation errors.
- **AI-Powered Agents**: A team of specialized agents (Arquiteto, Engenheiro, Tester, Revisor) collaborates to deliver high-quality outputs.

## 📂 Project Structure

```plaintext
.
├── inputs/                # Raw input data (e.g., CSV files)
├── outputs/               # Generated outputs (design docs, code, tests, etc.)
├── src/                   # Source code for the framework
│   ├── the_pipeline_creators/
│   │   ├── config/        # Configuration files for agents and tasks
│   │   ├──         # Core logic for managing agents and tasks
│   │   ├──         # Entry point for running the pipeline
├── db/                    # Persistent database for knowledge indexing
├──               # Project documentation
├──          # Python project configuration
└── .env                   # Environment variables

## Installation

1. Install UV:

```
pip install uv
´´´

2. Navigate to the project directory and install dependencies:

```
crewai install
´´´
Add your OPENAI_API_KEY or the local ollama to the .env file.

## 🏃 Running the Project

To execute the pipeline creation process, run:

```
crewai run
´´´

This command initializes the Pipeline Crew, which will:

Design the pipeline (outputs/pipeline_design.md).
Generate the implementation code (outputs/pipeline_dados.py).
Write Pytest scripts (outputs/test_pipeline.py).
Optionally review the code (outputs/CODE_REVIEW.md).
🧠 Understanding the Pipeline Crew
The Pipeline Crew consists of four AI-powered agents, each with a unique role:

- Arquiteto: Designs the pipeline architecture.
- Engenheiro: Implements the pipeline in Python.
- Tester: Writes comprehensive Pytest scripts.
- Revisor: Reviews the code for quality and standards.

These agents collaborate using configurations defined in:

- config/agents.yaml: Agent roles and goals.
- config/tasks.yaml: Task descriptions and expected outputs.

## 🧪 Testing
Run the generated Pytest scripts to validate the pipeline:

´´´
pytest [test_pipeline.py](http://_vscodecontentref_/2)
´´´

🤝 Contributing
We welcome contributions! Feel free to open issues or submit pull requests to improve the project.

💬 Support
Need help? Reach out to us:

Join our Discord
Chat with our Docs