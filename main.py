from os import system
import os
import dotenv
from neo4j import GraphDatabase

load_status = dotenv.load_dotenv("Neo4j-e2eb3cbe-Created-2024-06-16.txt")
if load_status is False:
    raise RuntimeError('Environment variables not loaded.')

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))



def find_vendedor():
    print("|Carregando vendedores...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    result = [row for row in session.execute(f"SELECT * FROM mercadolivre.vendedor;")]

    print("|Vendedores cadastrados")
    for i in range(len(result)):
        print(f"|{i+1} - {result[i].id}")
        print(f"|Nome: {result[i].nome}")
        print(f"|CNPJ: {result[i].cnpj}")

    try:
        r = int(input("|Selecione o vendedor: "))
        return result[r-1]
    except: pass

def find_usuario():
    print("|Carregando usuarios...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    result = [row for row in session.execute(f"SELECT * FROM mercadolivre.usuario;")]

    print("|Usuario cadastrados")
    for i in range(len(result)):
        print(f"|{i+1} - {result[i].id}")
        print(f"|Nome: {result[i].nome}")
        print(f"|Favoritos: {0 if not result[i].favoritos else len(result[i].favoritos)}")

    try:
        r = int(input("|Selecione o usuario: "))
        u = result[r-1]
        return {
            "id": u.id,
            "nome": u.nome,
            "favoritos": [] if u.favoritos is None else u.favoritos
        }
    except: pass

def selecionar_produtos(produtos: list = None):
    print("|Carregando produtos...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    if produtos is None:
        produtos = [row for row in session.execute(f"SELECT * FROM mercadolivre.produto;")]
    else:
        produtos = [[*session.execute(f"SELECT * FROM mercadolivre.produto where id = {id};")][0] for id in produtos]
    
    print("|Produtos")
    for i in range(len(produtos)):
        print(f"|{i+1} - {produtos[i].id}")
        print(f"|Nome: {produtos[i].nome}")
        print(f"|Descricao: {produtos[i].descricao}")
        print(f"|Valor: {produtos[i].valor}")
    
    try:
        selecionados = [int(n)-1 for n in input("|Selecione os produtos e separe com vírgulas(2, 5, 7, 8): ").split(",")]
        return [produtos[i] for i in selecionados]
    except: pass

def search_produto(nome: str):
    print("|Carregando produtos...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    produtos = [row for row in session.execute(f"SELECT * FROM mercadolivre.produto;")]
    produtos = [p for p in produtos if nome.lower() in p.nome.lower()]

    print("|Produtos encontrados")
    for p in produtos:
        print(f"|{p.id}")
        print(f"|Nome: {p.nome}")
        print(f"|Descricao: {p.descricao}")
        print(f"|Valor: {p.valor}")

def find_compra(data: str):
    print("|Carregando usuarios...", end="\r")
    session = cluster.connect()
    print(" "*100, end="\r")
    usuarios = [row for row in session.execute(f"SELECT * FROM mercadolivre.usuario;")]

    print("|Usuario cadastrados")
    for i in range(len(usuarios)):
        print(f"|{i+1} - {usuarios[i].id}")
        print(f"|Nome: {usuarios[i].nome}")
        print(f"|Favoritos: {0 if not usuarios[i].favoritos else len(usuarios[i].favoritos)}")
    
    try:
        usuario = usuarios[int(input("|Selecione o usuario: "))-1]
    except: return

    print(f"|Compras do usuário {usuario.nome}")
    compras = [] if not usuario.compras else [c for c in usuario.compras if str(c.data) == data]
    for i in range(len(compras)):
        print(f"|{i+1} - {compras[i].id}")
        print(f"|Nome: {usuario.nome}")
        print(f"|Valor: {compras[i].valor}")
        print(f"|Data: {compras[i].data}")
        print(f"|Produtos: {0 if not compras[i].produtos else len(compras[i].produtos)}")


def main():
    EXECUTANDO = True
    while EXECUTANDO:
        print("|Menu Principal      |")
        print("|1 - Insert Usuário  |")
        print("|2 - Insert Produto  |")
        print("|3 - Insert Vendedor |")
        print("|4 - Insert Compra   |")
        print("|5 - Search Usuário  |")
        print("|6 - Search Produto  |")
        print("|7 - Search Vendedor |")
        print("|8 - Search Compra   |")
        print("|0 - Sair            |")

        entrada = int(input("|Opção: "))
        system("cls")
        if entrada == 1:# Insert Usuário
            print("|Insira os dados do usuario")
            print("|Carregando...", end="\r")
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                print(" "*100, end="\r")

                records, summary, keys = driver.execute_query(
                    f"CREATE (:Usuario {{nome: '{input('|Nome: ')}', favoritos: []}})",
                    database_="neo4j",
                )
       
        elif entrada == 2:# Insert Produto
            print("|Insira os dados do produto")
            print("|Carregando...", end="\r")
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                print(" "*100, end="\r")

                records, summary, keys = driver.execute_query(
                    f"CREATE (:Produto {{nome: '{input('|Nome: ')}', descricao: '{input('|Descrição: ')}', valor: {float(input('|valor: '))}, vendedor: '{input('|Vendedor: ')}'}})",
                    database_="neo4j",
                )
        
        elif entrada == 3:# Insert Vendedor
            print("|Insira os dados do vendedor")
            print("|Carregando...", end="\r")
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                print(" "*100, end="\r")

                records, summary, keys = driver.execute_query(
                    f"CREATE (:Vendedor {{nome: '{input('|Nome: ')}', cnpj: '{input('|CNPJ: ')}', produtos: {input('|Produtos (separados por `,`): ').split(',')}}})",
                    database_="neo4j",
                )
        
        elif entrada == 4:# Insert Compra
            print("|Insira os dados da compra")
            print("|Carregando...", end="\r")
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                print(" "*100, end="\r")

                records, summary, keys = driver.execute_query(
                    f"CREATE (:Compra {{usuario: '{input('|Usuario: ')}', valor: {input('|Total: ')}, data: '{input('|Data(aaaa-mm-dd): ')}', produtos: {input('|Produtos (separados por `,`): ').split(',')}}})",
                    database_="neo4j",
                )
        
        elif entrada == 5:# Search Usuario
            print("|Busca por usuário")
            print("|Carregando...", end="\r")
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                print(" "*100, end="\r")

                records, summary, keys = driver.execute_query(
                    f"""MATCH (u:Usuario)
                        WHERE u.nome CONTAINS '{input('|Nome: ')}'
                        RETURN u""",
                    database_="neo4j",
                )

                for r in records:
                    print(r['u']._properties)
        
        elif entrada == 6:# Search Produto
            print("|Busca por produto: ")
            print("|Carregando...", end="\r")
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                print(" "*100, end="\r")
                
                records, summary, keys = driver.execute_query(
                    f"""MATCH (p:Produto)
                        WHERE p.nome CONTAINS '{input('|Nome: ')}'
                        RETURN p""",
                    database_="neo4j",
                )

                for r in records:
                    print(r['p']._properties)
        
        elif entrada == 7:# Search Vendedor
            print("|Busca por vendedor: ")
            print("|Carregando...", end="\r")
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                print(" "*100, end="\r")
                
                records, summary, keys = driver.execute_query(
                    f"""MATCH (v:Vendedor)
                        WHERE v.nome CONTAINS '{input('|Nome: ')}'
                        RETURN v""",
                    database_="neo4j",
                )

                for r in records:
                    print(r['v']._properties)
        
        elif entrada == 8:# Search Compra
            print("|Busca por compra: ")
            print("|Carregando...", end="\r")
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                driver.verify_connectivity()
                print(" "*100, end="\r")
                
                records, summary, keys = driver.execute_query(
                    f"""MATCH (c:Compra)
                        WHERE c.data CONTAINS '{input('|Data (aaaa-mm-dd): ')}'
                        RETURN c""",
                    database_="neo4j",
                )

                for r in records:
                    print(r['c']._properties)
        
        else: EXECUTANDO = False
    print("|Saindo...")
main()