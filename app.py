from flask import Flask, render_template, request, url_for
from processing import process, preprocess
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    # Значения по умолчанию
    IW = 45
    IF = 142
    VW = 8.5
    FP = 78
    message = None
    errors = []

    if request.method == "POST":
        # Очищаем сообщение перед новым расчетом
        message = ''
        # Получаем значения, введённые пользователем и преобразуем их в числа
        try:
            # Получаем значения, введённые пользователем
            IW = float(request.form.get("IW", 45))
            IF = float(request.form.get("IF", 142))
            VW = float(request.form.get("VW", 8.5))
            FP = float(request.form.get("FP", 78))

            # Проверяем, что значения корректны
            if IW < 43 or IW > 49:
                print("1")
                errors.append("Показатель IW должен быть положительным в интервале от 43.0 до 49.0")
            if IF < 141 or IF > 150:
                print("2")
                errors.append("Показатель IF должен быть положительным в интервале от 141.0 до 150.0")
            if VW < 4.5 or VW > 12.0:
                print("3")
                errors.append("Показатель VW должен быть положительным в интервале от 4.5 до 12.0")
            if FP < 50 or FP > 125:
                print("4")
                errors.append("Показатель FP должен быть положительным в интервале от 50.0 до 125.0")

            if errors:
                message = "<br>".join(errors)
            else:
                # Создание DataFrame
                data = pd.DataFrame({
                    'IW': [IW],
                    'IF': [IF],
                    'VW': [VW],
                    'FP': [FP],
                })

                # Обрабатываем данные
                scaled_data = preprocess(data)

                # # считаем показатели
                result = process(scaled_data)

                depth = round(result[0], 3)
                width = round(result[1], 3)

                # Сообщение с результатом расчета
                message = f"Глубина {depth} и ширина {width} сварного соединения"

        except ValueError:
            message = "Пожалуйста, введите корректные числовые значения."

    # Передаем все переменные в шаблон для отображения
    return render_template("index.html",
                           IW=IW,
                           IF=IF,
                           VW=VW,
                           FP=FP,
                           message=message)


if __name__ == '__main__':
    app.run()
