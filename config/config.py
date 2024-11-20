

class Settings:
    DEBUG: bool = True

    TITLE: str = "文件管理系统"

    # Mysql
    MYSQL_USERNAME: str = "root"
    MYSQL_PASSWORD: str = "root"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = 'filesharesystem'

    ip: str = "127.0.0.1"
    port: int = 5000


settings = Settings()
