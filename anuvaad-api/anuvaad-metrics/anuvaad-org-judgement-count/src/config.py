import os
import pymongo

## app configuration variables
DEBUG = False
API_URL_PREFIX = "/anuvaad-metrics"
HOST = "0.0.0.0"
PORT = 5001

ENABLE_CORS = True


MONGO_SERVER_URL = os.environ.get("MONGO_CLUSTER_URL", "mongodb://localhost:27017")
USER_DB = os.environ.get("MONGO_DB_IDENTIFIER", "usermanagement")
WFM_DB = os.environ.get("MONGO_WFM_DB", "anuvaad-etl-wfm-db")
PREPROCESSING_DB = os.environ.get("MONGO_CH_DB", "preprocessing")


USER_COLLECTION = "sample"
WFM_COLLECTION = "anuvaad-etl-wfm-jobs-collection"
FILE_CONTENT_COLLECTION = "file_content"

DOWNLOAD_FOLDER = "upload"
USERMANAGEMENT = os.environ.get(
    "USERMANAGEMENT_URL", "http://gateway_anuvaad-user-management:5001"
)

# mail server configs
MAIL_SETTINGS = {
    "MAIL_SERVER": os.environ.get("SMTP_HOST", "********************"),
    "MAIL_PORT": os.environ.get("SMTP_PORT", 465),
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get("SMTP_USERNAME", "***************"),
    "MAIL_PASSWORD": os.environ.get("SMTP_PASSWORD", "************************"),
    "MAIL_SENDER_NAME": os.environ.get("SMTP_SENDERNAME", "Anuvaad Support"),
    "MAIL_SENDER": os.environ.get("SUPPORT_EMAIL", "anuvaad.support@tarento.com"),
}
MAIL_SENDER = os.environ.get("SUPPORT_EMAIL", "anuvaad.support@tarento.com")


LANG_MAPPING = {
    "en": "English",
    "kn": "Kannada",
    "gu": "Gujrati",
    "or": "Oriya",
    "hi": "Hindi",
    "bn": "Bengali",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "ma": "Marathi",
    "pa": "Punjabi",
    "kok": "Konkani",
    "sa": "Sanskrit",
    "sd": "Sindhi",
    "ur": "Urdu",
    "ne": "Nepali",
    "brx": "bodo",
    "doi": "Dogri",
    "sat": "Santali",
    "mni": "Manipuri",
    "lus": "Lushai",
    "kha": "Khasi",
    "ks": "Kashmiri",
    "mai": "Maithili",
    "pnr": "Panim",
    "grt": "Garo",
    "si": "Sinhalese",
    "njz": "Nishi",
    "as": "Assamese",
}
