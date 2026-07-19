import logging
from typing import Optional

from agents.climate_intelligence_agent import ClimateAgent
from agents.crop_planning_agent import CropPlanningAgent
from agents.crop_health_agent import CropHealthAgent
from agents.market_agent import MarketAgent
from agents.government_scheme_agent import GovernmentSchemeAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.recommendation_agent import RecommendationAgent

logger = logging.getLogger(__name__)


class AgriSphereOrchestrator:

    def __init__(self):

        self.climate_agent = ClimateAgent()
        self.crop_planning_agent = CropPlanningAgent()
        self.crop_health_agent = CropHealthAgent()
        self.market_agent = MarketAgent()
        self.scheme_agent = GovernmentSchemeAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.recommendation_agent = RecommendationAgent()

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

            ###########################################################
            # STEP 1
            # Climate Intelligence
            ###########################################################

            logger.info("Running Climate Agent")

            climate = self.climate_agent.get_climate(city)

            ###########################################################
            # STEP 2
            # Crop Planning
            ###########################################################

            logger.info("Running Crop Planning Agent")

            crop_plan = self.crop_planning_agent.recommend_crop(
                temperature=climate["temperature"],
                humidity=climate["humidity"],
                rainfall=climate["rainfall"],
                soil_ph=soil_ph,
            )

            ###########################################################
            # STEP 3
            # Crop Health
            ###########################################################

            logger.info("Running Crop Health Agent")

            crop_health = self.crop_health_agent.analyze_crop(
                crop_image_path
            )

            ###########################################################
            # STEP 4
            # Market Intelligence
            ###########################################################

            logger.info("Running Market Agent")

            market = self.market_agent.analyze_market(
                crop=crop_plan["crop"],
                state=state,
                district=district,
            )

            ###########################################################
            # STEP 5
            # Government Schemes
            ###########################################################

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

            ###########################################################
            # STEP 6
            # Knowledge Agent (Optional)
            ###########################################################

            knowledge = None

            if question:

                logger.info("Running Knowledge Agent")

                knowledge = self.knowledge_agent.ask(question)

            ###########################################################
            # STEP 7
            # Final Recommendation
            ###########################################################

            logger.info("Running Recommendation Agent")

            recommendation = self.recommendation_agent.generate_recommendation(
                climate_data=climate,
                crop_plan=crop_plan,
                crop_health=crop_health,
                market_data=market,
                government_schemes=schemes,
            )

            ###########################################################
            # FINAL RESPONSE
            ###########################################################

            return {

                "success": True,

                "climate": climate,

                "crop_plan": crop_plan,

                "crop_health": crop_health,

                "market": market,

                "government_schemes": schemes,

                "knowledge": knowledge,

                "recommendation": recommendation,
            }

        except Exception as e:

            logger.exception("Pipeline Failed")

            return {

                "success": False,

                "error": str(e)
            }