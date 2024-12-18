from datetime import timedelta, timezone, datetime

PERU_TZ = timezone(timedelta(hours=-5))
def NOW():
    return datetime.now(PERU_TZ)

class App:
    name = "APP_NAME"
    host = "APP_HOST"
    port = "APP_PORT"

class MongoDB:
    uri = "MONGODB_URI"
    db = "MONGODB_DB"

class Env:
    APP = App()
    MONGODB = MongoDB()