from models.file_box_model import FileBoxModel
from services.session_service import SessionService


class FileBoxRepository:
    @staticmethod
    def get_filebox_model(user_id):
        return FileBoxModel.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_file_model(user_id, file_id):
        file_box = FileBoxRepository.get_filebox_model(user_id)
        if file_box is None:
            return None

        for file in file_box.files:
            if file.id == file_id:
                return file

        return None

    @staticmethod
    def init_files_box(file_model, user_id):
        file_box = FileBoxModel(user_id=user_id)
        file_box.files.append(file_model)
        SessionService.add_model(file_box)

    @staticmethod
    def add_file(file_user_model):
        SessionService.add_model(file_user_model)

    @staticmethod
    def delete_file(file_model):
        SessionService.delete_model(file_model)

    @staticmethod
    def save_file():
        SessionService.get_session().commit()
