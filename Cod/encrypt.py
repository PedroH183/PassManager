#! python3 
# don't save plain text in DB 

import os
import rsa
import base64 as bs


def encrypt(passwd): # using public key 

    """ENCRYPT THE PASSWORD FOR STORAGE IN DATABASE
    
    returns the password encrypted with rsa and encode with 32 base 
    """

    passwd = passwd.encode()

    ## verificando o cwd da execução do programa por causa do path relativo
    with open('./Cod\\keys\\pubkey.pem', mode='rb') as pub:
        pub = rsa.PublicKey.load_pkcs1(pub.read())

    encry_pass = rsa.encrypt(passwd, pub)
    encry_pass = bs.b32encode(encry_pass) 
    # this is very important for storage a value in db
    encry_pass = encry_pass.decode()

    return encry_pass


def decrypt(passwd): # using private key

    """DECRYPT THE PASSWORD STORAGED IN DB
    
    returns decrypt password storaged in db and decode the 32 base for copy for clipboard
    """

    passwd = passwd.encode()

    with open('./Cod\\keys\\privkey.pem', mode='rb') as priv:
        priv = rsa.PrivateKey.load_pkcs1(priv.read())
    
    decrypt_pass = bs.b32decode(passwd)
    decrypt_pass = rsa.decrypt(decrypt_pass, priv)
    decrypt_pass = decrypt_pass.decode()
    
    return decrypt_pass


def generatekeys_save(value):

    """MAKE THE DIRECTORY KEYS WITH KEY PUBLIC AND PRIVATE FOR ENCRYPT PASSWD IN DB
    
    if don't indentify a dir 'key' in the cod he will make with the public and private key
    """

    if value: # se houver algum diretório no cwd chamado keys ele vai ignorar a criação de novas chaves!! 
        return

    print('Não há chaves salvas digite um valor de base 2 para ser o tamanho da key\nExemplo:\n[256,512,1024,2048,4096]\nEscolha padrão press enter')
    tamanho_key = int(input())

    if tamanho_key == '':
        tamanho_key = 512 # ideal 

    (pubKey,privKey) = rsa.newkeys(tamanho_key) # você pode alterar para numeros maiores, mas verá que o cod ficará mais lento

    os.makedirs(os.getcwd()+'\\Cod\\keys') # create all directorys to the keys 

    with open('./Cod\\keys\\pubkey.pem', mode='ab+') as file: # create file pub and priv keys in dir keys ...
        file.write(pubKey.save_pkcs1('PEM'))
    
    with open('./Cod\\keys\\privkey.pem', mode='ab+') as file:
        file.write(privKey.save_pkcs1('PEM'))
    
    return