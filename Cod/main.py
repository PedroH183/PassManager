#! python3 
#
# RUN THE PASSMANAGER.BAT FOR RUN THE PROGRAM 
# MAIN SCRIPT FOR RUN AND CONNECT THE PROGRAM WITH THE DB 

import os 
import psycopg2 as psy
from inicio import entrada,opcao
from sys import exit
from encrypt import generatekeys_save
from function import run

#################### MENU ##################

dbname, usuario, pass_user = entrada()
value = os.path.isdir(os.getcwd() + '.\Cod\\keys')
generatekeys_save(value)

################# CONNECT DB ################
try:
    connect = psy.connect(host='localhost',user=usuario,password=pass_user,database=dbname)
    cursor = connect.cursor()
    print('DB CONNECT')
    escolha = opcao()
    run(connect, cursor, escolha)

except (Exception, psy.Error):
    print('FAIL IN CONNECT DB...')

finally:
    print('ENCERRANDO A CONEXÃO ...')
    cursor.close() # evitando perda de memoria
    connect.close()
    exit()