from application import db

""" Session Manager """


class SessionManager:

    @staticmethod
    def add_model(model):
        SessionManager.get_session().add(model)
        SessionManager.save_change()

    @staticmethod
    def update_model(model):
        SessionManager.get_session().update(model)
        SessionManager.save_change()

    @staticmethod
    def delete_model(model):
        SessionManager.get_session().delete(model)
        SessionManager.save_change()

    @staticmethod
    def get_session():
        return db.session

    @staticmethod
    def save_change():
        SessionManager.get_session().commit()

    @staticmethod
    def init_db():
        db.create_all()

    @staticmethod
    def drop_db():
        db.drop_all()
