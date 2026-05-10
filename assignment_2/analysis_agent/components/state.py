from typing import Optional, Dict, Any, TypedDict

class AnalysisAgentState(TypedDict): 
    """
    State schema for the Analysis Agent.  This is going to be used to store the state of the agent 
    as it processes the stock data and generates the analysis report.

    It is a TypedDict schema that defines the structure of the state object
    
    This agent is designed to analyze stock market data. It takes a stock ticker symbol as input,
    retrieves historical price data, performs technical analysis, and generates an analysis report
    about the stock's performance.
    
    Fields:
        ticker (str): Stock ticker for analysis.
        historical_data (dict | None): Historical price data for the stock.
        technical_data (dict | None): Technical analysis results.
        recommendation_info (str | None): Final formatted recommendation information string.
    """
    
    # Input
    ticker: str
    
    # Intermediate data
    historical_data: Optional[Dict[str, Any]]
    technical_data: Optional[Dict[str, Any]]
    
    # Final output
    recommendation_info: Optional[str]
