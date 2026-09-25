from dataclasses import dataclass

from google import genai

from ...config import settings


@dataclass
class ModelInfo:
    name: str
    display_name: str | None = None


class ModelRegistry:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self._generation_models: list[ModelInfo] = []
        self._embedding_models: list[ModelInfo] = []

        self._discovered = False

    # =========================================================
    # DISCOVER ALL MODELS
    # =========================================================

    def discover_models(self) -> None:

        generation_models = []
        embedding_models = []

        for model in self.client.models.list():

            if not model.name:
                continue

            clean_name = model.name.removeprefix("models/")

            info = ModelInfo(
                name=clean_name,
                display_name=getattr(
                    model,
                    "display_name",
                    None,
                ),
            )

            if self._is_embedding_model(clean_name):
                embedding_models.append(info)

            elif self._is_generation_model(clean_name):
                generation_models.append(info)

        self._generation_models = self._rank_generation_models(
            generation_models
        )

        self._embedding_models = self._rank_embedding_models(
            embedding_models
        )

        self._discovered = True

    # =========================================================
    # GENERATION MODELS
    # =========================================================

    def get_generation_models(self) -> list[ModelInfo]:

        if not self._discovered:
            self.discover_models()

        return self._generation_models

    def get_generation_model_names(self) -> list[str]:

        return [
            model.name
            for model in self.get_generation_models()
        ]

    # =========================================================
    # EMBEDDING MODELS
    # =========================================================

    def get_embedding_models(self) -> list[ModelInfo]:

        if not self._discovered:
            self.discover_models()

        return self._embedding_models

    def get_embedding_model_names(self) -> list[str]:

        return [
            model.name
            for model in self.get_embedding_models()
        ]

    # =========================================================
    # GENERATION MODEL FILTER
    # =========================================================

    def _is_generation_model(
        self,
        model_name: str,
    ) -> bool:

        name = model_name.lower()

        excluded_terms = (
            "embedding",
            "tts",
            "transcribe",
            "live",
            "image",
            "veo",
            "lyria",
            "robotics",
            "computer-use",
            "deep-research",
        )

        if any(
            term in name
            for term in excluded_terms
        ):
            return False

        if name == "aqa":
            return False

        return (
            name.startswith("gemini-")
            or name.startswith("gemma-")
        )

    # =========================================================
    # EMBEDDING MODEL FILTER
    # =========================================================

    def _is_embedding_model(
        self,
        model_name: str,
    ) -> bool:

        return "embedding" in model_name.lower()

    # =========================================================
    # GENERATION MODEL RANKING
    # =========================================================

    def _rank_generation_models(
        self,
        models: list[ModelInfo],
    ) -> list[ModelInfo]:

        def score(model: ModelInfo):

            name = model.name.lower()

            # Lower score = tried earlier.

            # Lightweight models first
            if "flash-lite" in name:
                base = 10

            # Normal Flash models
            elif "flash" in name:
                base = 20

            # Pro models
            elif "pro" in name:
                base = 30

            # Gemma models
            elif "gemma" in name:
                base = 40

            else:
                base = 50

            # Prefer stable-looking models before preview models.
            if "preview" in name:
                preview_penalty = 5
            else:
                preview_penalty = 0

            return (
                base + preview_penalty,
                name,
            )

        return sorted(
            models,
            key=score,
        )

    # =========================================================
    # EMBEDDING MODEL RANKING
    # =========================================================

    def _rank_embedding_models(
        self,
        models: list[ModelInfo],
    ) -> list[ModelInfo]:

        def score(model: ModelInfo):

            name = model.name.lower()

            if "embedding-2" in name:
                base = 10

            elif "embedding-001" in name:
                base = 20

            else:
                base = 30

            if "preview" in name:
                preview_penalty = 5
            else:
                preview_penalty = 0

            return (
                base + preview_penalty,
                name,
            )

        return sorted(
            models,
            key=score,
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self) -> None:

        self._generation_models = []
        self._embedding_models = []
        self._discovered = False

        self.discover_models()