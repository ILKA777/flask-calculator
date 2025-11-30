from flask import Flask
from flask import request, jsonify

app = Flask(__name__)


@app.route('/calculate', methods=['GET'])
def calculate():
    try:
        # Получаем параметры
        a = request.args.get('a')
        b = request.args.get('b')
        operator = request.args.get('operator')

        # Проверяем наличие параметров
        if not all([a, b, operator]):
            raise ValueError("Отсутствуют параметры: a, b или operator")

        # Парсим числа
        try:
            a = float(a)
            b = float(b)
        except (TypeError, ValueError):
            raise TypeError("Параметры a и b должны быть числами")

        # Выполняем операцию
        if operator == '+':
            result = a + b
        elif operator == '-':
            result = a - b
        elif operator == '*':
            result = a * b
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Деление на ноль невозможно")
            result = a / b
        else:
            raise ValueError(f"Неподдерживаемый оператор: {operator}. Допустимо: +, -, *, /")

        return jsonify({
            "a": a,
            "b": b,
            "operator": operator,
            "result": result
        })

    except (ValueError, TypeError, ZeroDivisionError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Внутренняя ошибка: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)