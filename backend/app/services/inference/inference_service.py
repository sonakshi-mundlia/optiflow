import asyncio
import time

from google import genai
from google.genai import errors
from google.genai import types

from ...config import settings
from .model_registry import ModelRegistry
from .fallback_service import FallbackService


class InferenceService:

    def __init__(
        self,
        model_registry: ModelRegistry,
    ):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model_registry = model_registry

        self.fallback_service = FallbackService(
            model_registry
        )

        self.semaphore = asyncio.Semaphore(
            settings.MAX_CONCURRENT_INFERENCE
        )

    async def generate(
        self,
        query: str,
        selected_model: str,
    ):

        fallback_chain = (
            self.fallback_service
            .get_fallback_chain(
                selected_model
            )
        )

        if not fallback_chain:

            raise RuntimeError(
                "No generation models are available."
            )

        print(
            f"Selected model: {selected_model}"
        )

        print(
            f"Fallback chain: {fallback_chain}"
        )

        last_error = None

        async with self.semaphore:

            for model_name in fallback_chain:

                print(
                    f"Trying model: {model_name}"
                )

                try:

                    start = time.perf_counter()

                    response = await asyncio.to_thread(
                        self.client.models.generate_content,
                        model=model_name,
                        contents=query,
                        config=types.GenerateContentConfig(
                            temperature=0.2
                        ),
                    )

                    latency_ms = (
                        time.perf_counter()
                        - start
                    ) * 1000

                    usage = response.usage_metadata

                    input_tokens = (
                        getattr(
                            usage,
                            "prompt_token_count",
                            0,
                        )
                        or 0
                    )

                    output_tokens = (
                        getattr(
                            usage,
                            "candidates_token_count",
                            0,
                        )
                        or 0
                    )

                    print(
                        f"SUCCESS: {model_name}"
                    )

                    return {
                        "answer": response.text,
                        "model": model_name,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "latency_ms": latency_ms,
                        "fallback_used": (
                            model_name != selected_model
                        ),
                    }

                # =================================================
                # SERVER ERRORS
                # =================================================

                except errors.ServerError as error:

                    last_error = error

                    print(
                        f"SERVER ERROR: {model_name}"
                    )

                    print(
                        f"Status: {error.code}"
                    )

                    if error.code in {
                        429,
                        500,
                        502,
                        503,
                        504,
                    }:

                        print(
                            "Trying next model..."
                        )

                        await asyncio.sleep(0.5)

                        continue

                    raise

                # =================================================
                # CLIENT ERRORS
                # =================================================

                except errors.ClientError as error:

                    last_error = error

                    print(
                        f"CLIENT ERROR: {model_name}"
                    )

                    print(error)

                    # 404 can mean that the model is listed
                    # but unavailable for this API/project.
                    if error.code == 404:

                        print(
                            "Model unavailable. "
                            "Trying next model..."
                        )

                        continue

                    # Rate/quota related
                    if error.code == 429:

                        print(
                            "Model rate limited. "
                            "Trying next model..."
                        )

                        continue

                    raise

                # =================================================
                # UNEXPECTED ERROR
                # =================================================

                except Exception as error:

                    print(
                        f"Unexpected error "
                        f"from {model_name}: {error}"
                    )

                    raise

        if last_error:
            raise last_error

        raise RuntimeError(
            "All discovered Gemini generation "
            "models failed."
        )