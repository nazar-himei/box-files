from application import create_app
from extensions.flask_config_extension import flask_run

app = create_app()

if __name__ == '__main__':
    flask_run(app)
