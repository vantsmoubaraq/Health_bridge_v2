from os import getenv
storage_env = getenv("HB_STORAGE")
from sqlalchemy import text

if storage_env == "db":
    from models.engine.db_storage import DB_Storage
    storage = DB_Storage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
