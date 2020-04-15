from flask import Flask
from flask_caching import Cache
from service.routes import configure_routes


app = Flask(__name__)
configure_routes(app)
config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)

cache = Cache(app)
cache.set('request_count', 0)
cache.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

