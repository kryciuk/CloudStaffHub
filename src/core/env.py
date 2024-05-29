import environ

env = environ.Env(DEBUG=(bool, False), SECRET_KEY=(str, "default_secret_key"), ENVIRONMENT=(str, "local"))
