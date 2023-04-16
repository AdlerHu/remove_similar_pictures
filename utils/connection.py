from sqlalchemy import create_engine

def connect_db():
    # 設定資料庫連線字串
    db_user = 'user1'
    db_password = 'test'
    db_host = '127.0.0.1'
    db_name = 'similar_images'
    connection_string = f'mysql://{db_user}:{db_password}@{db_host}/{db_name}'
    return create_engine(connection_string)
