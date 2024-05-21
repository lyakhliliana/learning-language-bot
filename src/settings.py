from envparse import Env

env = Env()

TG_TOKEN = env.str(
    "TG_TOKEN",
    default=""
)
