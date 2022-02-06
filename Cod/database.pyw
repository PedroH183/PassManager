#! python3 
#
# Use o bat para criar a tabela 
# Use o passManager.bat para rodar o script

import psycopg2 as psy
import sys as sy
import pyperclip as pyr

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
        while True:
            conta = str(input('Digite a conta que deseja apagar\n'))
            if conta =='':
                continue
            cur.execute(f"DELETE FROM contas WHERE email = '{conta}';")
            conn.commit()
            break
        print('Conta apagada')

    elif num == '3': # consulta 
        while True:
            conta=str(input('Digite a conta que deseja copiar senha\n'))
            if conta == '':
                continue
            cur.execute(f"SELECT senha FROM contas WHERE email = '{conta}';") 
            ## listar as opçaões (implementar)
            passw = cur.fetchall()
            pyr.copy(str(passw[0][0]))
            print('Senha copiada para o clipboard')
            break
    else:
        erro()

    re_running(conn, cur)
    return

def re_running(conexao, cursor):
    while True:
        choice = ['y','n']
        desire = str(input('Voce quer rodar o script novamente ?[Y/N]')).lower()
        if desire not in choice:
            continue
        if desire == 'y':
            global numero # trabalhando com o escopo 
            global escolha
            print(escolha)
            numero = input()
            runnig(conexao, cursor, numero)
        else:
            return


def erro():
    print(f"""Erro Operacional possíveis causa ::
              Seu DB está rodando ?
              O nome do DB está correto ?
              Seu user está cadastrado ?""")
    sy.exit()

# menu de entrada
dbname = str(input('Digite o nome do banco de dados\n'))
usuario= str(input('Digite o nome do Usuario que vai logar no DB\n'))
pass_user = str(input('Digite a senha do user\n'))
escolha = str("""
Escolha a opção que melhor descrever seu objetivo:
1--Salvar uma conta
2--Apagar uma conta
3--Consultar conta\n""")
print(escolha)
numero = input()

try:
    connect = psy.connect(host='localhost',user=usuario,password=pass_user,database=dbname)
    cursor = connect.cursor()
    runnig(connect, cursor, numero)

except:
    erro()

finally:
    cursor.close() # evitando perda de memoria
    connect.close()
