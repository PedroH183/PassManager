#! python3 
# menu para entrada de valores no database 

# modifique de acordo com seu db e user ...
def entrada():
    dbname = 'contas'
    usuario= 'tester'
    pass_user = '123456'
    return dbname, usuario, pass_user

def opcao():
    list_choice = ['1','2','3']
    while True:
        print((f"""
{'*'*25}Menu{'*'*25}    
Escolha uma função para o programa
1--Salvar uma conta
2--Apagar uma conta
3--Consultar conta
{'*'*25}Menu{'*'*25}
"""))
        escolha = str(input())
        if escolha not in list_choice:
            print('INSIRA UM VALOR VÁLIDO !!')
            continue
        else:
            break
    return escolha