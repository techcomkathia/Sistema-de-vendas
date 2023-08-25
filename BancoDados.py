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
            self.conexao.commit()
        except:
            print(" erro ao inserir compra na tabela de vendas")
        finally:
            self.desconectar_bd()
    
    def atualizar_cliente(self, cpf, novo_nome_cliente):
        try:
            self.conectar_bd()
            self.cursor.execute(''' UPDATE clientes SET  nome_cliente = ? WHERE id_cliente_cpf = ? ;''', (novo_nome_cliente, cpf))
            print(f"Cliente {cpf} atualizado com sucesso para o nome de {novo_nome_cliente}")
            self.conexao.commit()
        except:
            print("erro ao atualizar o cliente")
        finally:
            self.cursor.close()
    
    def atualizar_produto(self, id, novo_nome_produto):
        try:
            self.conectar_bd()
            self.cursor.execute(''' UPDATE produtos SET  nome_produto = ? WHERE id_produto = ? ;''', (novo_nome_produto, id))
            print (f"Produto {id} atualizado com sucesso para {novo_nome_produto}")
            self.conexao.commit()
        except:
            print("erro ao atualizar o produto")
        finally:
            self.cursor.close()
            
    def selecionar_todos_produtos(self):
        try:
            self.conectar_bd()
            lista_produtos= self.cursor.execute(''' SELECT * FROM produtos ''').fetchall()
            print("----------PRODUTOS LOJA------------")
            for produto in lista_produtos :
                print( f"ID: {produto[0]} ")
                print( f"NOME: {produto[1]}")
                print( f"VALOR: R$ {produto[2]}")
                print("======================================")
        except:
            print("erro ao listar os produtos")
        finally:
            self.cursor.close() 
    
    def selecionar_produto(self, id):
        try:
            self.conectar_bd()
            produto= self.cursor.execute(''' SELECT * FROM produtos WHERE id_produto = ? ''', (id,)).fetchall()
            
            print ("======================================")
            print (f"ID : {produto[0][0]}")
            print (f"NOME : {produto[0][1]}")
            print (f"PRECO : {produto[0][2]}")
            print ("======================================")
        except:
            print(f"erro ao selecionar o produto de id {id}")
        finally:
            self.cursor.close()
            
    def selecionar_venda(self, id_venda):
        try:
            self.conectar_bd()
            venda = self.cursor.execute('''
                SELECT clientes.nome_cliente, 
                    clientes.id_cliente_cpf,
                    produtos.nome_produto,
                    produtos.valor as valor_unitario,
                    vendas.quantidade,
                    vendas.quantidade * produtos.valor AS valor_total
                FROM vendas
                INNER JOIN produtos ON vendas.fk_produto = produtos.id_produto
                INNER JOIN clientes ON vendas.fk_cliente_cpf = clientes.id_cliente_cpf
                WHERE id_venda = ?;
            ''', (id_venda,))

            print("=== Detalhes da venda ===")
            for item in venda:
                print(f"Cliente: {item[0]}")
                print(f"CPF: {item[1]}")
                print(f"Produto: {item[2]}")
                print(f"SubTotal: R$ {item[3],3}")
                print(f"Quantidade: {item[4]} unidades")
                print(f"Total: R$ {format(item[5],'.2f')}")
                print("=========================")

        except:
            print(f"Erro ao selecionar a venda de ID {id_venda}")
        finally:
            self.desconectar_bd()
  
    def excluir_venda (self, id_venda):
        try:
            self.conectar_bd()
            self.cursor.execute('''DELETE FROM vendas WHERE id_venda = ?''', (id_venda))
            self.conexao.commit()

            print(f" Venda de id {id_venda} foi excluída com sucesso")
        except:
            print(f"Erro ao excluir a venda de ID {id_venda}")
        finally:
            self.desconectar_bd()
                
loja = BancoDados("loja.db")
# loja.inserir_dados_clientes(11122233344, "Maria José")

# loja.atualizar_produto(1,"Calça")

# loja.atualizar_cliente(11122233344, "Maria Joaquina")

# loja.inserir_compra(11122233344,1,10)

loja.selecionar_venda(3)


