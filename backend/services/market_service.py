import os
from datetime import datetime
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


class MarketService:
    """
    Market Service

    Fetches agricultural mandi prices from the official
    Government of India data.gov.in / AGMARKNET API.
    """

    # =====================================================
    # DATA.GOV.IN RESOURCE
    # =====================================================

    BASE_URL = (
        "https://api.data.gov.in/resource/"
        "9ef84268-d588-465a-a308-a864a43d0070"
    )

    # =====================================================
    # CONFIGURATION
    # =====================================================

    TIMEOUT = 60

    DEFAULT_LIMIT = 20

    # Browser-like headers are required because the
    # data.gov.in API responds correctly to this request
    # format from our Python environment.
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        self.api_key = os.getenv(
            "DATA_GOV_API_KEY"
        )

        if not self.api_key:

            raise RuntimeError(
                "DATA_GOV_API_KEY is missing. "
                "Add your data.gov.in API key to backend/.env"
            )

    # =====================================================
    # GET MARKET DATA
    # =====================================================

    def get_market_data(
        self,
        crop: str,
        state: str,
        district: str
    ) -> Dict:

        # -------------------------------------------------
        # Validate
        # -------------------------------------------------

        crop = crop.strip()
        state = state.strip()
        district = district.strip()

        if not crop:

            raise ValueError(
                "Crop is required."
            )

        if not state:

            raise ValueError(
                "State is required."
            )

        if not district:

            raise ValueError(
                "District is required."
            )

        # -------------------------------------------------
        # API PARAMETERS
        # -------------------------------------------------

        params = {

            "api-key":
                self.api_key,

            "format":
                "json",

            "limit":
                self.DEFAULT_LIMIT,

            "offset":
                0,

            "filters[state]":
                state,

            "filters[district]":
                district,

            "filters[commodity]":
                crop
        }

        print(
            "\n========================================"
        )

        print(
            "MARKET API REQUEST"
        )

        print(
            f"Crop     : {crop}"
        )

        print(
            f"State    : {state}"
        )

        print(
            f"District : {district}"
        )

        print(
            "========================================"
        )

        # -------------------------------------------------
        # REQUEST
        # -------------------------------------------------

        try:

            response = requests.get(

                self.BASE_URL,

                params=params,

                headers=self.HEADERS,

                timeout=(10, self.TIMEOUT)

            )

        except requests.exceptions.ConnectTimeout:

            raise RuntimeError(
                "Could not connect to data.gov.in. "
                "The government API is not responding."
            )

        except requests.exceptions.ReadTimeout:

            raise RuntimeError(
                "data.gov.in connected but did not "
                f"return data within {self.TIMEOUT} seconds."
            )

        except requests.exceptions.ConnectionError:

            raise RuntimeError(
                "Unable to connect to data.gov.in. "
                "Check your internet connection."
            )

        except requests.exceptions.RequestException as e:

            raise RuntimeError(
                f"Market API connection failed: {str(e)}"
            )

        # -------------------------------------------------
        # HTTP STATUS
        # -------------------------------------------------

        print(
            f"HTTP STATUS: {response.status_code}"
        )

        if response.status_code == 403:

            raise RuntimeError(
                "data.gov.in rejected the API key. "
                "Check DATA_GOV_API_KEY in .env."
            )

        if response.status_code == 400:

            raise RuntimeError(
                "data.gov.in rejected the request. "
                "Check the filters and API parameters."
            )

        if response.status_code != 200:

            raise RuntimeError(
                f"data.gov.in returned HTTP "
                f"{response.status_code}."
            )

        # -------------------------------------------------
        # JSON
        # -------------------------------------------------

        try:

            data = response.json()

        except ValueError:

            raise RuntimeError(
                "data.gov.in returned an invalid JSON response."
            )

        # -------------------------------------------------
        # RECORDS
        # -------------------------------------------------

        records = data.get(
            "records",
            []
        )

        print(
            f"RECORDS RECEIVED: {len(records)}"
        )

        # -------------------------------------------------
        # NO DATA
        # -------------------------------------------------

        if not records:

            print(
                "No market records found for "
                f"{crop} / {state} / {district}"
            )

            return {}

        # -------------------------------------------------
        # CLEAN
        # -------------------------------------------------

        cleaned_records = [

            self._clean_record(
                record
            )

            for record in records

        ]

        # -------------------------------------------------
        # REMOVE INVALID PRICES
        # -------------------------------------------------

        cleaned_records = [

            record

            for record in cleaned_records

            if record["modal_price"] > 0

        ]

        if not cleaned_records:

            print(
                "Records were received but no valid "
                "modal prices were found."
            )

            return {}

        # -------------------------------------------------
        # SORT BY DATE
        # -------------------------------------------------

        cleaned_records.sort(

            key=lambda record:
                self._date_sort_value(
                    record.get(
                        "arrival_date"
                    )
                ),

            reverse=True

        )

        latest = cleaned_records[0]

        # -------------------------------------------------
        # REFERENCE AVERAGE
        # -------------------------------------------------

        modal_prices = [

            record["modal_price"]

            for record in cleaned_records

            if record["modal_price"] > 0

        ]

        if modal_prices:

            average_price = (
                sum(modal_prices)
                / len(modal_prices)
            )

        else:

            average_price = (
                latest["modal_price"]
            )

        # -------------------------------------------------
        # FINAL RESULT
        # -------------------------------------------------

        result = {

            "crop":
                latest["crop"],

            "market":
                latest["market"],

            "district":
                latest["district"],

            "state":
                latest["state"],

            "current_price":
                latest["modal_price"],

            "modal_price":
                latest["modal_price"],

            "average_price":
                round(
                    average_price,
                    2
                ),

            "minimum_price":
                latest["min_price"],

            "maximum_price":
                latest["max_price"],

            "arrival_quantity":
                latest.get(
                    "arrival_quantity",
                    0
                ),

            "unit":
                "₹/quintal",

            "arrival_date":
                latest["arrival_date"],

            "last_updated":
                latest["arrival_date"],

            "data_source":
                "Government of India - data.gov.in / AGMARKNET"

        }

        print(
            "MARKET RESULT:"
        )

        print(
            result
        )

        print(
            "========================================\n"
        )

        return result

    # =====================================================
    # GET ALL MARKET DATA
    # =====================================================

    def get_all_market_data(
        self,
        state: Optional[str] = None,
        crop: Optional[str] = None
    ) -> List[Dict]:

        params = {

            "api-key":
                self.api_key,

            "format":
                "json",

            "limit":
                self.DEFAULT_LIMIT,

            "offset":
                0

        }

        if state:

            params[
                "filters[state]"
            ] = state.strip()

        if crop:

            params[
                "filters[commodity]"
            ] = crop.strip()

        try:

            response = requests.get(

                self.BASE_URL,

                params=params,

                headers=self.HEADERS,

                timeout=(10, self.TIMEOUT)

            )

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.ConnectTimeout:

            raise RuntimeError(
                "Could not connect to data.gov.in."
            )

        except requests.exceptions.ReadTimeout:

            raise RuntimeError(
                f"data.gov.in did not respond within "
                f"{self.TIMEOUT} seconds."
            )

        except requests.exceptions.Timeout:

            raise RuntimeError(
                "Market API request timed out."
            )

        except requests.exceptions.RequestException as e:

            raise RuntimeError(
                f"Market API request failed: {str(e)}"
            )

        except ValueError:

            raise RuntimeError(
                "Market API returned invalid JSON."
            )

        records = data.get(
            "records",
            []
        )

        return [

            self._clean_record(
                record
            )

            for record in records

        ]

    # =====================================================
    # CLEAN GOVERNMENT RECORD
    # =====================================================

    def _clean_record(
        self,
        record: Dict
    ) -> Dict:

        return {

            "state":
                str(
                    record.get(
                        "state",
                        ""
                    )
                ).strip(),

            "district":
                str(
                    record.get(
                        "district",
                        ""
                    )
                ).strip(),

            "market":
                str(
                    record.get(
                        "market",
                        ""
                    )
                ).strip(),

            "crop":
                str(
                    record.get(
                        "commodity",
                        ""
                    )
                ).strip(),

            "variety":
                str(
                    record.get(
                        "variety",
                        ""
                    )
                ).strip(),

            "grade":
                str(
                    record.get(
                        "grade",
                        ""
                    )
                ).strip(),

            "arrival_date":
                str(
                    record.get(
                        "arrival_date",
                        ""
                    )
                ).strip(),

            "min_price":
                self._to_float(
                    record.get(
                        "min_price"
                    )
                ),

            "max_price":
                self._to_float(
                    record.get(
                        "max_price"
                    )
                ),

            "modal_price":
                self._to_float(
                    record.get(
                        "modal_price"
                    )
                ),

            "arrival_quantity":
                self._to_float(
                    record.get(
                        "arrival_quantity",
                        0
                    )
                )

        }

    # =====================================================
    # FLOAT CONVERSION
    # =====================================================

    def _to_float(
        self,
        value
    ) -> float:

        if value is None:

            return 0.0

        try:

            if isinstance(
                value,
                str
            ):

                value = (
                    value
                    .replace(
                        ",",
                        ""
                    )
                    .strip()
                )

            return float(value)

        except (
            TypeError,
            ValueError
        ):

            return 0.0

    # =====================================================
    # DATE PARSER
    # =====================================================

    def _date_sort_value(
        self,
        date_string: Optional[str]
    ):

        if not date_string:

            return datetime.min

        formats = [

            "%d/%m/%Y",

            "%Y-%m-%d",

            "%d-%m-%Y"

        ]

        for date_format in formats:

            try:

                return datetime.strptime(
                    date_string,
                    date_format
                )

            except ValueError:

                continue

        return datetime.min