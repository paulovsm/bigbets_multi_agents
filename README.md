# BigBets Origination Assistant

An AI-powered assistant for analyzing opportunities across different industries, powered by [crewAI](https://crewai.com).

## Installation

Requirements:
- Python >=3.10 <=3.13
- [UV](https://docs.astral.sh/uv/) for dependency management

### Initial Setup

1. Install UV (if you haven't already):
```bash
pip install uv
```

2. Install dependencies:
```bash
crewai install
```

3. Configure your credentials in the `.env` file:
```
OPENAI_API_KEY=your_key_here
```

## Running the Application

There are two ways to run the application:

### 1. Basic Local Mode
```bash
./startup.sh
```

### 2. Ngrok Mode (Remote Access)
```bash
./startup_ngrok.sh
```

The Ngrok script will provide a URL that can be used to access the application remotely.

## Using the Assistant

1. Access the application through your browser (local or Ngrok URL)

2. Specify the industry you want to analyze. You can include details such as:
   - Region of interest (default: Brazil)
   - Number of main players to analyze (default: 10)
   - Whether you want to provide feedback during the process
   - Which steps to execute (Value Chain, Supply Signals, Demand Signals, Whitespace)

3. The assistant will:
   - Generate a unique ID for your analysis
   - Execute the selected steps
   - Save results in the `output/[Analysis_ID]` folder

4. You can interact with existing knowledge bases using a previous analysis ID

## Analysis Structure

The complete process includes four main steps:

1. **Value Chain Analysis**: Industry value chain analysis
2. **Supply Signals**: Supply-side signals analysis
3. **Demand Signals**: Demand-side signals analysis
4. **Whitespace Identification**: Opportunity identification

## Support

- [crewAI Documentation](https://docs.crewai.com)
- [crewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Discord](https://discord.com/invite/X4JWnZnxPb)
