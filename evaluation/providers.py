"""Model providers (Google Gemini and OpenAI-compatible) for the CogGym harness."""

from __future__ import annotations

import base64
import os
import re
import time
from typing import Any


class GeminiProvider:
    """Google Gemini provider. Supports API key or Vertex AI auth."""

    name = "google"

    def __init__(self, api_key: str | None = None, vertexai: bool = False,
                 project: str | None = None, location: str = "us-central1"):
        from google import genai

        if vertexai:
            project_id = project or os.environ.get("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise ValueError(
                    "Set GOOGLE_CLOUD_PROJECT or pass project=... when using Vertex AI"
                )
            self.client = genai.Client(
                vertexai=True,
                project=project_id,
                location=location,
            )
        else:
            self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError("Set GOOGLE_API_KEY env var or use --vertexai")
            self.client = genai.Client(api_key=self.api_key)

    def complete(
        self,
        system: str,
        messages: list[dict[str, Any]],
        model: str,
        temperature: float = 1.0,
        max_tokens: int = 1024,
    ) -> str:
        resp = self._call_api(system, messages, model, temperature, max_tokens)
        return resp.text or ""

    def complete_with_metadata(
        self,
        system: str,
        messages: list[dict[str, Any]],
        model: str,
        temperature: float = 1.0,
        max_tokens: int = 1024,
    ) -> dict[str, Any]:
        resp = self._call_api(system, messages, model, temperature, max_tokens)

        text = resp.text or ""

        # Extract reasoning/thinking from candidates
        reasoning = None
        if hasattr(resp, "candidates") and resp.candidates:
            thought_parts = [
                part.text for part in resp.candidates[0].content.parts
                if getattr(part, "thought", False) and part.text
            ]
            if thought_parts:
                reasoning = "\n".join(thought_parts)

        # Extract token usage
        token_usage = None
        if hasattr(resp, "usage_metadata") and resp.usage_metadata:
            um = resp.usage_metadata
            token_usage = {
                "input_tokens": getattr(um, "prompt_token_count", None),
                "output_tokens": getattr(um, "candidates_token_count", None),
                "thinking_tokens": getattr(um, "thoughts_token_count", None),
                "total_tokens": getattr(um, "total_token_count", None),
            }

        return {"text": text, "reasoning": reasoning, "token_usage": token_usage}

    # ── Internal ────────────────────────────────────────────────────────

    def _call_api(self, system, messages, model, temperature, max_tokens):
        from google.genai import types

        contents = self._build_contents(messages)
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            system_instruction=system,
            thinking_config=types.ThinkingConfig(
                thinking_budget=8192,
                include_thoughts=True,
            ),
        )
        return self.client.models.generate_content(
            model=model, contents=contents, config=config,
        )

    def _build_contents(self, messages: list[dict[str, Any]]) -> list[Any]:
        from google.genai import types

        contents = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            parts = self._parse_content(msg["content"])
            contents.append(types.Content(role=role, parts=parts))
        return contents

    def _parse_content(self, content: str | list[dict[str, Any]]) -> list[Any]:
        from google.genai import types

        if isinstance(content, str):
            return [types.Part.from_text(text=content)]

        parts = []
        for item in content:
            item_type = item.get("type", "")

            if item_type == "text":
                parts.append(types.Part.from_text(text=item.get("text", "")))

            elif item_type == "image":
                source = item.get("source", {})
                if source.get("type") == "base64":
                    image_bytes = base64.b64decode(source["data"])
                    parts.append(
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=source.get("media_type", "image/png"),
                        )
                    )

            elif item_type == "video":
                # Upload video via File API (for real-time calls)
                video_path = item.get("path", "")
                if video_path and os.path.exists(video_path):
                    uploaded = self.client.files.upload(file=video_path)
                    while uploaded.state == "PROCESSING":
                        time.sleep(2)
                        uploaded = self.client.files.get(name=uploaded.name)
                    if uploaded.state == "ACTIVE":
                        parts.append(
                            types.Part(
                                file_data=types.FileData(
                                    file_uri=uploaded.uri,
                                    mime_type=uploaded.mime_type,
                                )
                            )
                        )

            elif item_type == "audio":
                audio_path = item.get("path", "")
                if audio_path and os.path.exists(audio_path):
                    with open(audio_path, "rb") as audio_file:
                        parts.append(
                            types.Part.from_bytes(
                                data=audio_file.read(),
                                mime_type=item.get("mime_type", "audio/mpeg"),
                            )
                        )

            elif item_type == "gcs_file":
                # Reference file by GCS URI (for batch calls)
                parts.append(
                    types.Part(
                        file_data=types.FileData(
                            file_uri=item["uri"],
                            mime_type=item.get("mime_type", "video/mp4"),
                        )
                    )
                )
        return parts


class OpenAIProvider:
    """OpenAI Chat Completions provider (text and image experiments).

    Reads OPENAI_API_KEY. Set OPENAI_BASE_URL to use any OpenAI-compatible
    endpoint (for example OpenRouter). Video and audio stimuli are not supported
    by this provider; use GeminiProvider for those experiments.
    """

    name = "openai"

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        from openai import OpenAI

        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Set the OPENAI_API_KEY env var")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url or os.environ.get("OPENAI_BASE_URL") or None,
        )

    def complete(self, system, messages, model, temperature=1.0, max_tokens=1024) -> str:
        return self.complete_with_metadata(system, messages, model, temperature, max_tokens)["text"]

    def complete_with_metadata(
        self,
        system: str,
        messages: list[dict[str, Any]],
        model: str,
        temperature: float = 1.0,
        max_tokens: int = 1024,
    ) -> dict[str, Any]:
        chat = [{"role": "system", "content": system}] if system else []
        for msg in messages:
            role = "assistant" if msg["role"] == "assistant" else "user"
            chat.append({"role": role, "content": self._parse_content(msg["content"])})
        resp = self.client.chat.completions.create(
            model=model,
            messages=chat,
            temperature=temperature,
            max_completion_tokens=max_tokens,
        )
        text = resp.choices[0].message.content or ""
        token_usage = None
        if resp.usage is not None:
            details = getattr(resp.usage, "completion_tokens_details", None)
            token_usage = {
                "input_tokens": resp.usage.prompt_tokens,
                "output_tokens": resp.usage.completion_tokens,
                "thinking_tokens": getattr(details, "reasoning_tokens", None),
                "total_tokens": resp.usage.total_tokens,
            }
        return {"text": text, "reasoning": None, "token_usage": token_usage}

    @staticmethod
    def _parse_content(content: str | list[dict[str, Any]]) -> str | list[dict[str, Any]]:
        if isinstance(content, str):
            return content
        parts: list[dict[str, Any]] = []
        for item in content:
            item_type = item.get("type", "")
            if item_type == "text":
                parts.append({"type": "text", "text": item.get("text", "")})
            elif item_type == "image":
                source = item.get("source", {})
                if source.get("type") != "base64":
                    raise ValueError("OpenAIProvider only supports base64 image sources")
                url = f"data:{source.get('media_type', 'image/png')};base64,{source['data']}"
                parts.append({"type": "image_url", "image_url": {"url": url}})
            else:
                raise NotImplementedError(
                    f"OpenAIProvider does not support {item_type!r} stimuli; "
                    "use --provider gemini for video and audio experiments"
                )
        return parts


def make_provider(provider: str, model: str) -> Any:
    """Return a provider instance. provider is 'gemini', 'openai', or 'auto'."""
    if provider == "auto":
        provider = "gemini" if model.startswith("gemini") else "openai"
    if provider == "gemini":
        return GeminiProvider()
    if provider == "openai":
        return OpenAIProvider()
    raise ValueError(f"Unknown provider {provider!r}")


def call_with_retry(
    provider: Any,
    system: str,
    messages: list[dict[str, Any]],
    model: str,
    temperature: float = 1.0,
    max_tokens: int = 1024,
    max_retries: int = 3,
    backoff: float = 2.0,
    with_metadata: bool = False,
) -> str | dict[str, Any]:
    """Call provider with exponential backoff on rate-limit errors."""
    method = provider.complete_with_metadata if with_metadata else provider.complete
    for attempt in range(max_retries):
        try:
            return method(
                system=system, messages=messages, model=model,
                temperature=temperature, max_tokens=max_tokens,
            )
        except Exception as e:
            err_str = str(e).lower()
            is_retryable = any(
                kw in err_str
                for kw in ("rate_limit", "rate limit", "429",
                           "overloaded", "503", "resource exhausted", "quota")
            )
            if is_retryable and attempt < max_retries - 1:
                wait = backoff ** (attempt + 1)
                print(f"  Rate limited, retrying in {wait:.0f}s... (attempt {attempt + 2}/{max_retries})")
                time.sleep(wait)
            else:
                raise
    return "" if not with_metadata else {"text": "", "reasoning": None, "token_usage": None}
