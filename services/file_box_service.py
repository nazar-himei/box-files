from datetime import datetime
from io import BytesIO

from pydantic import ValidationError

from models.file_box_model import FileUserModel
from repositories.file_box_repository import FileBoxRepository
from repositories.profile_repository import ProfileRepository
from schemas.file_schema import FileUserBase, FileUpdateBase, FileDeleteBase, FileSettingsBase
from services.file_manager import FileManager, ZipFileManager


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
            description=files_of_user.description,
            create_file=files_of_user.created_file_time,
            changed_file=files_of_user.changed_file_time,
            size_of_data=files_of_user.size_of_data,
            type_data=files_of_user.type_of_data,
            file_id=files_of_user.id
        )

    @staticmethod
    def to_file_model(file_manager, file_box_id=None):
        return FileUserModel(
            filename=file_manager.get_filename(),
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

    # Parse model DeleteFileBase
    @staticmethod
    def parse_delete_file_scheme(data):
        from pydantic import ValidationError
        try:
            model = FileDeleteBase.parse_raw(data)
        except TypeError:
            return None

        except ValidationError:
            return None

        return model

    # Check if is files id has in database files
    def is_empty_files_id(self, files_id):
        if type(files_id) is int:
            files_id = [files_id]

        for id_file in files_id:
            user_file = self.get_detail_file(id_file)
            if user_file is None:
                return True

        return False

    # Delete files from storage use to files_id
    def delete_file_from(self, files_id):
        files = self.all_files().files

        if files is None:
            return

        for file in files:
            for id_file in files_id:
                if file.id == id_file:
                    FileBoxRepository.delete_file(file)

    @staticmethod
    def parse_update_file_model(data):
        try:
            model = FileUpdateBase.parse_raw(data)
        except TypeError:
            return None

        except ValidationError:
            return None

        return model

    # Update current file use file_update_model
    def update_file_model(self, file_update_model):
        user_file = self.get_detail_file(file_update_model.id)

        if user_file is None:
            return

        if file_update_model.filename is not None:
            user_file.filename = file_update_model.filename

        if file_update_model.description is not None:
            user_file.description = file_update_model.description

        FileBoxRepository.save_file()

    # Archive files from storage and return zip file in format: byte code
    def archive_files_byte(self, files_id):
        file_manger = ZipFileManager()
        files = self.all_files().files

        for file in files:
            for file_id in files_id:
                if file_id == file.id:
                    file_manger.write_file_to_zip(
                        f"{file.filename}.{file.type_of_data}",
                        file.data)

        file_manger.close_zip_file()

        return file_manger.file_byte

    # Generate filename
    @staticmethod
    def generate_filename_filebox():
        return f"filebox-download-{datetime.utcnow().isoformat()}.zip"

    def generate_file_settings_model(self, files_id):
        len_files_id = len(files_id)

        if len_files_id == 0:
            return

        if len_files_id > 1:
            archive_files = self.archive_files_byte(files_id)

            return FileSettingsBase(
                file_byte=archive_files,
                attachment_filename=self.generate_filename_filebox(),
                mimetype="application/zip"
            )

        file = self.get_detail_file(files_id[0])

        if file is None:
            return None

        return FileSettingsBase(
            file_byte=BytesIO(file.data),
            attachment_filename=f"{file.filename}.{file.type_of_data}",
            mimetype=f"application/{file.type_of_data}"
        )
