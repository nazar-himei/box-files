from io import BytesIO

from models.file_box_model import FileUserModel, FileBoxModel
from repositories.file_box_repository import FileBoxRepository
from repositories.profile_repository import ProfileRepository
from schemas.file_schema import FileUserBase
from services.file_manager import FileManager


class FileBoxService:
    def __init__(self, request, user_email):
        self.request = request
        self.user_email = user_email
        self.files_byte_context = {}

    # Update file bytes to files_byte_context.
    def iterable_files_and_update_files_byte_context(self):
        files = self.request.files.values()

        for file in files:
            self.add_byte_to_files_byte_context(
                key=file.filename,
                file_byte=file.read()
            )
            file.close()

    # Add files byte to files_byte_context
    def add_byte_to_files_byte_context(self, key, file_byte):
        self.files_byte_context[key] = file_byte

    # Clean all files in files_bytes_context
    def clean_file_bytes_context(self):
        self.files_byte_context.clear()

    # Provide user information.
    def get_user(self):
        return ProfileRepository.get_user(user_email=self.user_email)

    def all_files(self):
        return FileBoxRepository.get_filebox_model(self.get_user().id)

    def get_detail_file(self, file_id):
        user = self.get_user()
        return FileBoxRepository.get_file_model(user.id, file_id)

    @staticmethod
    def parse_file_model_to_file_base(files_of_user):
        return FileUserBase(
            filename=files_of_user.filename,
            create_file=files_of_user.created_file_time,
            changed_file=files_of_user.changed_file_time,
            size_of_data=files_of_user.size_of_data,
            type_data=files_of_user.type_of_data,
            file_id=files_of_user.id
        )

    @staticmethod
    def to_file_model(file_manager, file_box_id=None):
        return FileUserModel(
            filename=file_manager.file.filename,
            data=file_manager.file_byte,
            data_base64=file_manager.encode_base64(),
            size_of_data=file_manager.get_size_of_file(),
            type_of_data=file_manager.get_type_of_file(),
            file_key=file_box_id
        )

    # Iterable model from storage and return json model.
    def iterable_element_is_filebox(self):
        filebox = self.all_files()
        files = []

        if filebox is not None:
            for file in filebox.files:
                file_base = self.parse_file_model_to_file_base(file).to_json()
                files.append(file_base)

        return files

    # Check current size of file.
    def is_valid_files(self):
        files = self.request.files.values()

        for file in files:
            file_byte = self.files_byte_context.get(file.filename)
            file_manager = FileManager(file=file, file_byte=file_byte)
            is_valid_file = file_manager.get_size_of_file() <= 10

            if is_valid_file:
                return False

        return True

    # Iterable files from request and call method inti_filebox_and_save_file for save files.
    def upload_user_file(self):
        files = self.request.files.values()

        for file in files:
            file_byte = self.files_byte_context.get(file.filename)
            file_manager = FileManager(file=file, file_byte=file_byte)
            self.inti_filebox_and_save_file(file_manager)

    # This method for save file to storage and create Table if it has None
    def inti_filebox_and_save_file(self, file_manager):
        user = self.get_user()
        all_files = self.all_files()

        if all_files is None:
            FileBoxRepository.init_files_box(
                self.to_file_model(file_manager),
                user.id
            )
            return

        to_file_model = self.to_file_model(file_manager, all_files.id)
        FileBoxRepository.add_file(to_file_model)
