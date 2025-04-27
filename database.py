import os

import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash
from datetime import date

print('Conectando...\n')
try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        passwd=os.getenv('DB_PASSWORD', 'senha_teste'),
    )
except mysql.connector.Error as error:
    if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Erro na senha ou no nome do usuário')
    else:
        print(error)

cursor = connection.cursor()

cursor.execute('drop database if exists to_do_list;')
cursor.execute('create database to_do_list;')
cursor.execute('use to_do_list;')

tables = {}
tables['usuarios'] = ('''
    create table `usuarios`(
    `id` int(5) not null auto_increment,
    `nome` varchar(80) not null,
    `nickname` varchar(20) not null,
    `email` varchar(100) not null,
    `senha` varchar(100) not null,
    primary key (`id`)
    )engine = innodb default charset=utf8 collate utf8_bin;''')

tables['tarefas'] = ('''
    create table `tarefas`(
    `id` int(10) not null auto_increment,
    `titulo` varchar(80) not null,
    `tarefa` varchar(3000) not null,
    `importante` boolean not null default false,
    `data_criacao` datetime not null default current_timestamp,
    `prazo` date,
    `usuario_id` int(5) not null,
    primary key (`id`),
    foreign key (`usuario_id`) references `usuarios`(`id`) on delete cascade
    )engine = innodb default charset=utf8 collate utf8_bin;''')

for tabela in tables:
    tabela_sql = tables[tabela]
    try:
        print(f'Criando tabelas {tabela}...', end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Já existe a tabela')
        else:
            print(error.msg)
    else:
        print('OK')

cursor.execute('''
    insert into usuarios (nome, nickname, email, senha)
    values (%s, %s, %s, %s)  
''', ('Usuário teste', 'teste', 'teste@email.com', generate_password_hash('teste123').decode('utf8')))

cursor.execute('select id from usuarios where email=%s', ('teste@email.com',))
usuario_id = cursor.fetchone()[0]

tarefas_sql = '''
    insert into tarefas (titulo, tarefa, importante, prazo, usuario_id)
    values (%s, %s, %s, %s, %s)
'''
tarefas = [
    ('Estudar matemática', 'Capítulo 4 e 5', True, date(2025, 6, 1), usuario_id),
    ('Estudar Biologia', 'Capítulo 6 e 7', False, date(2025, 6, 3), usuario_id),
]

cursor.executemany(tarefas_sql, tarefas)

cursor.execute('select * from tarefas')
print(' --------------- Tarefas --------------- ')
for tarefa in cursor.fetchall():
    print(f'Título: {tarefa[1]}, Importante: {tarefa[3]}, Prazo: {tarefa[5]} User: {tarefa[6]}')

connection.commit()

cursor.close()
connection.close()






