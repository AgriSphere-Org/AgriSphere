from typing import Dict
from services.market_service import MarketService


class MarketAgent:
    """
    Market Intelligence Agent
    """

    def __init__(self):
        self.market_service = MarketService()

    def analyze_market(self, crop: str, state: str, district: str) -> Dict:
        market = self.market_service.get_market_data(crop, state, district)
        if not market:
            raise ValueError("No market data found.")

        trend = self._market_trend(market["current_price"], market["average_price"])
        forecast = self._price_forecast(trend)
        profit = self._profit_potential(market["current_price"], market["average_price"])
        confidence = self._confidence_score(trend, profit)

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
            "confidence": confidence,
        }

    def analyze_crop(self, crop: str) -> Dict:
        """Analyzes market trends, forecast, and reasoning for a specific crop."""
        market = self.market_service.get_crop(crop)
        if not market:
            raise ValueError(f"Crop '{crop}' not found in market database.")

        trend = self._market_trend(market["current_price"], market["average_price"])
        forecast = self._price_forecast(trend)
        profit = self._profit_potential(market["current_price"], market["average_price"])
        confidence = self._confidence_score(trend, profit)
        reasoning = self._generate_reasoning(
            market["current_price"], market["average_price"], trend, forecast
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
            "confidence": confidence,
            "price_history": market.get("price_history", []),
            "price_prediction": market.get("price_prediction", []),
            "reasoning": reasoning,
        }

    def compare_crop_trends(self, crop1: str, crop2: str) -> Dict:
        """Compares market trends and potential for two crops."""
        analysis_crop1 = self.analyze_crop(crop1)
        analysis_crop2 = self.analyze_crop(crop2)

        if analysis_crop1["confidence"] >= analysis_crop2["confidence"]:
            recommended_crop = analysis_crop1["crop"]
        else:
            recommended_crop = analysis_crop2["crop"]

        comparison_reasoning = self._compare_reasoning(analysis_crop1, analysis_crop2)

        return {
            "crop1": analysis_crop1,
            "crop2": analysis_crop2,
            "recommended_crop": recommended_crop,
            "comparison_reasoning": comparison_reasoning,
        }

    def _market_trend(self, current_price: float, average_price: float) -> str:
        if current_price > average_price * 1.10:
            return "Strongly Increasing"
        elif current_price > average_price:
            return "Increasing"
        elif current_price < average_price * 0.90:
            return "Strongly Decreasing"
        elif current_price < average_price:
            return "Decreasing"
        return "Stable"

    def _price_forecast(self, trend: str) -> str:
        forecasts = {
            "Strongly Increasing": "Prices are expected to continue rising.",
            "Increasing": "Prices may rise further in the coming days.",
            "Stable": "Prices are likely to remain stable.",
            "Decreasing": "Prices may decline further.",
            "Strongly Decreasing": "Prices are expected to remain under pressure.",
        }
        return forecasts.get(trend, "Forecast unavailable.")

    def _profit_potential(self, current_price: float, average_price: float) -> str:
        percentage = ((current_price - average_price) / average_price) * 100
        if percentage >= 15:
            return "Excellent"
        elif percentage >= 5:
            return "High"
        elif percentage >= 0:
            return "Moderate"
        return "Low"

    def _confidence_score(self, trend: str, profit: str) -> int:
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

    def _generate_reasoning(
        self,
        current_price: float,
        average_price: float,
        trend: str,
        forecast: str,
    ) -> str:
        if current_price > average_price:
            price_comparison = "Current market price is higher than the average market price."
        elif current_price < average_price:
            price_comparison = "Current market price is lower than the average market price."
        else:
            price_comparison = "Current market price is equal to the average market price."

        line2 = f"This indicates an {trend.lower()} market trend."
        line3 = f"{forecast}"

        if "Increasing" in trend:
            line4 = "Farmers may get better profit by waiting before selling."
        else:
            line4 = "Farmers should consider current demand before making selling decisions."

        return f"{price_comparison}\n{line2}\n{line3}\n{line4}"

    def _compare_reasoning(self, crop1_analysis: Dict, crop2_analysis: Dict) -> str:
        c1_name = crop1_analysis["crop"]
        c2_name = crop2_analysis["crop"]

        if crop1_analysis["confidence"] > crop2_analysis["confidence"]:
            better_crop = c1_name
            other_crop = c2_name
        elif crop2_analysis["confidence"] > crop1_analysis["confidence"]:
            better_crop = c2_name
            other_crop = c1_name
        else:
            better_crop = None

        line1 = f"Comparing {c1_name} ({crop1_analysis['market_trend']}) with {c2_name} ({crop2_analysis['market_trend']})."

        if better_crop:
            line2 = f"{better_crop} exhibits a stronger market confidence score compared to {other_crop}."
            line3 = f"The price forecast indicates better future returns and lower market risk for {better_crop}."
            line4 = f"Farmers are advised to prioritize {better_crop} for higher profitability."
        else:
            line2 = f"Both {c1_name} and {c2_name} show similar market confidence scores."
            line3 = "Future predictions indicate comparable market stability for both crops."
            line4 = "Farmers can choose based on local market access and holding capacity."

        return f"{line1}\n{line2}\n{line3}\n{line4}"