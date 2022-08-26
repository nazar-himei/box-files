class FileUserBase:
    def __init__(self, filename, size_of_data, type_data, file_id, create_file=None, changed_file=None):
        self.filename = filename
        self.create_file = create_file
        self.changed_file = changed_file
        self.size_of_data = size_of_data
        self.type_of_data = type_data
        self.id = file_id

    def to_json(self):
        return {
            "filename": self.filename,
            "create_file": self.create_file,
            "changed_file": self.changed_file,
            "size_data": self.size_of_data,
            "type_data": self.type_of_data,
            "id": self.id,
        }
