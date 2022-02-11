#! python3 
#
# Use o bat para criar a tabela 
# Use o passManager.bat para rodar o script

import psycopg2 as psy
from pyperclip import copy 
from inicio import entrada,opcao
from sys import exit
from encrypt import encrypt, decrypt
from randomPass import rd_pass

def print_select(conexao, cursor):

    cursor.execute(f'SELECT id, email FROM contas;')
    dados = cursor.fetchall()

    mssg =('*'*25+ 'Contas' +'*'*25)
    print(mssg)

    if len(dados)<1:
        print('Lista vazia...')
        print(mssg)
        re_running(conexao, cursor)

    for row in dados:
        if type(row) == tuple:
            row = list(row)
            print(row)

    print(mssg)

    return

def runnig(conn, cur, num): 
#Criando a tabela que armazenará suas contas 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contas(
    id Serial,
    email varchar(30) NOT NULL,
    senha varchar(300) NOT NULL,
    app_name varchar(10) NOT NULL,
    PRIMARY KEY(id));""")
    conn.commit() # atualizações pertinentes ao DB

    if num == '1':#salvar uma conta
        while True:

            email = str(input('Digite o email que deseja salvar\n'))
            app = str(input('Digite o nome do site que deseja salvar\n'))
            
            senha = rd_pass() # senha aleatória
            copy(senha)
            senha = encrypt(senha) # encriptação 

            if (email == '' or app == ''):
                print('não deixe campos em branco')
                continue

            cur.execute(f"INSERT INTO contas(email,senha,app_name) VALUES ('{email}', '{senha}', '{app}')")
            conn.commit()

            break
        print('CONTA SALVA E SENHA COPIADA')



    elif num == '2': # apagar uma conta 
        print_select(conn, cur)
        while True:

            cod = int(input('Digite o id da conta que deseja apagar\n'))
            if cod == '' or type(cod) != int:
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
            passw = cur.fetchone() # avaliar funcionamento
            passw = passw[0]
            
            passw = decrypt(passw) # tupla de lista
            copy(passw)
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
    print(f"""
              Seu DB está rodando ?
              CONFIGURE SEU DB EM INICIO.PY
            """)
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