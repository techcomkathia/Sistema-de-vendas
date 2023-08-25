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
        
        
loja = BancoDados("lojinha.bd")

loja.conectar_bd()