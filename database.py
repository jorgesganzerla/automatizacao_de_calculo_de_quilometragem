"""database.py - Gerenciador de conexão e operações com banco de dados MySQL"""

import mysql.connector
from datetime import datetime

class DatabaseManager:
    """Classe responsável por gerenciar todas as operações com o banco de dados"""
    
    def __init__(self):
        """Inicializa as configurações de conexão com o banco MySQL"""
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456789',
            'database': 'sistema_km'
        }
    
    def get_connection(self):
        #Estabelece e retorna uma conexão com o banco de dados
        return mysql.connector.connect(**self.config)
    
    def inserir_viagem(self, motorista, setor, destino, km_saida, km_chegada, modelo_carro):
        # Calcular quilometragem percorrida
        km_percorrida = km_chegada - km_saida
        # Formatar data e hora atual
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
        # Conectar ao banco
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Inserir registro na tabela viagens
        cursor.execute('''
            INSERT INTO viagens (data_hora, motorista, setor, destino, km_saida, km_chegada, km_percorrida, modelo_carro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (data_hora, motorista, setor, destino, km_saida, km_chegada, km_percorrida, modelo_carro))
        
        # Confirmar transação e fechar conexão
        conn.commit()
        conn.close()
        return km_percorrida
    
    def obter_todas_viagens(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Buscar todas as viagens ordenadas por ID decrescente
        cursor.execute('''
            SELECT id, data_hora, motorista, setor, destino, km_saida, km_chegada, km_percorrida, modelo_carro
            FROM viagens ORDER BY id DESC
        ''')
        
        viagens = cursor.fetchall()
        conn.close()
        
        # Converter tuplas em dicionários para facilitar o acesso
        return [
            {
                "id": v[0],
                "data": v[1].strftime("%d/%m/%Y %H:%M"),
                "motorista": v[2],
                "setor": v[3],
                "destino": v[4],
                "km_saida": float(v[5]),
                "km_chegada": float(v[6]),
                "km_percorrida": float(v[7]),
                "modelo_carro": v[8]
            }
            for v in viagens
        ]
    
    def obter_modelos_carros(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Buscar modelos únicos ordenados alfabeticamente
        cursor.execute('SELECT DISTINCT modelo_carro FROM viagens ORDER BY modelo_carro')
        modelos = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return modelos
    
    def obter_relatorio_por_modelo(self, modelo_carro):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Agrupar viagens por setor e somar quilometragens
        cursor.execute('''
            SELECT setor, SUM(km_percorrida) as total_km, COUNT(*) as total_viagens
            FROM viagens 
            WHERE modelo_carro = %s 
            GROUP BY setor 
            ORDER BY total_km DESC
        ''', (modelo_carro,))
        
        relatorio = cursor.fetchall()
        conn.close()
        
        # Converter resultado em lista de dicionários
        return [
            {
                "setor": r[0],
                "total_km": float(r[1]),
                "total_viagens": r[2]
            }
            for r in relatorio
        ]

if __name__ == "__main__":
    # Teste de conexão com o banco de dados
    db = DatabaseManager()
    print("Conexão com banco de dados estabelecida com sucesso!")