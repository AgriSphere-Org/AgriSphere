import logging
from typing import Optional

from agents.climate_intelligence_agent import ClimateAgent
from agents.crop_planning_agent import CropPlanningAgent
from agents.crop_health_agent import CropHealthAgent
from agents.market_agent import MarketAgent
from agents.government_scheme_agent import GovernmentSchemeAgent
from agents.knowledge_agent import KnowledgeAgent


logger = logging.getLogger(__name__)


class AgriSphereOrchestrator:

    def __init__(self):

        self.climate_agent = ClimateAgent()
        self.crop_planning_agent = CropPlanningAgent()
        self.crop_health_agent = CropHealthAgent()
        self.market_agent = MarketAgent()
        self.scheme_agent = GovernmentSchemeAgent()
        self.knowledge_agent = KnowledgeAgent()

    def run(
        self,
        city: str,
        soil_ph: float,
        crop_image_path: str,
        state: str,
        district: str,
        farmer_category: str,
        farm_size: float,
        irrigation: str,
        gender: str,
        age: int,
        question: Optional[str] = None,
    ):

        try:

            # ======================================================
            # STEP 1: CLIMATE INTELLIGENCE
            # ======================================================

            logger.info("Running Climate Agent")

            climate = self.climate_agent.get_climate(city)

            # ======================================================
            # STEP 2: CROP PLANNING
            # ======================================================

            logger.info("Running Crop Planning Agent")

            crop_plan = self.crop_planning_agent.recommend_crop(
                temperature=climate["temperature"],
                humidity=climate["humidity"],
                rainfall=climate["rainfall"],
                soil_ph=soil_ph,
            )

            # ======================================================
            # STEP 3: CROP HEALTH
            # ======================================================

            logger.info("Running Crop Health Agent")

            crop_health = self.crop_health_agent.analyze_crop(
                crop=crop_plan["crop"],
                image_path=crop_image_path,
            )

            # ======================================================
            # STEP 4: MARKET INTELLIGENCE
            # ======================================================

            logger.info("Running Market Agent")

            market = self.market_agent.analyze_market(
                crop=crop_plan["crop"],
                state=state,
                district=district,
            )

            # ======================================================
            # STEP 5: GOVERNMENT SCHEMES
            # ======================================================

            logger.info("Running Government Scheme Agent")

            schemes = self.scheme_agent.recommend_schemes(
                state=state,
                farmer_category=farmer_category,
                farm_size=farm_size,
                crop=crop_plan["crop"],
                irrigation=irrigation,
                gender=gender,
                age=age,
            )

            # ======================================================
            # STEP 6: KNOWLEDGE AGENT
            # ======================================================

            knowledge = None

            if question:

                logger.info("Running Knowledge Agent")

                knowledge = self.knowledge_agent.ask(question)

            # ======================================================
            # FINAL RESPONSE
            # ======================================================

            return {
                "success": True,

                "climate": climate,

                "crop_plan": crop_plan,

                "crop_health": crop_health,

                "market": market,

                "government_schemes": schemes,

                "knowledge": knowledge,
            }

        except Exception as e:

            logger.exception("Pipeline Failed")

            return {
                "success": False,
                "error": str(e),
            }