"""Order validation without provider credentials or network calls."""

import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient


class OrderValidationTest(unittest.TestCase):
    def setUp(self):
        provider = types.ModuleType("utils")
        provider.generate_description = lambda prompt: "test description"
        provider.DescriptionNotConfigured = type("DescriptionNotConfigured", (RuntimeError,), {})
        spec = importlib.util.spec_from_file_location(
            "order_api", Path(__file__).resolve().parents[1] / "App" / "main.py"
        )
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"utils": provider}):
            spec.loader.exec_module(module)
        self.client = TestClient(module.app)

    def test_both_order_routes_reject_nonpositive_quantities(self):
        for units in (0, -1):
            with self.subTest(units=units):
                query = self.client.post("/orders", params={"product": "book", "units": units})
                body = self.client.post("/orders_pydantic", json={"product": "book", "units": units})
                self.assertEqual(query.status_code, 422)
                self.assertEqual(body.status_code, 422)

    def test_positive_orders_preserve_success_response(self):
        for response in (
            self.client.post("/orders", params={"product": "book", "units": 2}),
            self.client.post("/orders_pydantic", json={"product": "book", "units": 2}),
        ):
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Order for 2 units of book placed successfully."})
