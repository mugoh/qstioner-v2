import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    CSRF_ENABLED = True
    BUNDLE_ERRORS = True
    SECRET_KEY = b'\xc2;F]l\x0490u&6t\xfe\x08'
    AUTH_TOKEN_EXP_DAYS = 30
    AUTH_TOKEN_EXP_SECS = 60 * 5


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True


APP_CONFIG = {'development': DevelopmentConfig,
              'testing': TestingConfig,
              'production': ProductionConfig
              }
