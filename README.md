# LangGraph Assessment AI

Final assessment project for demonstrating practical LangGraph agent development, debugging, state management, API integration, and notebook-based documentation for Springer Capital
LLM internship.

The repository contains two assignments:

- **Assignment 1:** debug and repair a weather agent.
- **Assignment 2:** build a stock market analysis agent from scratch.

## Project Structure

```text
langgraph_assessment/
├── assignment_1/
│   ├── weather_agent/
│   │   ├── components/
│   │   │   ├── config.py
│   │   │   ├── helper_functions.py
│   │   │   ├── nodes.py
│   │   │   ├── schema.py
│   │   │   └── state.py
│   │   ├── graph.py
│   │   ├── main.py
│   │   └── requirements.txt
│   └── weather_agent_debug.ipynb
├── assignment_2/
│   ├── analysis_agent/
│   │   ├── components/
│   │   │   ├── config.py
│   │   │   ├── helper_functions.py
│   │   │   ├── nodes.py
│   │   │   ├── schema.py
│   │   │   └── state.py
│   │   ├── graph.py
│   │   └── main.py
│   └── analysis_agent.ipynb
└── README.md
```

## Assignment 1: Weather Agent Debugging

Debug a broken LangGraph weather agent and make it fully functional.

The weather agent is designed to:

1. Accept a user name.
2. Fetch location data based on the current IP address.
3. Fetch current weather for the detected location.
4. Display a formatted weather report.

The debugging process and testing of successful and failure scenarios is contained in `assignment_1/weather_agent_debug.ipynb`

The fixed weather agent printd a clean weather summary containing the detected location and current weather information.

## Assignment 2: Stock Market Analysis Agent

Build a LangGraph stock analysis agent from scratch.

The stock agent is designed to:

1. Accept a stock ticker symbol, such as `AAPL`, `MSFT`, or `NVDA`.
2. Fetch 60 days of historical stock data using `yfinance`.
3. Calculate technical indicators:
   - 10-day Simple Moving Average;
   - 20-day Simple Moving Average;
   - 14-day Relative Strength Index.
4. Generate a `BUY`, `HOLD`, or `SELL` recommendation.
5. Display a formatted analysis report and supporting chart.

### Agent Flow

```text
START
  ↓
fetch_stock_data
  ↓
generate_technical_indicators
  ↓
generate_recommendation_node
  ↓
END
```

### Recommendation Logic

The recommendation is based on SMA crossover and RSI:

- `BUY`: 10-day SMA is above 20-day SMA and RSI is between 50 and 70.
- `SELL`: 10-day SMA is below 20-day SMA and RSI is between 30 and 50.
- `HOLD`: all other cases.

### Expected Output

The stock analysis agent printd:

- the ticker being analyzed;
- the final recommendation;
- the latest 10-day SMA;
- the latest 20-day SMA;
- the latest RSI;
- a visual chart showing price movement, moving averages, and RSI.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install langchain==0.3.26 langchain-core==0.3.75 langgraph==0.6.4
pip install pydantic==2.11.5 pydantic-settings==2.10.1 python-dotenv
pip install requests pandas numpy matplotlib yfinance jupyter
```

## Running the Agents

Run commands from the repository root:

```bash
cd final_assessment/langgraph_assessment
```

### Weather Agent

```bash
python -m assignment_1.weather_agent.main
```

The program prompts for a name and then displays weather data for the detected IP-based location.

### Stock Analysis Agent

```bash
python -m assignment_2.analysis_agent.main
```

The program prompts for a ticker symbol. If no ticker is entered, it defaults to `NVDA`.

## Notebooks

The project includes notebook demonstrations for both assignments:

- `assignment_1/weather_agent_debug.ipynb`
  - documents the weather agent bugs;
  - explains the fixes;
  - demonstrates the repaired agent.

- `assignment_2/analysis_agent.ipynb`
  - demonstrates the stock analysis agent;
  - runs the LangGraph workflow;
  - shows recommendation output and plots.


