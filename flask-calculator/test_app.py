import pytest
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(__file__))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_calculate_success(client):
    """Тест успешных операций"""
    test_cases = [
        ('5', '3', '%2B', 8),  # + encoded
        ('10', '4', '-', 6),
        ('3', '7', '*', 21),
        ('15', '3', '/', 5),
        ('2.5', '1.5', '%2B', 4.0),  # + encoded
        ('-5', '3', '-', -8)
    ]

    for a, b, op, expected in test_cases:
        response = client.get(f'/calculate?a={a}&b={b}&operator={op}')
        assert response.status_code == 200, f"Failed for {a} {op} {b}: {response.get_json()}"
        assert response.json['result'] == expected


def test_missing_parameters(client):
    """Тест отсутствия параметров"""
    response = client.get('/calculate?a=5&b=3')
    assert response.status_code == 400
    error_text = response.json['error']

    # Проверяем конкретную ошибку из нашего кода
    expected_errors = [
        "Все параметры (a, b, operator) обязательны",
        "Отсутствуют параметры: a, b или operator",
        "обязательны"
    ]

    # Тест пройдет если любая из этих фраз есть в ошибке
    assert any(expected in error_text for expected in expected_errors), f"Unexpected error: {error_text}"


def test_invalid_numbers(client):
    """Тест некорректных чисел"""
    response = client.get('/calculate?a=abc&b=3&operator=%2B')
    assert response.status_code == 400
    error_text = response.json['error']
    # Проверяем, что ошибка связана с числами (любое из этих слов)
    assert any(word in error_text for word in ['числ', 'number', 'float', 'convert'])

def test_division_by_zero(client):
    """Тест деления на ноль"""
    response = client.get('/calculate?a=5&b=0&operator=/')
    assert response.status_code == 400
    assert 'Деление на ноль' in response.json['error']


def test_invalid_operator(client):
    """Тест некорректного оператора"""
    response = client.get('/calculate?a=5&b=3&operator=^')
    assert response.status_code == 400
    assert 'Неподдерживаемый оператор' in response.json['error']