

class Settings:
    DEBUG: bool = False

    TITLE: str = "文件管理系统"
    with open("./config.ini", "r", encoding="utf-8") as f:
        str_config = f.readlines()

    config: dict = {}

    for line in str_config:
        t = line.strip().split("=")
        if len(t) == 2:
            config[t[0]] = t[1]

    ip: str = config["ip"]
    port: int = int(config["port"])


settings = Settings()
