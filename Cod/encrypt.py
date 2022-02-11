#! python3 
# don't save plain text in DB 

import rsa
import base64 as bs

def encrypt(passwd): # using public key 
    passwd = passwd.encode()
    
    with open('./Cod\keys\pubkey.pem', mode='rb') as pub:
        pub = rsa.PublicKey.load_pkcs1(pub.read())

    encry_pass = rsa.encrypt(passwd, pub)
    encry_pass = bs.b32encode(encry_pass) 
    # thi is very important for storage a value in db
    encry_pass = encry_pass.decode()

    return encry_pass


def decrypt(passwd): # using private key
    passwd = passwd.encode()

    with open('./Cod\keys\privkey.pem', mode='rb') as priv:
        priv = rsa.PrivateKey.load_pkcs1(priv.read())
    
    decrypt_pass = bs.b32decode(passwd)
    decrypt_pass = rsa.decrypt(decrypt_pass, priv)

    return decrypt_pass

# save a pub and private key in a file verify the documentation of RSA ...
# call the generatekeys_saves if you don't have a dir key 
def generatekeys_save():
    (pubKey,privKey) = rsa.newkeys(1024,poolsize=4)

    with open('./Cod\keys\pubkey.pem', mode='wb') as file:
        file.write(pubKey.save_pkcs1('PEM'))
    
    with open('./Cod\keys\privkey.pem', mode='wb') as file:
        file.write(privKey.save_pkcs1('PEM'))