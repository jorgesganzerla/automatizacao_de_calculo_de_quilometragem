#!/usr/bin/env python3
## Script para configuração inicial do banco de dados

from database import DatabaseManager

def main():
    #Função principal para testar a conexão com o banco de dados
    print("=== Setup do Banco de Dados ===")
    print("Testando conexão com MySQL...")
    
    try:
        # Inicializar gerenciador de banco de dados
        db = DatabaseManager()
        print("✓ Conexão com banco de dados estabelecida!")
        print("✓ Sistema pronto para uso!")
        print("\nPara executar o sistema, use: python main.py")
        
    except Exception as e:
        # Exibir erro caso a conexão falhe
        print(f"✗ Erro ao conectar com banco de dados: {e}")
        print("\nVerifique:")
        print("1. Se o MySQL está rodando")
        print("2. Se o banco 'sistema_km' foi criado (execute create_database.sql)")
        print("3. Se a senha no arquivo database.py está correta")
        return False
    
    return True

if __name__ == "__main__":
    main()
