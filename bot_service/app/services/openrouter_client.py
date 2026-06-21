# Реализация обращения к OpenRouter через httpx
import httpx
from app.core.config import settings

class OpenRouterClientError(Exception):
    """Базовое исключение для ошибок API OpenRouter"""
    pass

class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL.rstrip("/")
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL

    async def get_completion(self, prompt: str) -> str:
        """Отправляет запрос в OpenRouter и возвращает текст ответа модели"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://example.com",
            "X-Title": "Bot Service"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=60.0
                )

                if response.status_code != 200:
                    raise OpenRouterClientError(
                        f"OpenRouter вернул ошибку {response.status_code}: {response.text}"
                    )

                data = response.json()
                return data["choices"][0]["message"]["content"]

            except httpx.RequestError as exc:
                raise OpenRouterClientError(f"Ошибка сети при запросе к OpenRouter: {exc}")
            except (KeyError, IndexType) as exc:
                raise OpenRouterClientError(f"Некорректный формат ответа от OpenRouter: {exc}")
