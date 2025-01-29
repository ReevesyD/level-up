# Career Skills Gap Analyser

A Python-based system that uses OpenAI's GPT-4 to analyse the gap between your current skills and job requirements, then generates a personalised learning path. 

Utilises:
- Multi-threaded processing of LLM calls
- AI Agent Chaining
- AI Prompt Engineering
- Pydantic for Data Validation and Type Checking


## Features

- LinkedIn profile skills extraction
- Job requirements analysis
- Skills gap identification
- Personalised learning path generation
- Detailed progress milestones
- Resource recommendations

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd level-up
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # For Mac/Linux
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

1. Run the main script:
```bash
python3 -m src.main
```

2. When prompted:
   - Paste your resume / linkedin profile text
   - Paste the job listing text

3. The system will analyse the inputs and provide:
   - Current technical skills assessment
   - Identified skill gaps
   - Personalised learning path
   - Resource recommendations
   - Progress milestones

4. Detailed results will be saved to `analysis_results.json`

## Project Structure

- `src/`
  - `main.py` - Main entry point and CLI interface
  - `models.py` - Pydantic data models
  - `chains.py` - LLM chain implementations
  - `orchestrator.py` - Chain orchestration logic
- `requirements.txt` - Project dependencies
- `README.md` - Project documentation

## Dependencies

- Python 3.8+
- OpenAI API
- Pydantic
- python-dotenv
- aiohttp

## Licence

MIT Licence
