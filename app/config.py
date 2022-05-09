import os
import os.path as op

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY')

    DATABASE_CONNECT_OPTIONS = {}
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "secret"

    # Recaptcha secret keys
    RECAPTCHA_PUBLIC_KEY = "6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J"
    RECAPTCHA_PRIVATE_KEY = "6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu"

    # Set Bootswatch theme
    FLASK_ADMIN_SWATCH = 'cerulean'

    CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND"]

    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    hostname = os.environ["DB_HOSTNAME"]
    port = os.environ["DB_PORT"]
    database = os.environ["APPLICATION_DB"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{user}:{password}@{hostname}:{port}/{database}"
    )

    # File upload configs
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif', '.pdf', '.docx', '.doc']

    # Languages for Babel
    LANGUAGES = {'en_US': 'English',
                 'fr_FR': 'French'}

    # Mailing config parameters
    # The actual values should be different for testing, development, and
    # production
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = int(os.environ['MAIL_PORT'] or 25)
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS'] == "True"
    MAIL_USE_SSL = os.environ['MAIL_USE_SSL'] == "True"
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER'] or os.environ['MAIL_USERNAME']

    PATH_PERSONAL_FILES = op.join(
        op.dirname(__file__), 'data', 'personal_files')
    PATH_INIT_MODELS = op.join(op.dirname(__file__), 'data_types')


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
