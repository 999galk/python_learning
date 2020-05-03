from flask import Flask, render_template

from views.items import item_blueprint
from views.alerts import alert_blueprint

app = Flask(__name__)
app.register_blueprint(item_blueprint, url_prefix='/items')
app.register_blueprint(alert_blueprint, url_prefix='/alerts')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__ ':
    app.run(port=4996,debug=True)