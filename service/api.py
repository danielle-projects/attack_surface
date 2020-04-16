from argparse import ArgumentParser
from flask import Flask

from service.routes import configure_routes


def create_attack_surface_app(input_file_path):
    app = Flask(__name__)
    app.config['INPUT_FILE_PATH'] = input_file_path
    configure_routes(app)
    return app


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input_file_path',
                        help='path of vm/firewall input file',
                        default='data/input-0.json')
    args = parser.parse_args()
    attack_surface_app = create_attack_surface_app(args.input_file_path)
    attack_surface_app.run(debug=True)

