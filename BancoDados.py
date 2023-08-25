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
                                id_cliente_cpf INTERGER PRIMARY KEY, 
                                nome_cliente VARCHAR(50) NOT NULL,
                            );''')
        
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS produtos(
                                id_produto INTERGER PRIMARY KEY AUTOINCREMENT,
                                nome_produto VARCHAR(50),
                                valor FLOAT);
                                ''')
        
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS vendas(
                                id_venda INTERGER PRIMARY KEY AUTOINCREMENT
                                fk_cliente_cpf INTERGER NOT NULL,
                                fk_produto INTERNGER NOT NULL
                                quantidade INTERGER NOT NULL,
                                FOREIGN KEY (fk_produto) REFERENCES produtos(id_produto),
                                FOREIGN KEY (fk_cliente_cpf) REFERENCES clientes (id_cliente_cpf)
                            );''')
        self.conexao.commit()
        print( f"Tabelas produtos, clientes e vendas criadas para  o banco de dados {self.nome_bd}")
        self.desconectar_bd()
        
        
