#! python3 
# FUNÇÕES DO COD 

import encrypt as enc
import inicio
from pyperclip import copy
from randomPass import rd_pass


def save(conn,cur):
    """SAVE A ACCOUNT IN DATABASE"""
    
    while True:

        email = str(input('Digite o email que deseja salvar\n'))
        app = str(input('Digite o nome do site que deseja salvar\n'))

        if (email == '' or app == ''):
            print('não deixe campos em branco')
            continue
        
        else:
            break
    
    senha = rd_pass() # senha aleatória
    copy(senha)
    senha = enc.encrypt(senha) # encriptação 

    cur.execute(f"INSERT INTO contas(email,senha,app_name) VALUES ('{email}', '{senha}', '{app}')")
    conn.commit()

    print('CONTA SALVA E SENHA COPIADA')

    return 

def delete(conn,cur):
    """DELETE ACCOUNT IN DATABASE BY ID"""

    dados = printer(cur) # print account storaged

    while True:

        if len(dados) == 0:
            print('LISTA VAZIA')
            re_run(conn, cur)

        try:
            cod = int(input('Digite o id da conta que deseja apagar\n'))

        except ValueError:
            print("DIGITE UM VALOR DE ID (NUMERO)")
            continue

        cur.execute(f"DELETE FROM contas WHERE id = {cod}")
        conn.commit()

        print('ACCOUNT DELETED...')
        break

    return
        

def printer(cur):
    """PRINT THE VALUES STORAGED IN DB"""

    cur.execute(f'SELECT id, email FROM contas;')
    dados = cur.fetchall() # tuple return

    print('*'*25+ 'Contas' +'*'*25)
    
    if len(dados) == 0:
        print('LISTA VAZIA')
        return # falling in re_run the program 

    [print(list(row)) for row in dados]    
    print('*'*25+ 'Contas' +'*'*25)
    
    return 

def query(cur):
    """CONSULT THE VALUES STORAGED IN DB FOR COPY PASSWORD"""

    printer(cur) # take id return of contas table

    datas = []

    cur.execute("""SELECT id FROM contas""")
    linhas = cur.fetchall()

    for row in linhas:
        datas.append(row[0])

    while True:
            
        conta = int(input('Digite o id da conta que deseja copiar senha\n'))

        if conta not in datas:
            print('DIGITE UM ID VÁLIDO')
            continue

        cur.execute(f"SELECT senha FROM contas WHERE id = '{conta}';") # error ???
        passw = cur.fetchone() # avaliar funcionamento
        passw = passw[0]
            
        passw = enc.decrypt(passw) # tupla de lista
        copy(passw)
        print('SENHA COPIADA PARA O CLIPBOARD')
        break
    
    return

    
def re_run(conn, cur):
    """ASK IF WANT RE RUN THE PROGRAM"""

    while True:
        choice = ['y','n']
        desire = str(input('Voce quer rodar o script novamente ?[Y/N]')).lower()

        if desire not in choice:
            continue

        if desire == 'y':
            escolha = inicio.opcao()
            print(escolha)
            run(conn, cur, escolha) # database.py

        elif desire == 'n':
            cur.close()
            conn.close()
            exit('Bye...')
        
        else:
            erro()
        


def erro():
    """ERROR BETWEEN RUN THE PROGRAM"""

    print(f"""ERRO AO TENTAR RE-EXECUTAR O PROGRAMA""")
    exit('BYE...')


def run(conn, cur, choice): 
    """MAKE TABLE IN DB AND CALL THE FUNCTIONS FOR PROGRAM RUN"""

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contas(
    id Serial,
    email varchar(30) NOT NULL,
    senha varchar NOT NULL,
    app_name varchar(10) NOT NULL,
    PRIMARY KEY(id));""")
    conn.commit()

    if choice == '1': # SAVE A ACCOUNT IN DB
        save(conn,cur)

    elif choice == '2': # DELETE A ACCOUNT IN DB
        delete(conn,cur)

    elif choice == '3': # COPY THE PASSWORD STORAGED IN DB
        query(cur)
    

    return 