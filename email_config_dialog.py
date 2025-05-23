import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb
from email_manager import EmailManager

# Cores da Shopee
SHOPEE_ORANGE = '#FF5722'
SHOPEE_BG = '#F5F5F5'
SHOPEE_SOFT_ORANGE = '#FFF3E6'
SHOPEE_WHITE = '#FFFFFF'
SHOPEE_TEXT = '#222222'
SHOPEE_GRAY = '#757575'

# Cores para o tema escuro
DARK_BG = '#222222'
DARK_TEXT = '#FFFFFF'
DARK_HIGHLIGHT = '#333333'

class EmailConfigDialog:
    def __init__(self, parent):
        self.parent = parent
        self.email_manager = EmailManager()
        self.dialog = None
        self.result = None
        
        # Variáveis para os campos
        self.remetente_email_var = tk.StringVar()
        self.remetente_senha_var = tk.StringVar()
        self.assunto_var = tk.StringVar()
        self.corpo_var = tk.StringVar()
        self.novo_destinatario_var = tk.StringVar()
        
        # Widgets
        self.destinatarios_listbox = None
        self.corpo_text = None
        
    def show(self):
        """Mostra o diálogo de configuração de email"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Configurações de Email")
        self.dialog.geometry("900x900")
        self.dialog.resizable(True, True)
        
        # Configurar estilo
        bg_color = DARK_BG
        section_bg = DARK_BG
        section_fg = DARK_TEXT
        input_bg = DARK_HIGHLIGHT
        input_fg = DARK_TEXT
        
        self.dialog.configure(bg=bg_color)
        
        # Tornar modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centralizar na tela
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (850 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (750 // 2)
        self.dialog.geometry(f"850x750+{x}+{y}")
        
        # Criar interface
        self.create_widgets()
        
        # Carregar configurações existentes
        self.load_current_config()
        
        # Aguardar fechamento do diálogo
        self.dialog.wait_window()
        return self.result
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        bg_color = DARK_BG
        section_bg = DARK_BG
        section_fg = DARK_TEXT
        input_bg = DARK_HIGHLIGHT
        input_fg = DARK_TEXT
        
        # ===== IMPLEMENTAÇÃO DE SCROLL MELHORADA =====
        # Frame container principal
        container = tk.Frame(self.dialog, bg=bg_color)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Canvas para rolagem
        canvas = tk.Canvas(container, bg=bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=bg_color)
        
        # Configurar o scrollable_frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Criar janela do canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configurar scroll
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Função para ajustar largura do frame scrollable
        def configure_canvas(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas.bind('<Configure>', configure_canvas)
        
        # Função para scroll com mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        
        # Bind scroll do mouse para canvas e scrollable_frame
        canvas.bind("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame de conteúdo com padding otimizado
        content_frame = tk.Frame(scrollable_frame, bg=bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Título
        title_label = tk.Label(
            content_frame,
            text="Configurações de Email Automático",
            font=("Arial", 16, "bold"),
            bg=section_bg,
            fg=SHOPEE_ORANGE
        )
        title_label.pack(pady=(0, 15))
        
        # ===== SEÇÃO 1: CONFIGURAÇÕES DO REMETENTE =====
        remetente_frame = tk.LabelFrame(
            content_frame,
            text="Configurações do Remetente (Gmail)",
            font=("Arial", 12, "bold"),
            bg=section_bg,
            fg=SHOPEE_ORANGE,
            relief="groove",
            bd=2
        )
        remetente_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Email do remetente
        tk.Label(
            remetente_frame,
            text="Email:",
            font=("Arial", 10, "bold"),
            bg=section_bg,
            fg=section_fg
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        email_entry = tk.Entry(
            remetente_frame,
            textvariable=self.remetente_email_var,
            font=("Arial", 10),
            bg=input_bg,
            fg=input_fg,
            width=40
        )
        email_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Senha de app do Gmail
        tk.Label(
            remetente_frame,
            text="Senha de App:",
            font=("Arial", 10, "bold"),
            bg=section_bg,
            fg=section_fg
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        senha_entry = tk.Entry(
            remetente_frame,
            textvariable=self.remetente_senha_var,
            font=("Arial", 10),
            show="*",
            bg=input_bg,
            fg=input_fg,
            width=40
        )
        senha_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Botão de teste
        test_btn = tk.Button(
            remetente_frame,
            text="Testar Conexão",
            command=self.testar_conexao,
            bg=SHOPEE_ORANGE,
            fg=SHOPEE_WHITE,
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        test_btn.grid(row=2, column=1, padx=10, pady=8, sticky="e")
        
        # Configurar grid
        remetente_frame.columnconfigure(1, weight=1)
        
        # Info sobre senha de app
        info_label = tk.Label(
            remetente_frame,
            text="⚠️ Use uma Senha de App do Gmail, não sua senha normal!\nAcesse: Conta Google > Segurança > Verificação em duas etapas > Senhas de app",
            font=("Arial", 9),
            bg=section_bg,
            fg=SHOPEE_GRAY,
            justify=tk.LEFT
        )
        info_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 8), sticky="w")
        
        # ===== SEÇÃO 2: DESTINATÁRIOS =====
        destinatarios_frame = tk.LabelFrame(
            content_frame,
            text="Destinatários",
            font=("Arial", 12, "bold"),
            bg=section_bg,
            fg=SHOPEE_ORANGE,
            relief="groove",
            bd=2
        )
        destinatarios_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Adicionar destinatário
        add_frame = tk.Frame(destinatarios_frame, bg=section_bg)
        add_frame.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(
            add_frame,
            text="Novo destinatário:",
            font=("Arial", 10, "bold"),
            bg=section_bg,
            fg=section_fg
        ).pack(side=tk.LEFT)
        
        novo_email_entry = tk.Entry(
            add_frame,
            textvariable=self.novo_destinatario_var,
            font=("Arial", 10),
            bg=input_bg,
            fg=input_fg,
            width=30
        )
        novo_email_entry.pack(side=tk.LEFT, padx=(10, 5))
        
        add_btn = tk.Button(
            add_frame,
            text="Adicionar",
            command=self.adicionar_destinatario,
            bg=SHOPEE_ORANGE,
            fg=SHOPEE_WHITE,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2"
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Lista de destinatários
        list_frame = tk.Frame(destinatarios_frame, bg=section_bg)
        list_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        tk.Label(
            list_frame,
            text="Destinatários cadastrados:",
            font=("Arial", 10, "bold"),
            bg=section_bg,
            fg=section_fg
        ).pack(anchor="w")
        
        # Listbox com scrollbar (altura reduzida para economizar espaço)
        scroll_frame = tk.Frame(list_frame, bg=section_bg)
        scroll_frame.pack(fill=tk.X, pady=5)
        
        list_scrollbar = tk.Scrollbar(scroll_frame)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.destinatarios_listbox = tk.Listbox(
            scroll_frame,
            yscrollcommand=list_scrollbar.set,
            bg=input_bg,
            fg=input_fg,
            selectbackground=SHOPEE_ORANGE,
            font=("Arial", 10),
            height=5  # Reduzido de 6 para 5
        )
        self.destinatarios_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        list_scrollbar.config(command=self.destinatarios_listbox.yview)
        
        # Botão remover
        remove_btn = tk.Button(
            list_frame,
            text="Remover Selecionado",
            command=self.remover_destinatario,
            bg="#F44336",
            fg=SHOPEE_WHITE,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2"
        )
        remove_btn.pack(pady=5)
        
        # ===== SEÇÃO 3: MENSAGEM =====
        mensagem_frame = tk.LabelFrame(
            content_frame,
            text="Configurações da Mensagem",
            font=("Arial", 12, "bold"),
            bg=section_bg,
            fg=SHOPEE_ORANGE,
            relief="groove",
            bd=2
        )
        mensagem_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Assunto
        tk.Label(
            mensagem_frame,
            text="Assunto:",
            font=("Arial", 10, "bold"),
            bg=section_bg,
            fg=section_fg
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        assunto_entry = tk.Entry(
            mensagem_frame,
            textvariable=self.assunto_var,
            font=("Arial", 10),
            bg=input_bg,
            fg=input_fg,
            width=60
        )
        assunto_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Corpo da mensagem
        tk.Label(
            mensagem_frame,
            text="Corpo da mensagem:",
            font=("Arial", 10, "bold"),
            bg=section_bg,
            fg=section_fg
        ).grid(row=1, column=0, sticky="nw", padx=10, pady=5)
        
        text_frame = tk.Frame(mensagem_frame, bg=section_bg)
        text_frame.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        text_scrollbar = tk.Scrollbar(text_frame)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.corpo_text = tk.Text(
            text_frame,
            yscrollcommand=text_scrollbar.set,
            bg=input_bg,
            fg=input_fg,
            font=("Arial", 10),
            height=6,  # Reduzido de 8 para 6
            wrap=tk.WORD
        )
        self.corpo_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.config(command=self.corpo_text.yview)
        
        # Info sobre variáveis
        var_info = tk.Label(
            mensagem_frame,
            text="Variáveis disponíveis: {data_hora}, {janela}",
            font=("Arial", 9),
            bg=section_bg,
            fg=SHOPEE_GRAY
        )
        var_info.grid(row=2, column=1, padx=10, pady=(5, 8), sticky="w")
        
        # Configurar grid
        mensagem_frame.columnconfigure(1, weight=1)
        
        # ===== BOTÕES DE AÇÃO =====
        btn_frame = tk.Frame(content_frame, bg=bg_color)
        btn_frame.pack(fill=tk.X, pady=(15, 20))
        
        # Botão Cancelar
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancelar",
            command=self.cancelar,
            bg=SHOPEE_GRAY,
            fg=SHOPEE_WHITE,
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Botão Salvar
        save_btn = tk.Button(
            btn_frame,
            text="Salvar Configurações",
            command=self.salvar_configuracoes,
            bg="#4CAF50",
            fg=SHOPEE_WHITE,
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        save_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Bind Enter no campo de novo destinatário
        novo_email_entry.bind("<Return>", lambda e: self.adicionar_destinatario())
        
        # Bind do scroll do mouse para todos os widgets relevantes
        def bind_mousewheel(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel(child)
        
        bind_mousewheel(scrollable_frame)
        
        # Atualizar scroll após criação completa
        self.dialog.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def load_current_config(self):
        """Carrega as configurações atuais"""
        config = self.email_manager.load_email_config()
        
        self.remetente_email_var.set(config.get("remetente_email", ""))
        self.remetente_senha_var.set(config.get("remetente_senha", ""))
        self.assunto_var.set(config.get("assunto_padrao", ""))
        
        # Carregar corpo da mensagem
        if self.corpo_text:
            self.corpo_text.delete("1.0", tk.END)
            self.corpo_text.insert("1.0", config.get("corpo_mensagem", ""))
        
        # Carregar destinatários
        self.atualizar_lista_destinatarios()
    
    def atualizar_lista_destinatarios(self):
        """Atualiza a lista de destinatários"""
        if not self.destinatarios_listbox:
            return
            
        self.destinatarios_listbox.delete(0, tk.END)
        config = self.email_manager.load_email_config()
        
        for destinatario in config.get("destinatarios", []):
            self.destinatarios_listbox.insert(tk.END, destinatario)
    
    def testar_conexao(self):
        """Testa a conexão SMTP"""
        email = self.remetente_email_var.get().strip()
        senha = self.remetente_senha_var.get().strip()
        
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha email e senha antes de testar.")
            return
        
        sucesso, mensagem = self.email_manager.testar_conexao(email, senha)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
        else:
            messagebox.showerror("Erro", mensagem)
    
    def adicionar_destinatario(self):
        """Adiciona um novo destinatário"""
        email = self.novo_destinatario_var.get().strip()
        
        if not email:
            messagebox.showerror("Erro", "Digite um email para adicionar.")
            return
        
        sucesso, mensagem = self.email_manager.adicionar_destinatario(email)
        
        if sucesso:
            self.novo_destinatario_var.set("")
            self.atualizar_lista_destinatarios()
            messagebox.showinfo("Sucesso", mensagem)
        else:
            messagebox.showerror("Erro", mensagem)
    
    def remover_destinatario(self):
        """Remove o destinatário selecionado"""
        if not self.destinatarios_listbox.curselection():
            messagebox.showerror("Erro", "Selecione um destinatário para remover.")
            return
        
        index = self.destinatarios_listbox.curselection()[0]
        email = self.destinatarios_listbox.get(index)
        
        if messagebox.askyesno("Confirmar", f"Remover {email} da lista?"):
            sucesso, mensagem = self.email_manager.remover_destinatario(email)
            
            if sucesso:
                self.atualizar_lista_destinatarios()
                messagebox.showinfo("Sucesso", mensagem)
            else:
                messagebox.showerror("Erro", mensagem)
    
    def salvar_configuracoes(self):
        """Salva todas as configurações"""
        # Validar campos obrigatórios
        email = self.remetente_email_var.get().strip()
        senha = self.remetente_senha_var.get().strip()
        assunto = self.assunto_var.get().strip()
        
        if not email:
            messagebox.showerror("Erro", "Email do remetente é obrigatório.")
            return
        
        if not senha:
            messagebox.showerror("Erro", "Senha de app é obrigatória.")
            return
        
        if not assunto:
            messagebox.showerror("Erro", "Assunto é obrigatório.")
            return
        
        # Obter corpo da mensagem
        corpo = ""
        if self.corpo_text:
            corpo = self.corpo_text.get("1.0", tk.END).strip()
        
        if not corpo:
            messagebox.showerror("Erro", "Corpo da mensagem é obrigatório.")
            return
        
        # Verificar se há destinatários
        config = self.email_manager.load_email_config()
        if not config.get("destinatarios", []):
            messagebox.showerror("Erro", "Adicione pelo menos um destinatário.")
            return
        
        # Salvar configurações
        sucesso, mensagem = self.email_manager.atualizar_configuracoes_smtp(
            email, senha, assunto, corpo
        )
        
        if sucesso:
            self.result = True
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            self.dialog.destroy()
        else:
            messagebox.showerror("Erro", mensagem)
    
    def cancelar(self):
        """Cancela e fecha o diálogo"""
        self.result = False
        self.dialog.destroy() 