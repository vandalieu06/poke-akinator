class Config(object):
    SECRET_KEY = "86d27b0aaa812eee1b0d607355b1eaf96c4ebd955cc4f72523543535a109b671"
    MAIN_REDIRECT_URL = "/game"


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5000


class ProductionConfig(Config):
    DEBUG = False
    HOST = "0.0.0.0"
