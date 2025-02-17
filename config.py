class Config:

    # 開発/本番環境
    DEBUG = True

    # DB接続情報
    SQLALCHEMY_DATABASE_URI = (
        # 開発環境
        # "postgresql+psycopg2://{user}:{password}@localhost/{db_name}".format(
        #     **{
        #         "user": "postgres",
        #         "password": "postgres",
        #         # "host": "postgres",
        #         "db_name": "filmhive",
        #     }
        # )
        # 本番環境
        "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(
            **{
                "user": "postgres.tltxwylvrqpoxwwudiga",
                "password": "filmhive",
                "host": "aws-0-ap-northeast-1.pooler.supabase.com",
                "port": "6543",
                "db_name": "postgres",
            }
        )
    )
