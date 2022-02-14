#! python3 
#
# RUN THE PASSMANAGER.BAT
# MAIN SCRIPT FOR RUN AND CONNECT THE PROGRAM WITH THE DB 

import os 
import psycopg2 as psy
from config import entrada,opcao
from sys import exit
from encrypt import generatekeys_save
from function import run

#################### MENU ##################

dbname, usuario, pass_user = entrada()
print('Verificando se há chaves salvas')
value = os.path.isdir(os.getcwd() + '.\Cod\\keys') # procurar o diretório chave 
generatekeys_save(value) # gerar as chaves e criar o diretório para elas 

################# CONNECT DB ################
try:
    connect = psy.connect(host='localhost',user=usuario,password=pass_user,database=dbname)
    cursor = connect.cursor()
    print('DB CONNECT')
    escolha = opcao()
    run(connect, cursor, escolha)

except (Exception, psy.Error):
    print('ERROR RELACIONADO COM O PSYCOPG2')

finally:
    print('ENCERRANDO A CONEXÃO ...')
    cursor.close() # evitando perda de memoria
    connect.close()
    exit()