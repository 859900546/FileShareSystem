

class Settings:
    DEBUG: bool = True

    TITLE: str = "文件管理系统"
    with open("./config.ini", "r", encoding="utf-8") as f:
        str_config = f.readlines()

    config: dict = {}

    for line in str_config:
        t = line.strip().split("=")
        if len(t) == 2:
            config[t[0]] = t[1]
    # Mysql
    MYSQL_USERNAME: str = config["MYSQL_USERNAME"]
    MYSQL_PASSWORD: str = config["MYSQL_PASSWORD"]
    MYSQL_HOST: str = config["MYSQL_HOST"]
    MYSQL_PORT: int = int(config["MYSQL_PORT"])
    MYSQL_DATABASE: str = config["MYSQL_DATABASE"]

    ip: str = config["ip"]
    port: int = int(config["port"])


settings = Settings()
