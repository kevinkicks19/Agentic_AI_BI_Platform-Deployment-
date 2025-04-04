# Agenetic AI Business Intelligence Platform

An intelligent platform that leverages AI agents for business analysis, problem discovery, and solution planning.

## Features

- **Problem Discovery Workflow**: Automated business problem analysis using AI agents
- **Intelligent Agents**:
  - Coach Agent: Guides problem discovery through structured conversations
  - Router Agent: Analyzes problems and creates comprehensive solution plans
- **Document Generation**: Automated creation of inception documents and solution plans
- **Framework-Based Analysis**: Utilizes established business frameworks (SWOT, PESTLE, etc.)

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd agenetic-ai-business-intelligence
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Configure your API keys and settings

4. Install Ollama:
- Follow instructions at [Ollama's website](https://ollama.ai)
- Pull required models:
```bash
ollama pull llama2
```

## Usage

1. Run tests:
```bash
python -m pytest app/tests/ -v
```

2. Example workflow usage:
```python
from app.workflows.problem_discovery_workflow import ProblemDiscoveryWorkflow

workflow = ProblemDiscoveryWorkflow(
    workflow_id="example",
    name="Problem Analysis",
    description="Analyze business problem"
)

results = await workflow.execute({
    "initial_query": "Your business problem description",
    "user_context": {
        "industry": "Your Industry",
        "company_size": "Company Size",
        # ... other context
    }
})
```

## Project Structure

```
app/
├── agents/             # AI agent implementations
├── config/            # Configuration settings
├── tests/            # Test cases
└── workflows/        # Workflow implementations
```

## Dependencies

- Python 3.8+
- Ollama
- AutoGen
- FastAPI
- Other requirements listed in requirements.txt

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 