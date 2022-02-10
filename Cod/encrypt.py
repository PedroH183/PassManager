#! python3 
# Gerando um hash para retirar o sample text do banco de dados


import rsa
# é uma criptografia assimetrica, chaves diferentes são usadas
# criptografar com a publi e descri com a priv

def encrypt(passwd):
    passwd = passwd.encode('utf-8')
    
    with open('./keys\publi.pem', mode='rb') as pub:
        data_content = pub.read()

    pub = rsa.PublicKey.load_pkcs1_openssl_pem(data_content,'PEM')
    passwd = rsa.encrypt(passwd, pub)

    return passwd


def decrypt(passwd):
    passwd = passwd.encode()

    with open('./keys\priv.pem', mode='rb') as priv:
        data_content = priv.read()

    priv = rsa.PrivateKey.load_pkcs1(data_content)
    decrypt_pass = rsa.decrypt(passwd, priv)
    
    decrypt_pass = str(passwd)

    return decrypt_pass

x = encrypt('polololkfa4')
print(x)