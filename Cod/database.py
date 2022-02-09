#! python3 
#
# Use o bat para criar a tabela 
# Use o passManager.bat para rodar o script

import psycopg2 as psy
from pyperclip import copy 
from inicio import entrada,opcao
from sys import exit
from encrypt import encrypt
from randomPass import rd_pass

def print_select(conexao, cursor):
    cursor.execute(f'SELECT id, email FROM contas;')
    dados = cursor.fetchall()
    print('*'*25+ 'Contas' +'*'*25)
    if len(dados)<1:
        print('Lista vazia...')
        print('*'*25+ 'Contas' +'*'*25)
        re_running(conexao, cursor)
    for row in dados:
        print(row)
    print('*'*25+ 'Contas' +'*'*25)
    return

def runnig(conn, cur, num): 
#Criando a tabela que armazenará suas contas 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contas(
    id Serial,
    email varchar(30),
    senha varchar(70),
    salt varchar(35),
    app_name varchar(30),
    PRIMARY KEY(id));""")
    conn.commit() # atualizações pertinentes ao DB

    if num == '1':#salvar uma conta
        while True:
            email = str(input('Digite o email que deseja salvar\n'))
            app = str(input('Digite o nome do app que deseja salvar\n'))

            ## send to hash.py for encrypt password 
            senha = rd_pass()
            senha, salt = encrypt(senha) # senha aleatória
            ## aprender a criptografar está indo apenas o hash 
            if (email == '' or senha ==''):
                print('não deixe campos em branco')
                continue
            cur.execute(f"INSERT INTO contas(email,senha,salt) VALUES ('{email}', '{senha}','{salt}')")
            conn.commit()
            break
        print('conta salva')

    elif num == '2': # apagar uma conta 
        print_select(conn, cur)
        while True:
            cod = int(input('Digite o id da conta que deseja apagar\n'))
            if cod == '':
                continue
            cur.execute(f"DELETE FROM contas WHERE id = {cod}")
            conn.commit()
            break
        print('Conta apagada')

    elif num == '3': # consulta 
        # inserindo o print de lista 
        print_select(conn,cur)
        while True:
            conta=str(input('Digite o id da conta que deseja copiar senha\n'))
            if conta == '':
                continue
            cur.execute(f"SELECT senha FROM contas WHERE id = '{conta}';") 
            ## listar as opçaões (implementar)
            passw = cur.fetchall()
            copy(str(passw[0][0])) # tupla de listas 
            print('Senha copiada para o clipboard')
            break
    else:
        erro()
    
    re_running(conn, cur)

    
def re_running(conexao, cursor):
    while True:
        choice = ['y','n']
        desire = str(input('Voce quer rodar o script novamente ?[Y/N]')).lower()
        if desire not in choice:
            continue
        if desire == 'y':
            escolha = opcao()
            print(escolha)
            runnig(conexao, cursor, escolha)
        elif desire == 'n':
            cursor.close()
            conexao.close()
            exit('Bye...')
        else:
            print('erro de interpretação')


def erro():
    print(f"""Erro Operacional possíveis causa ::
              Seu DB está rodando ?
              O nome do DB está correto ?
              Seu user está cadastrado ?
              A função correta ?""")
    exit()

# menu de entrada
dbname, usuario, pass_user = entrada()

try:
    connect = psy.connect(host='localhost',user=usuario,password=pass_user,database=dbname)
    cursor = connect.cursor()
    print('DB CONNECT')
    escolha = opcao()
    runnig(connect, cursor, escolha)

except (Exception, psy.Error):
    print('FAIL IN CONNECT DB...')

finally:
    print('ENCERRANDO A CONEXÃO ...')
    cursor.close() # evitando perda de memoria
    connect.close()
    exit()