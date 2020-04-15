from flask import Flask

from service.routes import configure_routes


app = Flask(__name__)
configure_routes(app, input_file_path='/home/danielle/MyProj/attack_surface/data/input-2.json')

if __name__ == '__main__':
    app.run(debug=True)

