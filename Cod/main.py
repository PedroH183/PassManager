#! python3 
#
# RUN THE PASSMANAGER.BAT
# MAIN SCRIPT FOR RUN AND CONNECT THE PROGRAM WITH THE DB 

import os
import traceback
import psycopg2 as psy
from config import entrada,opcao
from sys import exit
from encrypt import generatekeys_save
from function import run
from traceback import format_exc

#################### MENU ##################

dbname, usuario, pass_user = entrada()
print('Verificando se há chaves salvas')
value = os.path.isdir(os.getcwd() + './Cod\\keys') # procurar o diretório chaves
generatekeys_save(value) # gerar as chaves e criar o diretório para elas 

################# CONNECT DB ################
try:
    connect = psy.connect(host='localhost',user=usuario,password=pass_user,database=dbname)
    cursor = connect.cursor()
    print('DB CONNECT')
    escolha = opcao()
    run(connect, cursor, escolha)

except (Exception, psy.Error):

    dir_exist = os.path.isdir('./Cod\\Error')

    # create dir 
    if dir_exist == False: # if the directory not exist, create 
        os.mkdir('./Cod\\Error')
        i = 1
    else:
        # interpreting the dir 
        dire = os.listdir('./Cod\\Error')
        if dire == []:
            i = 1
        else:
            for i in range(len(dire) + 1):
                i += 1
        
    with open(f'./Cod\\Error\Erro_psy_num{i}.txt',mode='a')as file:
        file.write(traceback.format_exc()) # module traceback 

finally:
    cursor.close() # evitando perda de memoria
    connect.close()
    print('ENCERRANDO A CONEXÃO ...')
    exit()