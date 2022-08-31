from application import db


class SessionManager:
    """ Session Manager """

    # Add model to database
    @staticmethod
    def add_model(model):
        SessionManager.get_session().add(model)
        SessionManager.save_change()

    # Update current model in database
    @staticmethod
    def update_model(model):
        SessionManager.get_session().update(model)
        SessionManager.save_change()

    # Delete model in database
    @staticmethod
    def delete_model(model):
        SessionManager.get_session().delete(model)
        SessionManager.save_change()

    # Get current db session
    @staticmethod
    def get_session():
        return db.session

    # Save change in database
    @staticmethod
    def save_change():
        SessionManager.get_session().commit()

    # Create database
    @staticmethod
    def init_db():
        db.create_all()

    # Drop current database
    @staticmethod
    def drop_db():
        db.drop_all()
