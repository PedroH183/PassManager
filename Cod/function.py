#! python3 
# FUNÇÕES DO COD 

import encrypt as enc
import config
from pyperclip import copy
from randomPass import rd_pass

def save(conn,cur):

    """SAVE A ACCOUNT IN DATABASE
    
    email input == str, the email is value for storage your user with app_name 
    app input == str, is the name of application that you wants save 
    senha output == str, is the password random that will storaged in DB with encryptation

    """
    
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
    senha = enc.encrypt(senha) # encrypt the password random 

    cur.execute(f"INSERT INTO contas(email,senha,app_name) VALUES ('{email}', '{senha}', '{app}')")
    conn.commit()

    print('CONTA SALVA E SENHA COPIADA')

    return 

def delete(conn,cur):

    """DELETE ACCOUNT IN DATABASE BY ID
    
    Cod is a int values asked is also id in DB that is more comfortable digit the id that email 

    """

    dados = printer(conn, cur) # print account storaged

    if len(dados) == 0:
        print('NÃO TEM DELETE, DB VAZIO')
        re_run(conn, cur)

    while True:
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
        

def printer(conn,cur):

    """PRINT THE VALUES STORAGED IN DB
    
    Is default query for not need repeat query in all definitations and not print the value encrypt of db
    because he's a massive length of characters 


    returns dados
    """

    cur.execute(f'SELECT id, email FROM contas')
    dados = cur.fetchall() # tuple return

    if len(dados) == 0:
        print('LISTA VAZIA')
        re_run(conn,cur)

    print('*'*25+ 'Contas' +'*'*25)
    [print(list(row)) for row in dados]  # print all values in dados   
    print('*'*25+ 'Contas' +'*'*25)

    return dados

def query(conn,cur):

    """CONSULT THE VALUES STORAGED IN DB FOR COPY PASSWORD
    
    datas will storage all id's valid for avaible conta input that if not in datas will repeat the loop
    also decrypts the password storaged in db and copy for clipboard 

    """

    printer(conn,cur) # take id return of contas table

    datas = []

    cur.execute("""SELECT id FROM contas""")
    linhas = cur.fetchall()

    for row in linhas:
        datas.append(row[0])

    if len(linhas) == 0:
        print('NÃO TEM CONSULTA, DB VAZIO')
        re_run(conn,cur)

    while True:
            
        conta = int(input('Digite o id da conta que deseja copiar senha\n'))

        if conta not in datas:
            print('DIGITE UM ID VÁLIDO')
            continue

        cur.execute(f"SELECT senha FROM contas WHERE id = '{conta}';")
        passw = cur.fetchone()
        passw = passw[0]
            
        passw = enc.decrypt(passw) # tupla de lista
        copy(passw)
        print('SENHA COPIADA PARA O CLIPBOARD')
        break
    
    return

    
def re_run(conn, cur):

    """ASK IF WANT RE RUN THE PROGRAM
    
    choice is a value positive and negative for re-run the program 
    don't have return because will exit or possible error of logical 

    """

    while True:

        choice = ['y','n']
        desire = str(input('Voce quer rodar o script novamente ?[Y/N]')).lower()

        if desire not in choice:
            continue

        if desire == 'y':
            escolha = config.opcao()
            run(conn, cur, escolha) # database.py

        elif desire == 'n':
            cur.close()
            conn.close()
            exit('Bye...')
        
        else:
            print(f"""ERRO AO TENTAR RE-EXECUTAR O PROGRAMA""")
            exit('BYE...')


def run(conn, cur, choice): # modificar 

    """MAKE TABLE IN DB AND CALL THE FUNCTIONS FOR PROGRAM RUN"""

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contas(
    id Serial,
    email varchar(30) NOT NULL,
    senha varchar NOT NULL,
    app_name varchar NOT NULL,
    PRIMARY KEY(id));""")
    conn.commit()

    if choice == '1': # SAVE A ACCOUNT IN DB
        save(conn,cur)

    elif choice == '2': # DELETE A ACCOUNT IN DB
        delete(conn,cur)

    elif choice == '3': # COPY THE PASSWORD STORAGED IN DB
        query(conn,cur)
    
    re_run(conn,cur) # não cai no return
