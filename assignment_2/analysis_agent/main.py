from .graph import analysis_agent
from .components.helper_functions import plot_rsi_with_candles


def main():
    ticker = input("Enter the ticker symbol of interest: ").strip().upper()

    if not ticker:
        ticker = "NVDA"

    state = {
        "ticker": ticker,
        "historical_data": None,
        "technical_data": None, 
        "recommendation_info": None,
    }

    try:
        final_state = analysis_agent.invoke(state)

        print("\n" + "=" * 60)
        print("ANALYSIS INFORMATION")
        print("=" * 60)

        recommendation_info = final_state.get("recommendation_info")

        if recommendation_info:
            print(recommendation_info)
        else:
            print("Sorry, unable to retrieve recommendation information at this time.")

        historical_data = final_state.get("historical_data")
        technical_data = final_state.get("technical_data")

        if historical_data and technical_data:
            plot_rsi_with_candles(
                ticker=final_state["ticker"],
                date=historical_data["date"],
                open=historical_data["open"],
                high=historical_data["high"],
                low=historical_data["low"],
                closing=historical_data["close"],
                ten_day_sma=technical_data["ten_day_simple_moving_average"],
                twenty_day_sma=technical_data["twenty_day_simple_moving_average"],
                rsi=technical_data["relative_strength_index"],
            )

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check your ticker symbol, internet connection, and try again.")


if __name__ == "__main__":
    main()