import asyncio

from google import genai

from ..config import settings
from .inference.model_registry import ModelRegistry


class EmbeddingService:

    def __init__(
        self,
        model_registry: ModelRegistry,
    ):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model_registry = model_registry

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        models = (
            self.model_registry
            .get_embedding_model_names()
        )

        if not models:
            raise RuntimeError(
                "No embedding models are available."
            )

        last_error = None

        for model_name in models:

            try:
                print(
                    f"Trying embedding model: "
                    f"{model_name}"
                )

                response = await asyncio.to_thread(
                    self.client.models.embed_content,
                    model=model_name,
                    contents=text,
                )

                embedding = response.embeddings[0].values

                print(
                    f"Embedding success: "
                    f"{model_name}"
                )

                return list(embedding)

            except Exception as error:

                last_error = error

                print(
                    f"Embedding model failed: "
                    f"{model_name}"
                )

                print(error)

                continue

        if last_error:
            raise last_error

        raise RuntimeError(
            "All embedding models failed."
        )