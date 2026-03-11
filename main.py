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
        self.root.geometry("600x550")
        
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
        
        # Criar campo de mês de referência
        self.mes_entry = self.create_field(main_frame, "Mês de Referência (MM/AAAA):", 0)
        
        # Criar campos de entrada para dados da viagem
        self.nome_entry = self.create_field(main_frame, "Nome do Motorista:", 1)
        self.setor_entry = self.create_field(main_frame, "Setor:", 2)
        self.destino_entry = self.create_field(main_frame, "Local de Destino:", 3)
        self.km_saida_entry = self.create_field(main_frame, "KM de Saída:", 4)
        self.km_chegada_entry = self.create_field(main_frame, "KM de Chegada:", 5)
        self.modelo_carro_entry = self.create_field(main_frame, "Modelo do Carro:", 6)
        
        # Frame para organizar os botões
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20, sticky="ew")
        
        # Botão para calcular e registrar viagem
        calcular_btn = ctk.CTkButton(btn_frame, text="Calcular e Registrar", 
                                   command=self.calcular_viagem)
        calcular_btn.pack(side="left", padx=10, pady=10)
        
        # Botão para limpar todos os campos
        limpar_btn = ctk.CTkButton(btn_frame, text="Limpar Campos", command=self.limpar_campos)
        limpar_btn.pack(side="left", padx=10, pady=10)
        
        # Botão para excluir viagens
        excluir_btn = ctk.CTkButton(btn_frame, text="Excluir Viagem", 
                                   command=self.mostrar_viagens_para_excluir)
        excluir_btn.pack(side="left", padx=10, pady=10)
        
        # Botão para gerar relatórios
        relatorio_btn = ctk.CTkButton(btn_frame, text="Gerar Relatórios", 
                                    command=self.mostrar_selecao_mes)
        relatorio_btn.pack(side="left", padx=10, pady=10)
        
        # Label para exibir mensagens de resultado
        self.resultado_label = ctk.CTkLabel(main_frame, text="", 
                                          font=ctk.CTkFont(size=14, weight="bold"))
        self.resultado_label.grid(row=8, column=0, columnspan=2, pady=10)
        
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
            mes_referencia = self.mes_entry.get().strip()
            nome = self.nome_entry.get().strip()
            setor = self.setor_entry.get().strip()
            destino = self.destino_entry.get().strip()
            km_saida = float(self.km_saida_entry.get())
            km_chegada = float(self.km_chegada_entry.get())
            modelo_carro = self.modelo_carro_entry.get().strip()
            
            # Verificar se todos os campos foram preenchidos
            if not all([mes_referencia, nome, setor, destino, modelo_carro]):
                self.resultado_label.configure(text="Por favor, preencha todos os campos!", 
                                             text_color="red")
                return
            
            # Validar formato do mês (MM/AAAA)
            if len(mes_referencia) != 7 or mes_referencia[2] != '/':
                self.resultado_label.configure(text="Formato de mês inválido! Use MM/AAAA", 
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
            km_percorrida = self.db.inserir_viagem(mes_referencia, nome, setor, destino, km_saida, km_chegada, modelo_carro)
            
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
        self.mes_entry.delete(0, 'end')
        self.nome_entry.delete(0, 'end')
        self.setor_entry.delete(0, 'end')
        self.destino_entry.delete(0, 'end')
        self.km_saida_entry.delete(0, 'end')
        self.km_chegada_entry.delete(0, 'end')
        self.modelo_carro_entry.delete(0, 'end')
        self.resultado_label.configure(text="")
    
    def mostrar_viagens_para_excluir(self):
        """Exibe janela com lista de viagens para exclusão"""
        # Obter todas as viagens
        viagens = self.db.obter_todas_viagens()
        if not viagens:
            self.resultado_label.configure(text="Nenhuma viagem registrada!", text_color="orange")
            return
        
        # Criar janela de exclusão
        excluir_window = ctk.CTkToplevel(self.root)
        excluir_window.title("Excluir Viagem")
        excluir_window.geometry("900x500")
        
        # Título
        title = ctk.CTkLabel(excluir_window, text="Selecione a viagem para excluir", 
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=20)
        
        # Frame scrollable para lista de viagens
        scrollable_frame = ctk.CTkScrollableFrame(excluir_window)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Listar viagens com botão de exclusão
        for viagem in viagens:
            viagem_frame = ctk.CTkFrame(scrollable_frame)
            viagem_frame.pack(fill="x", pady=5, padx=10)
            
            # Informações da viagem
            info_text = (f"ID: {viagem['id']} | Mês: {viagem['mes_referencia']} | {viagem['data']} | "
                        f"{viagem['motorista']} ({viagem['setor']}) | Destino: {viagem['destino']} | "
                        f"{viagem['modelo_carro']} | KM: {viagem['km_saida']:.1f} → {viagem['km_chegada']:.1f} "
                        f"(Percorrida: {viagem['km_percorrida']:.1f} km)")
            
            info_label = ctk.CTkLabel(viagem_frame, text=info_text, wraplength=750)
            info_label.pack(side="left", pady=10, padx=10)
            
            # Botão de exclusão
            excluir_btn = ctk.CTkButton(viagem_frame, text="Excluir", width=80,
                                       command=lambda v_id=viagem['id'], w=excluir_window: self.excluir_viagem(v_id, w))
            excluir_btn.pack(side="right", padx=10)
    
    def excluir_viagem(self, viagem_id, window):
        """Exclui uma viagem do banco de dados
        
        Args:
            viagem_id: ID da viagem a ser excluída
            window: Janela a ser fechada após exclusão
        """
        # Confirmar exclusão
        if self.db.excluir_viagem(viagem_id):
            self.resultado_label.configure(text="Viagem excluída com sucesso!", text_color="green")
            window.destroy()
        else:
            self.resultado_label.configure(text="Erro ao excluir viagem!", text_color="red")
    
    def mostrar_selecao_mes(self):
        """Exibe janela de seleção de mês para relatórios"""
        # Obter meses disponíveis
        meses = self.db.obter_meses_disponiveis()
        if not meses:
            self.resultado_label.configure(text="Nenhum mês com registros encontrado!", text_color="orange")
            return
        
        # Criar janela de seleção de mês
        mes_window = ctk.CTkToplevel(self.root)
        mes_window.title("Selecionar Mês")
        mes_window.geometry("400x400")
        
        # Título
        title = ctk.CTkLabel(mes_window, text="Selecione o Mês de Referência", 
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=20)
        
        # Frame scrollable para lista de meses
        buttons_frame = ctk.CTkScrollableFrame(mes_window)
        buttons_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botão para cada mês
        for mes in meses:
            btn = ctk.CTkButton(buttons_frame, text=mes, 
                              command=lambda m=mes: self.mostrar_modelos_por_mes(m, mes_window))
            btn.pack(pady=5, fill="x")
    
    def mostrar_modelos_por_mes(self, mes_referencia, parent_window):
        """Exibe janela de seleção de modelo de carro filtrado por mês
        
        Args:
            mes_referencia: Mês selecionado
            parent_window: Janela pai a ser fechada
        """
        parent_window.destroy()
        
        # Obter modelos do mês selecionado
        modelos = self.db.obter_modelos_carros(mes_referencia)
        if not modelos:
            self.resultado_label.configure(text=f"Nenhum modelo encontrado para {mes_referencia}!", text_color="orange")
            return
        
        # Criar janela de seleção de modelo
        modelo_window = ctk.CTkToplevel(self.root)
        modelo_window.title(f"Modelos - {mes_referencia}")
        modelo_window.geometry("400x400")
        
        # Título
        title = ctk.CTkLabel(modelo_window, text=f"Selecione o Modelo do Carro\nMês: {mes_referencia}", 
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=20)
        
        # Frame scrollable para lista de modelos
        buttons_frame = ctk.CTkScrollableFrame(modelo_window)
        buttons_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botão para cada modelo
        for modelo in modelos:
            btn = ctk.CTkButton(buttons_frame, text=modelo, 
                              command=lambda m=modelo: self.mostrar_relatorio_modelo(m, mes_referencia, modelo_window))
            btn.pack(pady=5, fill="x")
    
    def mostrar_relatorio_modelo(self, modelo, mes_referencia, parent_window):
        """Exibe relatório detalhado de quilometragem por setor para um modelo específico
        
        Args:
            modelo: Modelo do carro selecionado
            mes_referencia: Mês de referência
            parent_window: Janela pai a ser fechada
        """
        # Fechar janela de seleção
        parent_window.destroy()
        
        # Obter dados do relatório
        relatorio = self.db.obter_relatorio_por_modelo(modelo, mes_referencia)
        if not relatorio:
            self.resultado_label.configure(text=f"Nenhum dado encontrado para {modelo} em {mes_referencia}!", text_color="orange")
            return
        
        # Criar janela do relatório
        relatorio_window = ctk.CTkToplevel(self.root)
        relatorio_window.title(f"Relatório - {modelo} - {mes_referencia}")
        relatorio_window.geometry("600x400")
        
        # Frame scrollable para o relatório
        scrollable_frame = ctk.CTkScrollableFrame(relatorio_window)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título do relatório
        header = ctk.CTkLabel(scrollable_frame, text=f"RELATÓRIO DE QUILOMETRAGEM\n{modelo} - {mes_referencia}", 
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
