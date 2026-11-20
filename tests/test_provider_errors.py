"""Provider failures use safe HTTP responses without contacting OpenAI."""
import importlib
import sys
from pathlib import Path
from unittest.mock import patch

import httpx
import openai
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.mark.parametrize("kind,upstream,status", [
    (openai.APITimeoutError, None, 504),
    (openai.APIConnectionError, None, 503),
    (openai.RateLimitError, 429, 503),
    (openai.AuthenticationError, 401, 503),
    (openai.PermissionDeniedError, 403, 503),
    (openai.BadRequestError, 400, 502),
    (openai.InternalServerError, 500, 502),
])
def test_provider_failure_is_safe_and_client_closes(kind, upstream, status):
    main = importlib.import_module("App.main")
    request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
    if upstream is None:
        error = kind(request=request)
    else:
        error = kind("sensitive provider detail", response=httpx.Response(upstream, request=request), body=None)
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}), patch("openai.OpenAI") as constructor:
        provider = constructor.return_value.__enter__.return_value
        provider.chat.completions.create.side_effect = error
        response = TestClient(main.app).post("/product_description", json={"name": "Book", "notes": "Private notes"})
        assert response.status_code == status
        assert "sensitive" not in response.text
        assert "Private notes" not in response.text
        constructor.assert_called_once_with(api_key="test-key", timeout=20.0, max_retries=0)
        constructor.return_value.__exit__.assert_called_once()
