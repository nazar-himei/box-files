from base64 import b64decode, b64encode
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from magic import from_buffer

from consts.file_const import ALLOWED_EXTENSIONS


# FileManager is model for provide more detail about file [type, size, base64]
class FileManager:

    def __init__(self, file, file_byte=None):
        self.file = file
        self.file_byte = file_byte

    # Decode file to base64
    def decode_base64(self):
        return b64decode(self.encode_base64())

    # Encode file to base64
    def encode_base64(self):
        return b64encode(self.file_byte)

    # Get current size of file.
    def get_size_of_file(self):
        return len(self.encode_base64()) * 3 / 4 - str(self.encode_base64()).count('=')

    # Provide type info file.
    def get_type_of_file(self):
        bytes_file = BytesIO(self.decode_base64())
        bytes_file.seek(0)
        type_file = from_buffer(bytes_file.read(), mime=True).split('/')[-1]

        return type_file

    # Get file name without type a file.
    def get_filename(self):
        filename = self.file.filename.split('.')
        last_index_file_type = len(filename) - 1

        return filename[last_index_file_type]

    @staticmethod
    def allowed_files(filename):
        return '.' in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class ZipFileManager:
    """
    ZipFileManager is model that does archive files.
    Default convert type .zip
    """

    def __init__(self, mode='w', compression=ZIP_DEFLATED):
        self.mode = mode
        self.compression = compression
        self.file_byte = BytesIO()
        self.zip_file = ZipFile(
            file=self.file_byte,
            mode=mode,
            compression=compression,
        )

    # Write file to zip.
    def write_file_to_zip(self, filename, file_data):
        self.zip_file.writestr(filename, file_data)

    # Close zip file and clear.
    def close_zip_file(self):
        self.zip_file.close()
        self.file_byte.seek(0)
