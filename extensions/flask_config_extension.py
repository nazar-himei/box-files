from configs.config import Config


def flask_config(app, config: Config):
    """
    Default Flask configuration.
    """

    app.secret_key = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.JWT_REFRESH_TOKEN_EXPIRES


def flask_run(app, config: Config):
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT,
    )
