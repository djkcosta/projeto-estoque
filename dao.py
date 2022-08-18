#DAO = DATA ACCESS OBJECT = OBJETO DE ACESSO A DADOS
#ONDE VOCE INSERE OS COMANDOS SQL
# INSTALAR SQLITEestudio

import sqlite3

#comandos SQL
from produto import Produto

SQL_PREPARA_BANCO = 'create table if not exists produto' \
                    '(descricao varchar(60) not null, ' \
                    'preco double not null, ' \
                    'quantidade integer not null)'

SQL_SALVA_PRODUTO = 'insert into produto values (?, ?, ?)'
SQL_LISTA_PRODUTO = 'select descricao, preco, quantidade, rowid from produto'
SQL_LISTA_PRODUTO_POR_ID = 'select descricao, preco, quantidade, rowid from produto where rowid=?'
SQL_ATUALIZA_PRODUTO = 'update produto set descricao=?, preco=?, quantidade=? where rowid=?'
SQL_DELETA_PRODUTO = 'delete from produto where rowid=?'


class ProdutoDao:
    def __init__(self, nome_banco):
        self.__nome_banco = nome_banco
        self.prepara_banco()

    def prepara_banco(self):
        print('Conectando banco de dados...', end='')
        conexao = sqlite3.connect(self.__nome_banco)
        conexao.cursor().execute(SQL_PREPARA_BANCO)
        #comitando senão nada tem efeito
        conexao.commit()
        print('OK')

    def salvar(self, produto):
        print('Salvando o produto....', end='')
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()

        if (produto.id!= None and len(produto.id) >0): #significa que o produto ja existe na tabela
            cursor.execute(SQL_ATUALIZA_PRODUTO,(produto.descricao, produto.preco, produto.quantidade, produto.id))
        else:
            cursor.execute(SQL_SALVA_PRODUTO, (produto.descricao, produto.preco, produto.quantidade))
            produto.id = cursor.lastrowid

        conexao.commit()
        print('OK')
        return produto

    def buscar_por_id(self, id):
        conexao = sqlite3.connect(self.__nome_banco) #criar conexao com o banco de dados
        cursor = conexao.cursor() #obtem o cursor do banco
        cursor.execute(SQL_LISTA_PRODUTO_POR_ID, [str(id)]) #executa o comando SQL
        tupla = cursor.fetchone() #recupera a consulta em forma de tupla
        return Produto(tupla[0], tupla[1], tupla[2], tupla[3]) #cria um objeto Produto a partir da tuplae retorna este

    def deletar(self, id):
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()
        cursor.execute(SQL_DELETA_PRODUTO, [str(id)])
        conexao.commit()

    def listar(self): #LISTA TODOS OS ITENS DA TABELA
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()
        cursor.execute(SQL_LISTA_PRODUTO)
        lista = cursor.fetchall()
        produtos = []
        for tupla in lista:
            produto = Produto(tupla[0], tupla[1], tupla[2], tupla[3])
            produtos.append(produto)
        return produtos