def register_routes(app):
    """
    Register routes with blueprint and namespace
    """
    from routes.auth_route import auth
    from routes.filebox_route import filebox

    app.register_blueprint(auth)
    app.register_blueprint(filebox)
