import numpy as np
from flask import Flask, render_template, request
from processing import process, preprocess

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    # Значения по умолчанию
    IW = 45
    IF = 140
    VW = 8.5
    FP = 78

    message = ''

    if request.method == "POST":
        # Получаем значения, введённые пользователем
        IW = request.form.get("IW", 45)
        IF = request.form.get("IF", 140)
        VW = request.form.get("VW", 8.5)
        FP = request.form.get("FP", 78)



        data = np.array([[VW],
                         [IW],
                         [IF],
                         [FP],
                         ])
        data = data.reshape(1,-1)

        # Обрабатываем данные
        scaled_data = preprocess(data)


        # считаем показатели


        depth, width = process(scaled_data)
        depth = round(depth, 3)
        width = round(width, 3)


        # Сообщение с результатом расчета
        message = f"Глубина шва {depth} и ширина шва {width}"

    # Передаем все переменные в шаблон для отображения
    return render_template("index.html",
                           IW=IW,
                           IF=IF,
                           VW=VW,
                           FP=FP,
                           message=message)


if __name__ == '__main__':
    app.run()
