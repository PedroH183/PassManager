#! python3 
# Gerando um hash para retirar o sample text do banco de dados

import bcrypt as bc

## ver o modulo cryptography...
def encrypt(passwd):
    passwd = passwd.encode()
    salt = str(bc.gensalt())
    pass_encrypt = str(bc.hashpw(passwd, bc.gensalt()))
    salt = salt.strip('b\'')
    pass_encrypt = pass_encrypt.strip('b\'')
    return pass_encrypt, salt 
## os hash podem gerar barras invertidas ??
## eles podem dar problemas no armazenamento ??

def decrypt(passwd, salt):
    print()
