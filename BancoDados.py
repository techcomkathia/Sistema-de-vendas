import sqlite3


#criação da Classe Database

class BancoDados():
    def __init__(self, nome_bd) -> None:
        self.nome_bd = nome_bd
        self.conexao = None
        self.cursor = None
    #  .conn usado para manter uma conexão com o banco de dados
    #  .corsor para executar consultas.
    
    def conectar_bd(self):
        self.conexao = sqlite3.connect(self.nome_bd)
        self.cursor = self.conexao.cursor()
        print (f"Banco {self.nome_bd} conectado")
    
    def desconectar_bd(self):
        self.conexao.close()
        print (f"Banco {self.nome_bd} desconectado")
        
        
    #método criar tabela une os comandos sql para o objeto instanciado
    def criar_tabelas(self):
        self.conectar_bd() #abre uma conexão com o banco
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes(
                                id_cliente_cpf INTEGER PRIMARY KEY, 
                                nome_cliente VARCHAR(50) NOT NULL
                            );''')
        
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS produtos(
                                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome_produto VARCHAR(50),
                                valor FLOAT);
                                ''')
        
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS vendas(
                                id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                                fk_cliente_cpf INTEGER NOT NULL,
                                fk_produto INTENGER NOT NULL,
                                quantidade INTEGER NOT NULL,
                                FOREIGN KEY (fk_produto) REFERENCES produtos(id_produto),
                                FOREIGN KEY (fk_cliente_cpf) REFERENCES clientes (id_cliente_cpf)
                            );''')
        self.conexao.commit()
        print( f"Tabelas produtos, clientes e vendas criadas para  o banco de dados {self.nome_bd}")
        self.desconectar_bd()
        
        
    def inserir_dados_clientes (self, cpf, nome_cliente):
        try:
            self.conectar_bd()
            self.cursor.execute(''' INSERT INTO clientes (id_cliente_cpf, nome_cliente)
                                    VALUES (?,?);''', #comando SQL
                                    (cpf, nome_cliente)) # passagem dos parâmetros recebidos pela função
            print(f"Cliente {nome_cliente} de CPF {cpf} inserido com sucesso")
            self.conexao.commit() # efetivando o comando
            
        except: 
            print ("Erro ao inserir cliente")
        finally:
            self.desconectar_bd() #fechando a conexão
    
    def inserir_dados_produto (self, nome_produto, valor):
        try:
            self.conectar_bd()
            self.cursor.execute(''' INSERT INTO produtos (nome_produto, valor)              
                                VALUES (?,?);''',
                                (nome_produto, valor))
            
            self.conexao.commit() # efetivando o comando
            
        except:
            print("erro ao inserir cliente")
            
        finally:
            self.desconectar_bd() #fechando a conexão
    
    def inserir_compra(self, cpf_cliente, id_produto, quantidade):
        try:
            self.conectar_bd()
            self.cursor.execute(''' INSERT INTO vendas (fk_cliente_cpf, fk_produto, quantidade)
                                    VALUES (?,?,?);''', 
                                    (cpf_cliente, id_produto, quantidade))
            print("Compra registrada")
        except:
            print(" erro ao inserir compra na tabela de vendas")
        finally:
            self.desconectar_bd()
        
        
        
loja = BancoDados("loja.db")
loja.inserir_dados_clientes(11122233344, "Maria José")

loja.inserir_dados_produto("Camiseta",29.90)

loja.inserir_compra(11122233344, 1, 10)
