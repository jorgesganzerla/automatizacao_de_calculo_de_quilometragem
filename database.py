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
            'password': '',  # Altere para sua senha do MySQL
            'database': 'sistema_km'
        }
    
    def get_connection(self):
        """Estabelece e retorna uma conexão com o banco de dados"""
        return mysql.connector.connect(**self.config)
    
    def inserir_viagem(self, mes_referencia, motorista, setor, destino, km_saida, km_chegada, modelo_carro):
        """Insere uma nova viagem no banco de dados
        
        Args:
            mes_referencia: Mês de referência no formato MM/AAAA
            motorista: Nome do motorista
            setor: Setor de trabalho
            destino: Local de destino da viagem
            km_saida: Quilometragem inicial
            km_chegada: Quilometragem final
            modelo_carro: Modelo do veículo utilizado
            
        Returns:
            km_percorrida: Total de quilômetros percorridos
        """
        # Calcular quilometragem percorrida
        km_percorrida = km_chegada - km_saida
        # Formatar data e hora atual
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Conectar ao banco
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Inserir registro na tabela viagens
        cursor.execute('''
            INSERT INTO viagens (mes_referencia, data_hora, motorista, setor, destino, km_saida, km_chegada, km_percorrida, modelo_carro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (mes_referencia, data_hora, motorista, setor, destino, km_saida, km_chegada, km_percorrida, modelo_carro))
        
        # Confirmar transação e fechar conexão
        conn.commit()
        conn.close()
        return km_percorrida
    
    def obter_todas_viagens(self, mes_referencia=None):
        """Retorna todas as viagens registradas no banco de dados
        
        Args:
            mes_referencia: Filtro opcional por mês (formato MM/AAAA)
        
        Returns:
            Lista de dicionários contendo os dados de cada viagem
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Buscar viagens com filtro opcional de mês
        if mes_referencia:
            cursor.execute('''
                SELECT id, mes_referencia, data_hora, motorista, setor, destino, km_saida, km_chegada, km_percorrida, modelo_carro
                FROM viagens WHERE mes_referencia = %s ORDER BY id DESC
            ''', (mes_referencia,))
        else:
            cursor.execute('''
                SELECT id, mes_referencia, data_hora, motorista, setor, destino, km_saida, km_chegada, km_percorrida, modelo_carro
                FROM viagens ORDER BY id DESC
            ''')
        
        viagens = cursor.fetchall()
        conn.close()
        
        # Converter tuplas em dicionários para facilitar o acesso
        return [
            {
                "id": v[0],
                "mes_referencia": v[1],
                "data": v[2].strftime("%d/%m/%Y %H:%M"),
                "motorista": v[3],
                "setor": v[4],
                "destino": v[5],
                "km_saida": float(v[6]),
                "km_chegada": float(v[7]),
                "km_percorrida": float(v[8]),
                "modelo_carro": v[9]
            }
            for v in viagens
        ]
    
    def obter_meses_disponiveis(self):
        """Retorna lista de meses disponíveis com registros
        
        Returns:
            Lista com os meses de referência distintos ordenados
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Buscar meses únicos ordenados
        cursor.execute('SELECT DISTINCT mes_referencia FROM viagens ORDER BY mes_referencia DESC')
        meses = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return meses
    
    def obter_modelos_carros(self, mes_referencia=None):
        """Retorna lista de modelos de carros únicos cadastrados
        
        Args:
            mes_referencia: Filtro opcional por mês (formato MM/AAAA)
        
        Returns:
            Lista com os modelos de carros distintos
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Buscar modelos únicos com filtro opcional de mês
        if mes_referencia:
            cursor.execute('SELECT DISTINCT modelo_carro FROM viagens WHERE mes_referencia = %s ORDER BY modelo_carro', (mes_referencia,))
        else:
            cursor.execute('SELECT DISTINCT modelo_carro FROM viagens ORDER BY modelo_carro')
        
        modelos = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return modelos
    
    def obter_relatorio_por_modelo(self, modelo_carro, mes_referencia=None):
        """Retorna relatório de quilometragem por setor para um modelo específico
        
        Args:
            modelo_carro: Modelo do veículo para filtrar o relatório
            mes_referencia: Filtro opcional por mês (formato MM/AAAA)
            
        Returns:
            Lista de dicionários com setor, total de km e total de viagens
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Agrupar viagens por setor e somar quilometragens com filtro opcional de mês
        if mes_referencia:
            cursor.execute('''
                SELECT setor, SUM(km_percorrida) as total_km, COUNT(*) as total_viagens
                FROM viagens 
                WHERE modelo_carro = %s AND mes_referencia = %s
                GROUP BY setor 
                ORDER BY total_km DESC
            ''', (modelo_carro, mes_referencia))
        else:
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
    
    def excluir_viagem(self, viagem_id):
        """Exclui uma viagem do banco de dados
        
        Args:
            viagem_id: ID da viagem a ser excluída
            
        Returns:
            True se excluído com sucesso, False caso contrário
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Excluir viagem pelo ID
            cursor.execute('DELETE FROM viagens WHERE id = %s', (viagem_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao excluir viagem: {e}")
            return False

if __name__ == "__main__":
    # Teste de conexão com o banco de dados
    db = DatabaseManager()
    print("Conexão com banco de dados estabelecida com sucesso!")
