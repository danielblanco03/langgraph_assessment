from typing import Optional, Dict, Any, TypedDict

class WeatherAgentState(TypedDict): #A TypedDict type represents dict objects that contain only keys of type str.
    """
    State schema for the Weather Agent.

    It is a TypedDict schema that defines the structure of the state object
    
    This agent fetches location data based on IP address, retrieves current weather
    information, and generates a personalized weather greeting message.
    
    Fields:
        name (str): User's name for personalized greeting.
        location_data (dict | None): Location information from IP geolocation API.
        weather_data (dict | None): Weather information from Open-Meteo API.
        weather_info (str | None): Final formatted weather information string.
    """
    
    # Input
    name: str
    
    # Intermediate data
    location_data: Optional[Dict[str, Any]]
    weather_data: Optional[Dict[str, Any]]
    
    # Final output
    weather_info: Optional[str]

