from langgraph.graph import StateGraph, START, END
from .components.state import AnalysisAgentState
from .components.nodes import (
    fetch_stock_data,
    generate_technical_indicators, 
    generate_recommendation_node
)

builder = StateGraph(AnalysisAgentState)

# Add nodes
builder.add_node("fetch_stock_data", fetch_stock_data)
builder.add_node("generate_technical_indicators", generate_technical_indicators)
builder.add_node("generate_recommendation_node", generate_recommendation_node)

# Add edges - simple linear flow
# Update: LangGraph processes nodes in parallel by default, so order doesn't matter
builder.add_edge(START, "fetch_stock_data")
builder.add_edge("fetch_stock_data", "generate_technical_indicators")
builder.add_edge("generate_technical_indicators", "generate_recommendation_node")
builder.add_edge("generate_recommendation_node", END)

# Auto-compile the graph
analysis_agent = builder.compile()