from .pricing_service import PricingService


class CostService:

    def calculate(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:

        return PricingService.calculate(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )