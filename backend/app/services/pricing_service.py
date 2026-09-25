from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPricing:
    input_per_million: float
    output_per_million: float


class PricingService:

    # =========================================================
    # CURRENT STANDARD PAID-TIER PRICING
    # USD per 1 million tokens
    # =========================================================

    PRICING: dict[str, ModelPricing] = {

        # -----------------------------------------------------
        # Gemini 3.1 Flash-Lite
        # -----------------------------------------------------

        "gemini-3.1-flash-lite": ModelPricing(
            input_per_million=0.25,
            output_per_million=1.50,
        ),

        # -----------------------------------------------------
        # Gemini 3.5 Flash-Lite
        # -----------------------------------------------------

        "gemini-3.5-flash-lite": ModelPricing(
            input_per_million=0.30,
            output_per_million=2.50,
        ),

        # -----------------------------------------------------
        # Gemini 3.5 Flash
        # -----------------------------------------------------

        "gemini-3.5-flash": ModelPricing(
            input_per_million=1.50,
            output_per_million=9.00,
        ),

        # -----------------------------------------------------
        # Gemini 3.6 Flash
        # -----------------------------------------------------

        "gemini-3.6-flash": ModelPricing(
            input_per_million=0.75,
            output_per_million=3.75,
        ),

        # -----------------------------------------------------
        # Gemini 3.7 Flash
        # -----------------------------------------------------

        "gemini-3.7-flash": ModelPricing(
            input_per_million=0.75,
            output_per_million=3.75,
        ),

        # -----------------------------------------------------
        # Gemini 3.8 Flash
        # -----------------------------------------------------

        "gemini-3.8-flash": ModelPricing(
            input_per_million=0.75,
            output_per_million=3.75,
        ),

        # -----------------------------------------------------
        # Gemini 2.5 Flash-Lite
        # -----------------------------------------------------

        "gemini-2.5-flash-lite": ModelPricing(
            input_per_million=0.10,
            output_per_million=0.40,
        ),
    }

    # =========================================================
    # CALCULATE COST
    # =========================================================

    @classmethod
    def calculate(
        cls,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:

        model_name = model.removeprefix("models/")

        pricing = cls.PRICING.get(model_name)

        # -----------------------------------------------------
        # UNKNOWN MODEL
        # -----------------------------------------------------

        if pricing is None:
            return 0.0

        # -----------------------------------------------------
        # TOKEN COST
        # -----------------------------------------------------

        input_cost = (
            input_tokens / 1_000_000
        ) * pricing.input_per_million

        output_cost = (
            output_tokens / 1_000_000
        ) * pricing.output_per_million

        total_cost = input_cost + output_cost

        return round(total_cost, 8)

    # =========================================================
    # GET MODEL PRICING
    # =========================================================

    @classmethod
    def get_pricing(
        cls,
        model: str,
    ) -> ModelPricing | None:

        model_name = model.removeprefix("models/")

        return cls.PRICING.get(model_name)