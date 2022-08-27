from pydantic import BaseModel


class FileDeleteBase(BaseModel):
    files_id: list

    def __repr__(self):
        return f'files_id {self.files_id}'
