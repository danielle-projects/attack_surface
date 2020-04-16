import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from service.routes import configure_routes


app = Flask(__name__)
input_file_path = 'data/input-0.json'
configure_routes(app, input_file_path=input_file_path)

if __name__ == '__main__':
    app.run(debug=True)

