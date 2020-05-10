class Config:
    DEBUG = False
    TESTING = False
    HOST = "0.0.0.0"
    SECRET_KEY = (
        b"\xd3|\x9e\xfd\xa6\xbc\xa3\xaeb\x0f[-\xf2\xfas\x99\xa6\xb9\xe4%\xda8\xbc\x8d"
    )
    JSON_SORT_KEYS = False
    HUBSTAFF_APP_TOKEN = "GZQk6jIePM5JkFcz0j-3ZguSb2qm8Z4RQXamFV9NjQI"
    HUBSTAFF_AUTH_TOKEN = "-BI-txT5DJ3xOclZkajXi6DqvXpSZCWF2CQnmT40WAM"
    HUBSTAFF_API = "https://api.hubstaff.com/v1"
    # Hardcoding default values. Change this to send mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    # Hardcoding recipients. Ideally should use frontend to get recipients
    MAIL_SENDER = "kumaranvpl@gmail.com"
    MAIL_RECIPIENTS = ["hiring2@reef.pl"]


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    ENV = "production"
    SECRET_KEY = (
        b"2 \xd1\x9b\xcarR\x05\xcf]\xfe\x9d\xc5K\x08{'\xa2\xa1\xe3\xc5\r\xef\x1f"
    )
