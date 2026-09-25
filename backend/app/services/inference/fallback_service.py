from .model_registry import ModelRegistry


class FallbackService:

    def __init__(
        self,
        model_registry: ModelRegistry,
    ):
        self.model_registry = model_registry

    def get_fallback_chain(
        self,
        selected_model: str,
    ) -> list[str]:

        models = (
            self.model_registry
            .get_generation_model_names()
        )

        if not models:
            return []

        if selected_model not in models:
            return models

        selected_index = models.index(
            selected_model
        )

        return models[selected_index:]

    def get_next_fallback(
        self,
        selected_model: str,
        failed_model: str,
    ) -> str | None:

        chain = self.get_fallback_chain(
            selected_model
        )

        if failed_model not in chain:
            return None

        failed_index = chain.index(
            failed_model
        )

        next_index = failed_index + 1

        if next_index >= len(chain):
            return None

        return chain[next_index]