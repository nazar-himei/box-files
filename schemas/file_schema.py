from pydantic import BaseModel


class FileUserBase:
    def __init__(self, filename, size_of_data, type_data, file_id, description=None, create_file=None,
                 changed_file=None):
        self.filename = filename
        self.description = description,
        self.create_file = create_file
        self.changed_file = changed_file
        self.size_of_data = size_of_data
        self.type_of_data = type_data
        self.id = file_id

    def to_json(self):
        return {
            "filename": self.filename,
            "description": f"{self.description[0]}",
            "create_file": self.create_file,
            "changed_file": self.changed_file,
            "size_data": self.size_of_data,
            "type_data": self.type_of_data,
            "id": self.id,
        }


class FileDeleteBase(BaseModel):
    files_id: list

    def __repr__(self):
        return f'files_id {self.files_id}'


class FileUpdateBase(BaseModel):
    id: int
    description: str = None
    filename: str = None

    def __repr__(self):
        return f'file id: {self.id} description: ${self.description} filename: {self.filename}'


class FileSettingsBase:
    def __init__(self, file_byte, attachment_filename, mimetype):
        self.file_byte = file_byte
        self.attachment_filename = attachment_filename,
        self.mimetype = mimetype
