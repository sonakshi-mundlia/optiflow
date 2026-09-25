from ..inference.model_registry import ModelRegistry


class RoutingService:

    def __init__(
        self,
        model_registry: ModelRegistry,
    ):
        self.model_registry = model_registry

    def select_model(
        self,
        complexity: str,
        router_score: float,
    ) -> str:

        models = (
            self.model_registry
            .get_generation_model_names()
        )

        if not models:
            raise RuntimeError(
                "No Gemini text-generation models "
                "are available."
            )

        # -----------------------------------------------------
        # LOW COMPLEXITY
        # -----------------------------------------------------

        if complexity == "low":

            index = 0

        # -----------------------------------------------------
        # MEDIUM COMPLEXITY
        # -----------------------------------------------------

        elif complexity == "medium":

            index = min(
                2,
                len(models) - 1,
            )

        # -----------------------------------------------------
        # HIGH COMPLEXITY
        # -----------------------------------------------------

        else:

            index = min(
                4,
                len(models) - 1,
            )

        return models[index]