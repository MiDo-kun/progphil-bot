import os
from pathlib import Path

import dotenv
import yaml


dotenv.load_dotenv()


def _load_env(loader: yaml.Loader, node: yaml.Node) -> str:
    """A constructor for loading ENV YAML tags

    Usage in the YAML config:

        # Key is the config key
        app:
            key: !ENV "value"
    """

    default = None
    config_value = loader.construct_scalar(node)
    return os.getenv(config_value, default)


yaml.SafeLoader.add_constructor("!ENV", _load_env)

if Path("user-config.yml").exists():
    print("`user-config.yml` file found, loading user configurations.")
    with open("user-config.yml", "r") as CONFIG:
        CONFIG = yaml.safe_load(CONFIG)
else:
    with open("config.yml", "r") as CONFIG:
        CONFIG = yaml.safe_load(CONFIG)


class ConfigGen(type):
    """A metaclass for accessing configuration by accessing
    class attributes.

    key specifies the YAML key.

    Example:
        # config.yml

        bot: <--- key
            prefix: "!"
            token: !ENV "token"


        # config.py

        class BotConfig(metaclass=ConfigGen):
            key = "bot"

            prefix: str
            token: str

        # main.py

        from config import BotConfig

        class PPH(Bot):
            super().init(
            **kwargs,
            command_prefix=BotConfig.prefix,
            intents=intents
        )

        instance = PPH()

        instance.run(BotConfig.token)
    """

    def __getattr__(cls, name: str):
        """This method will get invoked in the child class
        when you try to get an attribute from the child class
        """
        try:
            name = name.lower()
            return CONFIG[cls.key][name]
        except KeyError:
            print(f"\u001b[31mERROR\u001b[37m: \u001b[33m{name}\u001b[37m was not found in the config file. Did you set it up correctly?")


# Dataclasses here
class BotConfig(metaclass=ConfigGen):
    key = "bot"

    prefix: str
    token: str


class GuildInfo(metaclass=ConfigGen):
    key = "guild"

    staff_roles: list[int]
    dev_help_forum: int
    log_channel: int


class Database(metaclass=ConfigGen):
    key = "database"

    name: str
    host: str
    user: str
    password: str


class API(metaclass=ConfigGen):
    key = "api"

    api_ninja: str