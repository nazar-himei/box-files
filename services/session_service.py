from application import db


class SessionService:
    """
    Session Manager provide function work with database
    """

    # Add model to database
    @staticmethod
    def add_model(model):
        SessionService.get_session().add(model)
        SessionService.save_change()

    # Update current model in database
    @staticmethod
    def update_model(model):
        SessionService.get_session().update(model)
        SessionService.save_change()

    # Delete model in database
    @staticmethod
    def delete_model(model):
        SessionService.get_session().delete(model)
        SessionService.save_change()

    # Get current db session
    @staticmethod
    def get_session():
        return db.session

    # Save change in database
    @staticmethod
    def save_change():
        SessionService.get_session().commit()

    # Create database
    @staticmethod
    def create_db():
        db.create_all()

    # Drop current database
    @staticmethod
    def drop_db():
        db.drop_all()
