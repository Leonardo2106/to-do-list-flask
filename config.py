import os

SECRET_KEY = os.getenv('SECRET_KEY', 't0_d0_l1s7')

SQLALCHEMY_DATABASE_URI = (
    f'{os.getenv('SGBD', 'mysql+mysqlconnector')}://'
    f'{os.getenv('DB_USER', 'root')}:'
    f'{os.getenv('DB_PASSWORD', 'senha_teste')}@'
    f'{os.getenv('DB_HOST', 'localhost')}/'
    f'{os.getenv('DB_NAME', 'to_do_list')}'
)