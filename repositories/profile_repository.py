from services.session_service import SessionManager
from models.user_model import UserModel
from datetime import datetime


class ProfileRepository:

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_user(user_id=None, user_email=None):
        query = UserModel.query

        if user_id is not None:
            return query.filter_by(id=user_id).first()

        return query.filter_by(email=user_email).first()

    @staticmethod
    def add_user(user_model):
        SessionManager.init_db()
        SessionManager.add_model(user_model)

    @staticmethod
    def delete_user(user_model):
        SessionManager.delete_model(user_model)

    @staticmethod
    def update_status_active_user(user_email):
        user = ProfileRepository.get_user(user_email=user_email)
        user.last_login_date = datetime.utcnow()
        SessionManager.save_change()
