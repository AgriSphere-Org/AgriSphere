from typing import Dict

from services.market_service import MarketService


class MarketAgent:
    """
    Market Intelligence Agent

    Responsibilities:
    - Analyze market prices
    - Identify market trend
    - Estimate price forecast
    - Calculate profit potential
    - Generate market intelligence
    """

    def __init__(self):

        self.market_service = MarketService()

    # ----------------------------------------------------

    def analyze_market(

        self,

        crop: str,

        state: str,

        district: str

    ) -> Dict:

        market = self.market_service.get_market_data(

            crop,

            state,

            district

        )

        if not market:

            raise ValueError(

                "No market data found."

            )

        trend = self._market_trend(

            market["current_price"],

            market["average_price"]

        )

        forecast = self._price_forecast(

            trend

        )

        profit = self._profit_potential(

            market["current_price"],

            market["average_price"]

        )

        confidence = self._confidence_score(

            trend,

            profit

        )

        return {

            "crop": market["crop"],

            "market": market["market"],

            "district": market["district"],

            "state": market["state"],

            "current_price": market["current_price"],

            "average_price": market["average_price"],

            "minimum_price": market["minimum_price"],

            "maximum_price": market["maximum_price"],

            "arrival_quantity": market["arrival_quantity"],

            "unit": market["unit"],

            "market_trend": trend,

            "price_forecast": forecast,

            "profit_potential": profit,

            "confidence": confidence

        }

    # ----------------------------------------------------

    def _market_trend(

        self,

        current_price: float,

        average_price: float

    ) -> str:

        if current_price > average_price * 1.10:

            return "Strongly Increasing"

        elif current_price > average_price:

            return "Increasing"

        elif current_price < average_price * 0.90:

            return "Strongly Decreasing"

        elif current_price < average_price:

            return "Decreasing"

        return "Stable"

    # ----------------------------------------------------

    def _price_forecast(

        self,

        trend: str

    ) -> str:

        forecasts = {

            "Strongly Increasing":
                "Prices are expected to continue rising.",

            "Increasing":
                "Prices may rise further in the coming days.",

            "Stable":
                "Prices are likely to remain stable.",

            "Decreasing":
                "Prices may decline further.",

            "Strongly Decreasing":
                "Prices are expected to remain under pressure."

        }

        return forecasts.get(

            trend,

            "Forecast unavailable."

        )

    # ----------------------------------------------------

    def _profit_potential(

        self,

        current_price: float,

        average_price: float

    ) -> str:

        percentage = (

            (current_price - average_price)

            / average_price

        ) * 100

        if percentage >= 15:

            return "Excellent"

        elif percentage >= 5:

            return "High"

        elif percentage >= 0:

            return "Moderate"

        return "Low"

    # ----------------------------------------------------

    def _confidence_score(

        self,

        trend: str,

        profit: str

    ) -> int:

        score = 50

        if trend == "Strongly Increasing":

            score += 25

        elif trend == "Increasing":

            score += 15

        elif trend == "Stable":

            score += 10

        if profit == "Excellent":

            score += 25

        elif profit == "High":

            score += 15

        elif profit == "Moderate":

            score += 10

        return min(score, 100)