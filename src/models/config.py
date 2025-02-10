from configparser import ConfigParser


class ConfigProvider:
    def __init__(self) -> None:
        self.data: ConfigParser = ConfigParser()
        self.data_read_ok: list[str] = self.data.read("data.cfg")
