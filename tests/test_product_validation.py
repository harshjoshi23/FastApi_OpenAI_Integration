"""Invalid product inputs must not reach the paid generation boundary."""
import importlib
from pathlib import Path
import sys
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.mark.parametrize('payload', [
    {'name': '', 'notes': ''},
    {'name': '   \t', 'notes': 'details'},
    {'name': 'x' * 201, 'notes': ''},
    {'name': 'Book', 'notes': 'x' * 4001},
])
def test_invalid_product_never_calls_provider(payload):
    main = importlib.import_module('App.main')
    with patch.object(main, 'generate_description') as generate:
        response = TestClient(main.app).post('/product_description', json=payload)
    assert response.status_code == 422
    generate.assert_not_called()


def test_trimmed_product_accepts_documented_limits():
    main = importlib.import_module('App.main')
    with patch.object(main, 'generate_description', return_value='Description') as generate:
        response = TestClient(main.app).post('/product_description', json={'name': ' ' + 'x' * 200 + ' ', 'notes': ' ' + 'y' * 4000 + ' '})
    assert response.status_code == 200
    generate.assert_called_once_with('Product name: ' + 'x' * 200 + ', Notes: ' + 'y' * 4000)
