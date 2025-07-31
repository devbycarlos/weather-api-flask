#Weather App - API w/ Flask
from dotenv import load_dotenv
from flask import Flask
from routes import weather_bp

import os

load_dotenv()

app = Flask(__name__)

@app.template_filter("datetimeformat")
def datetimeformat(value, format='%B %d, %Y'):
    from datetime import datetime
    return datetime.fromtimestamp(value).strftime(' %B %d, %Y %a')

app.register_blueprint(weather_bp)



if __name__ == '__main__':
    app.run(debug=True)


