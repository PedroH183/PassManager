#! python3 
#
# Use o bat para criar a tabela 
# Use o passManager.bat para rodar o script

import psycopg2 as psy
from pyperclip import copy 
from inicio import entrada,opcao
from sys import exit

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
    senha varchar(20),
    PRIMARY KEY(id));""")
    conn.commit() # atualizações pertinentes ao DB

    if num == '1':#salvar uma conta
        while True:
            email = str(input('Digite o email que deseja salvar\n'))
            senha = str(input('Digite a senha que deseja salvar\n'))
            if (email == '' or senha ==''):
                print('não deixe campos em branco')
                continue
            cur.execute(f"INSERT INTO contas(email,senha) VALUES ('{email}', '{senha}')")
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
    print('Voce está dentro')
    escolha = opcao()
    runnig(connect, cursor, escolha)

except (Exception, psy.Error) as e:
    print('Erro ao tentar conectar ao banco de dados')

finally:
    print('Bye..')
    cursor.close() # evitando perda de memoria
    connect.close()
    exit()