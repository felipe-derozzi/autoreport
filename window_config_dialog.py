import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from config_manager import ConfigManager

class WindowConfigDialog:
    def __init__(self, parent):
        self.dialog = tb.Toplevel(parent)
        self.dialog.title("Configuração das Janelas de Carregamento")
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        
        # Centralizar a janela
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configurar cores
        self.SHOPEE_ORANGE = '#FF5722'
        self.DARK_BG = '#222222'
        self.DARK_TEXT = '#FFFFFF'
        self.DARK_HIGHLIGHT = '#333333'
        
        self.config_manager = ConfigManager()
        self.current_config = self.config_manager.load_config()
        
        # Dicionário para armazenar as variáveis dos campos
        self.field_vars = {}
        
        # Armazenar referência ao canvas
        self.canvas = None
        
        self.create_widgets()
        
        # Vincular evento de fechamento da janela
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        # Frame principal com scrollbar
        container = ttk.Frame(self.dialog)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas com scrollbar
        self.canvas = tk.Canvas(container, bg=self.DARK_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        # Frame que conterá o conteúdo
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Criar janela no canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=540)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar layout
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        title = ttk.Label(
            self.scrollable_frame,
            text="Configuração das Janelas de Carregamento",
            font=('Segoe UI', 14, 'bold'),
            style='warning.TLabel'
        )
        title.pack(pady=(0, 20))
        
        # Frame para cada janela
        for window_key, window_config in self.current_config.items():
            self.create_window_frame(self.scrollable_frame, window_key, window_config)
        
        # Botões
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(pady=20, fill='x')
        
        ttk.Button(
            button_frame,
            text="Salvar",
            style='warning.TButton',
            command=self.save_changes
        ).pack(side='right', padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            style='warning.Outline.TButton',
            command=self.on_closing
        ).pack(side='right', padx=5)
        
        # Configurar scroll com mouse wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        if self.canvas:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
    def on_closing(self):
        """Método chamado quando a janela é fechada"""
        if self.canvas:
            self.canvas.unbind_all("<MouseWheel>")
        self.dialog.destroy()
        
    def create_window_frame(self, parent, window_key, window_config):
        # Criar frame para a janela
        frame = ttk.LabelFrame(
            parent,
            text=window_config['nome'],
            padding="10"
        )
        frame.pack(fill='x', pady=5)
        
        # Grid para os campos
        frame.columnconfigure(1, weight=1)
        
        # Inicializar dicionário para as variáveis desta janela
        self.field_vars[window_key] = {}
        
        # Nome da janela
        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        nome_var = tk.StringVar(value=window_config['nome'])
        self.field_vars[window_key]['nome'] = nome_var
        nome_entry = ttk.Entry(frame, textvariable=nome_var)
        nome_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Horário de início
        ttk.Label(frame, text="Início:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        inicio_var = tk.StringVar(value=window_config['inicio'])
        self.field_vars[window_key]['inicio'] = inicio_var
        inicio_entry = ttk.Entry(frame, textvariable=inicio_var)
        inicio_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        # Horário de fim
        ttk.Label(frame, text="Fim:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        fim_var = tk.StringVar(value=window_config['fim'])
        self.field_vars[window_key]['fim'] = fim_var
        fim_entry = ttk.Entry(frame, textvariable=fim_var)
        fim_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        # Vincular evento de scroll também ao frame
        frame.bind("<MouseWheel>", self._on_mousewheel)
        
    def validate_time_format(self, time_str):
        """Valida o formato da hora (HH:MM)"""
        try:
            if len(time_str.split(':')) != 2:
                return False
            hours, minutes = map(int, time_str.split(':'))
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except:
            return False
            
    def save_changes(self):
        """Salva as alterações nas configurações"""
        new_config = {}
        
        for window_key in self.current_config.keys():
            # Obter valores das variáveis
            nome = self.field_vars[window_key]['nome'].get()
            inicio = self.field_vars[window_key]['inicio'].get()
            fim = self.field_vars[window_key]['fim'].get()
            
            # Validar campos
            if not nome or not inicio or not fim:
                messagebox.showerror(
                    "Erro de Validação",
                    "Todos os campos são obrigatórios!"
                )
                return
                
            # Validar formato das horas
            if not self.validate_time_format(inicio) or not self.validate_time_format(fim):
                messagebox.showerror(
                    "Erro de Validação",
                    "Formato de hora inválido! Use HH:MM"
                )
                return
            
            new_config[window_key] = {
                "nome": nome,
                "inicio": inicio,
                "fim": fim
            }
        
        # Salvar configurações
        if self.config_manager.save_config(new_config):
            messagebox.showinfo(
                "Sucesso",
                "Configurações salvas com sucesso!"
            )
            self.on_closing()
        else:
            messagebox.showerror(
                "Erro",
                "Erro ao salvar as configurações!"
            ) 