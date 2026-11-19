"""Startup and provider configuration are tested without real API calls."""

import importlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class StartupTest(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict("os.environ", {"OPENAI_API_KEY": ""})
        self.env.start()
        self.addCleanup(self.env.stop)
        with patch("dotenv.load_dotenv"), patch("openai.OpenAI") as constructor:
            self.utils = importlib.import_module("App.utils")
            importlib.reload(self.utils)
            self.main = importlib.import_module("App.main")
            importlib.reload(self.main)
            constructor.assert_not_called()
        self.client = TestClient(self.main.app)

    def test_health_docs_and_orders_work_without_credentials(self):
        self.assertEqual(self.client.get("/ok").status_code, 200)
        self.assertEqual(self.client.get("/openapi.json").status_code, 200)
        self.assertEqual(self.client.post("/orders", params={"product": "book", "units": 1}).status_code, 200)

    def test_generation_without_key_returns_service_unavailable(self):
        with patch("openai.OpenAI") as constructor:
            response = self.client.post("/product_description", json={"name": "Book", "notes": "Hardcover"})
            self.assertEqual(response.status_code, 503)
            constructor.assert_not_called()

    def test_configured_generation_constructs_and_closes_client(self):
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            with patch("openai.OpenAI") as constructor:
                client = constructor.return_value.__enter__.return_value
                client.chat.completions.create.return_value.choices = [
                    MagicMock(message=MagicMock(content="Description"))
                ]
                response = self.client.post("/product_description", json={"name": "Book", "notes": "Hardcover"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"product_description": "Description"})
                constructor.assert_called_once_with(api_key="test-key")
                constructor.return_value.__exit__.assert_called_once()
