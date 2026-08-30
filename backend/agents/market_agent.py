from typing import Dict

from services.market_service import MarketService


class MarketAgent:
    """
    Market Intelligence Agent

    Responsibilities:
    - Analyze latest official mandi prices
    - Identify market trend
    - Calculate price change
    - Estimate price outlook
    - Calculate profit potential
    - Return latest available market information
    """

    def __init__(self):

        self.market_service = MarketService()

    # ----------------------------------------------------
    # MAIN MARKET ANALYSIS
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
                "No market data found for the selected crop and location."
            )

        # ------------------------------------------------
        # Latest official mandi prices
        # ------------------------------------------------

        current_price = float(
            market.get(
                "current_price",
                market.get(
                    "modal_price",
                    0
                )
            ) or 0
        )

        minimum_price = float(
            market.get(
                "minimum_price",
                market.get(
                    "min_price",
                    0
                )
            ) or 0
        )

        maximum_price = float(
            market.get(
                "maximum_price",
                market.get(
                    "max_price",
                    0
                )
            ) or 0
        )

        # ------------------------------------------------
        # Average/reference price
        #
        # Prefer service-provided historical average.
        # Otherwise calculate the average of min/max.
        # ------------------------------------------------

        average_price = market.get(
            "average_price"
        )

        if average_price is None:

            if (
                minimum_price > 0
                and maximum_price > 0
            ):

                average_price = (
                    minimum_price
                    + maximum_price
                ) / 2

            else:

                average_price = current_price

        average_price = float(
            average_price or 0
        )

        # ------------------------------------------------
        # Market trend
        # ------------------------------------------------

        trend = self._market_trend(
            current_price,
            average_price
        )

        # ------------------------------------------------
        # Price change
        # ------------------------------------------------

        price_change_percentage = (
            self._price_change_percentage(
                current_price,
                average_price
            )
        )

        # ------------------------------------------------
        # Forecast / outlook
        # ------------------------------------------------

        forecast = self._price_forecast(
            trend
        )

        # ------------------------------------------------
        # Profit potential
        # ------------------------------------------------

        profit = self._profit_potential(
            current_price,
            average_price
        )

        # ------------------------------------------------
        # Confidence
        # ------------------------------------------------

        confidence = self._confidence_score(
            trend,
            profit
        )

        # ------------------------------------------------
        # Return
        # ------------------------------------------------

        return {

            "crop":
                market.get(
                    "crop",
                    crop
                ),

            "market":
                market.get(
                    "market",
                    "Unknown"
                ),

            "district":
                market.get(
                    "district",
                    district
                ),

            "state":
                market.get(
                    "state",
                    state
                ),

            "current_price":
                current_price,

            "average_price":
                round(
                    average_price,
                    2
                ),

            "minimum_price":
                minimum_price,

            "maximum_price":
                maximum_price,

            "arrival_quantity":
                market.get(
                    "arrival_quantity",
                    market.get(
                        "arrivals",
                        0
                    )
                ),

            "unit":
                market.get(
                    "unit",
                    "₹/quintal"
                ),

            "market_trend":
                trend,

            "price_change_percentage":
                round(
                    price_change_percentage,
                    2
                ),

            "price_forecast":
                forecast,

            "profit_potential":
                profit,

            "confidence":
                confidence,

            "last_updated":
                market.get(
                    "last_updated",
                    market.get(
                        "arrival_date",
                        market.get(
                            "date",
                            None
                        )
                    )
                ),

            "data_source":
                market.get(
                    "data_source",
                    "Government of India - data.gov.in / Agmarknet"
                )

        }

    # ----------------------------------------------------
    # MARKET TREND
    # ----------------------------------------------------

    def _market_trend(
        self,
        current_price: float,
        average_price: float
    ) -> str:

        if average_price <= 0:

            return "Unavailable"

        if current_price >= average_price * 1.10:

            return "Strongly Increasing"

        elif current_price > average_price:

            return "Increasing"

        elif current_price <= average_price * 0.90:

            return "Strongly Decreasing"

        elif current_price < average_price:

            return "Decreasing"

        return "Stable"

    # ----------------------------------------------------
    # PRICE CHANGE
    # ----------------------------------------------------

    def _price_change_percentage(
        self,
        current_price: float,
        average_price: float
    ) -> float:

        if average_price <= 0:

            return 0.0

        return (
            (
                current_price
                - average_price
            )
            / average_price
        ) * 100

    # ----------------------------------------------------
    # PRICE OUTLOOK
    # ----------------------------------------------------

    def _price_forecast(
        self,
        trend: str
    ) -> str:

        forecasts = {

            "Strongly Increasing":
                "Current mandi prices are significantly above the reference price. Prices may remain strong if market conditions continue.",

            "Increasing":
                "Current mandi prices are above the reference price. Prices may remain firm if demand continues.",

            "Stable":
                "Current mandi prices are close to the reference price. Prices may remain relatively stable.",

            "Decreasing":
                "Current mandi prices are below the reference price. Monitor the market before making major selling decisions.",

            "Strongly Decreasing":
                "Current mandi prices are significantly below the reference price. Prices are currently under pressure.",

            "Unavailable":
                "Insufficient price history is available for a reliable market outlook."

        }

        return forecasts.get(
            trend,
            "Market outlook unavailable."
        )

    # ----------------------------------------------------
    # PROFIT POTENTIAL
    # ----------------------------------------------------

    def _profit_potential(
        self,
        current_price: float,
        average_price: float
    ) -> str:

        if average_price <= 0:

            return "Unavailable"

        percentage = (
            (
                current_price
                - average_price
            )
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
    # CONFIDENCE SCORE
    # ----------------------------------------------------

    def _confidence_score(
        self,
        trend: str,
        profit: str
    ) -> int:

        score = 50

        # Trend contribution

        if trend == "Strongly Increasing":

            score += 25

        elif trend == "Increasing":

            score += 15

        elif trend == "Stable":

            score += 10

        elif trend == "Decreasing":

            score += 5

        # Profit contribution

        if profit == "Excellent":

            score += 25

        elif profit == "High":

            score += 15

        elif profit == "Moderate":

            score += 10

        elif profit == "Low":

            score += 5

        return min(
            score,
            100
        )