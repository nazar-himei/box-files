INVALID_TYPE_DATA_JSON = {"status": "failure", "msg": "Incorrect data type"}
INVALID_TYPE_OF_FILE = {"status": "failure", "msg": "Invalid upload file"}
INVALID_FILE_ID = {"status": "failure", "msg": "Invalid file id"}


def default_body_json(status="success", data=()):
    return {"status": status, "data": data}
