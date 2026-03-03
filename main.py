"""main.py - Interface gráfica do Sistema de Cálculo de Quilometragem"""

import customtkinter as ctk
from datetime import datetime
from database import DatabaseManager

class SistemaKilometragem:
    """Classe principal que gerencia a interface gráfica do sistema"""
    
    def __init__(self):
        """Inicializa a janela principal e configurações do sistema"""
        # Criar janela principal
        self.root = ctk.CTk()
        self.root.title("Sistema de Cálculo de Quilometragem")
        self.root.geometry("600x500")
        
        # Configurar tema da interface
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Inicializar gerenciador de banco de dados
        self.db = DatabaseManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura todos os elementos da interface gráfica"""
        # Título principal
        title = ctk.CTkLabel(self.root, text="Sistema de Cálculo de Quilometragem", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        # Frame principal que contém todos os elementos
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Criar campos de entrada para dados da viagem
        self.nome_entry = self.create_field(main_frame, "Nome do Motorista:", 0)
        self.setor_entry = self.create_field(main_frame, "Setor:", 1)
        self.destino_entry = self.create_field(main_frame, "Local de Destino:", 2)
        self.km_saida_entry = self.create_field(main_frame, "KM de Saída:", 3)
        self.km_chegada_entry = self.create_field(main_frame, "KM de Chegada:", 4)
        self.modelo_carro_entry = self.create_field(main_frame, "Modelo do Carro:", 5)
        
        # Frame para organizar os botões
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")
        
        # Botão para calcular e registrar viagem
        calcular_btn = ctk.CTkButton(btn_frame, text="Calcular e Registrar", 
                                   command=self.calcular_viagem)
        calcular_btn.pack(side="left", padx=10, pady=10)
        
        # Botão para limpar todos os campos
        limpar_btn = ctk.CTkButton(btn_frame, text="Limpar Campos", command=self.limpar_campos)
        limpar_btn.pack(side="left", padx=10, pady=10)
        
        # Botão para gerar relatórios
        relatorio_btn = ctk.CTkButton(btn_frame, text="Gerar Relatórios", 
                                    command=self.mostrar_relatorios)
        relatorio_btn.pack(side="left", padx=10, pady=10)
        
        # Label para exibir mensagens de resultado
        self.resultado_label = ctk.CTkLabel(main_frame, text="", 
                                          font=ctk.CTkFont(size=14, weight="bold"))
        self.resultado_label.grid(row=7, column=0, columnspan=2, pady=10)
        
    def create_field(self, parent, label_text, row):
        """Cria um campo de entrada com label
        
        Args:
            parent: Frame pai onde o campo será inserido
            label_text: Texto do label
            row: Linha da grid onde o campo será posicionado
            
        Returns:
            entry: Widget de entrada criado
        """
        # Criar label do campo
        label = ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        
        # Criar campo de entrada
        entry = ctk.CTkEntry(parent, width=300)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        
        # Configurar expansão da coluna
        parent.grid_columnconfigure(1, weight=1)
        
        return entry
    
    def calcular_viagem(self):
        """Valida os dados, calcula a quilometragem e registra a viagem no banco"""
        try:
            # Obter e validar dados dos campos
            nome = self.nome_entry.get().strip()
            setor = self.setor_entry.get().strip()
            destino = self.destino_entry.get().strip()
            km_saida = float(self.km_saida_entry.get())
            km_chegada = float(self.km_chegada_entry.get())
            modelo_carro = self.modelo_carro_entry.get().strip()
            
            # Verificar se todos os campos foram preenchidos
            if not all([nome, setor, destino, modelo_carro]):
                self.resultado_label.configure(text="Por favor, preencha todos os campos!", 
                                             text_color="red")
                return
            
            # Validar se KM de chegada é maior que KM de saída
            if km_chegada < km_saida:
                self.resultado_label.configure(text="KM de chegada deve ser maior que KM de saída!", 
                                             text_color="red")
                return
            
            # Calcular quilometragem percorrida
            km_percorrida = km_chegada - km_saida
            
            # Registrar viagem no banco de dados
            km_percorrida = self.db.inserir_viagem(nome, setor, destino, km_saida, km_chegada, modelo_carro)
            
            # Exibir mensagem de sucesso
            self.resultado_label.configure(
                text=f"Quilometragem percorrida: {km_percorrida:.1f} km", 
                text_color="green"
            )
            
        except ValueError:
            # Tratar erro de conversão de valores numéricos
            self.resultado_label.configure(text="Por favor, insira valores numéricos válidos para KM!", 
                                         text_color="red")
    
    def limpar_campos(self):
        """Limpa todos os campos de entrada e mensagens de resultado"""
        self.nome_entry.delete(0, 'end')
        self.setor_entry.delete(0, 'end')
        self.destino_entry.delete(0, 'end')
        self.km_saida_entry.delete(0, 'end')
        self.km_chegada_entry.delete(0, 'end')
        self.modelo_carro_entry.delete(0, 'end')
        self.resultado_label.configure(text="")
    
    def mostrar_relatorios(self):
        """Exibe janela de seleção de modelo de carro para gerar relatórios"""
        # Obter lista de modelos cadastrados
        modelos = self.db.obter_modelos_carros()
        if not modelos:
            self.resultado_label.configure(text="Nenhum modelo de carro encontrado!", text_color="orange")
            return
        
        # Criar janela de seleção de modelo
        relatorio_window = ctk.CTkToplevel(self.root)
        relatorio_window.title("Gerar Relatórios")
        relatorio_window.geometry("400x300")
        
        # Título da janela
        title = ctk.CTkLabel(relatorio_window, text="Selecione o Modelo do Carro", 
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=20)
        
        # Frame scrollable para lista de modelos
        buttons_frame = ctk.CTkScrollableFrame(relatorio_window)
        buttons_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Criar botão para cada modelo de carro
        for modelo in modelos:
            btn = ctk.CTkButton(buttons_frame, text=modelo, 
                              command=lambda m=modelo: self.mostrar_relatorio_modelo(m, relatorio_window))
            btn.pack(pady=5, fill="x")
    
    def mostrar_relatorio_modelo(self, modelo, parent_window):
        """Exibe relatório detalhado de quilometragem por setor para um modelo específico
        
        Args:
            modelo: Modelo do carro selecionado
            parent_window: Janela pai a ser fechada
        """
        # Fechar janela de seleção
        parent_window.destroy()
        
        # Obter dados do relatório
        relatorio = self.db.obter_relatorio_por_modelo(modelo)
        if not relatorio:
            self.resultado_label.configure(text=f"Nenhum dado encontrado para {modelo}!", text_color="orange")
            return
        
        # Criar janela do relatório
        relatorio_window = ctk.CTkToplevel(self.root)
        relatorio_window.title(f"Relatório - {modelo}")
        relatorio_window.geometry("600x400")
        
        # Frame scrollable para o relatório
        scrollable_frame = ctk.CTkScrollableFrame(relatorio_window)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título do relatório
        header = ctk.CTkLabel(scrollable_frame, text=f"RELATÓRIO DE QUILOMETRAGEM - {modelo}", 
                            font=ctk.CTkFont(size=16, weight="bold"))
        header.pack(pady=10)
        
        # Calcular totais gerais
        total_geral = sum(item["total_km"] for item in relatorio)
        total_viagens = sum(item["total_viagens"] for item in relatorio)
        
        # Frame para resumo geral
        resumo_frame = ctk.CTkFrame(scrollable_frame)
        resumo_frame.pack(fill="x", pady=10, padx=10)
        
        # Exibir resumo geral
        resumo_text = f"Total Geral: {total_geral:.1f} km | Total de Viagens: {total_viagens}"
        resumo_label = ctk.CTkLabel(resumo_frame, text=resumo_text, 
                                  font=ctk.CTkFont(size=14, weight="bold"))
        resumo_label.pack(pady=10)
        
        # Exibir relatório detalhado por setor
        for item in relatorio:
            setor_frame = ctk.CTkFrame(scrollable_frame)
            setor_frame.pack(fill="x", pady=5, padx=10)
            
            # Formatar texto do setor
            setor_text = (f"Setor: {item['setor']} | "
                         f"Quilometragem Total: {item['total_km']:.1f} km | "
                         f"Viagens: {item['total_viagens']}")
            
            setor_label = ctk.CTkLabel(setor_frame, text=setor_text)
            setor_label.pack(pady=10, padx=10)
    
    def run(self):
        """Inicia o loop principal da interface gráfica"""
        self.root.mainloop()

if __name__ == "__main__":
    # Criar e executar o sistema
    app = SistemaKilometragem()
    app.run()