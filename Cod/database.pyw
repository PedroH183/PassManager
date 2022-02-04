#! python3 
# Criar o banco de dados para que QUERY.PY possa armazenar



import psycopg2 as psy
from sys import exit

dbname = str(input('Digite o nome do banco de dados '))
usuario= str(input('Digite o nome do Usuario que vai logar no DB'))
pass_user = str(input('Digite a senha do user '))

def erro():
    print(f"""Erro Operacional possíveis causa ::
              Seu DB está rodando ?
              O nome do DB está correto ?
              Seu user está cadastrado ?""")
    exit()


try:
    conn = psy.connect(host='localhost',user=usuario,password=pass_user,\
    database=dbname)
except:
    erro()


cur = conn.cursor()
#Criando a tabela que armazenará suas contas 
cur.execute("""
CREATE TABLE IF NOT EXISTS contas(
    id Serial,
    site varchar(15),
    senha varchar(10),
    PRIMARY KEY(id)
    );
""")
conn.commit() # atualizações pertinentes ao DB

cur.close()
conn.close()