import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import ttkbootstrap as tb
import os
import threading
import sys
import pandas as pd
from config_manager import ConfigManager
from window_config_dialog import WindowConfigDialog
from email_manager import EmailManager
from email_config_dialog import EmailConfigDialog

# Cores da Shopee
SHOPEE_ORANGE = '#FF5722'
SHOPEE_BG = '#F5F5F5'
SHOPEE_SOFT_ORANGE = '#FFF3E6'  # Laranja suave para fundo
SHOPEE_WHITE = '#FFFFFF'
SHOPEE_TEXT = '#222222'
SHOPEE_GRAY = '#757575'

# Cores para o tema escuro (agora padrão)
DARK_BG = '#222222'
DARK_TEXT = '#FFFFFF'
DARK_HIGHLIGHT = '#333333'

# Variável para controlar o tema atual
tema_escuro = False

# ===== CONTROLE DE JANELAS MODAIS =====
janela_modal_aberta = False

# Variáveis globais para elementos da UI
root = None
scroll_canvas = None
main_frame = None
top_frame = None
title_frame = None
title = None
logo_label = None
conferencia_label = None
output_dir_label = None
info_text = None
placeholder_text = None
status_label = None
expedicao_var = None
conferencia_var = None
output_dir_var = None
expedicao_listbox = None
conferencia_listbox = None
window_label = None
window_var = None

# Função para atualizar toda a interface
def atualizar_interface(root=None, scroll_canvas=None, main_frame=None, 
                                  top_frame=None, title_frame=None, title=None, logo_label=None, 
                                  conferencia_label=None, output_dir_label=None, 
                                  info_text=None, placeholder_text=None, status_label=None):
    if not all([root, scroll_canvas, main_frame, top_frame]):
        return
        
    # Configurar cores base
    bg_color = DARK_BG
    section_bg = DARK_BG
    section_fg = DARK_TEXT
    title_color = SHOPEE_ORANGE
    
    # Cores para campos de entrada
    input_bg = DARK_HIGHLIGHT
    input_fg = DARK_TEXT
    
    # Atualizar elementos principais
    root.configure(bg=bg_color)
    scroll_canvas.configure(bg=bg_color)
    main_frame.configure(bg=bg_color)
    top_frame.configure(bg=bg_color)
    
    # Atualizar cabeçalho
    if all([title_frame, title, logo_label]):
        title_frame.configure(bg=section_bg)
        title.configure(bg=section_bg, fg=SHOPEE_ORANGE)
        logo_label.configure(bg=section_bg)
    
    # Atualizar todos os frames e seus conteúdos
    for widget in main_frame.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.configure(bg=section_bg)
            
            # Atualizar elementos dentro do frame
            for child in widget.winfo_children():
                # Atualizar labels
                if isinstance(child, tk.Label) and not isinstance(child, ttk.Label):
                    if conferencia_label and output_dir_label and child not in [conferencia_label, output_dir_label]:
                        child.configure(bg=section_bg, fg=section_fg)
                
                # Atualizar campos de entrada (labels de informação)
                if conferencia_label and output_dir_label and child in [conferencia_label, output_dir_label]:
                    child.configure(bg=input_bg, fg=input_fg)
                
                # Atualizar Listbox
                if isinstance(child, tk.Listbox):
                    child.configure(bg=input_bg, fg=input_fg, selectbackground=SHOPEE_ORANGE)
                
                # Atualizar Text
                if isinstance(child, tk.Text):
                    child.configure(bg=input_bg, fg=input_fg)
    
    # Atualizar status label
    if status_label:
        current_fg = status_label.cget("foreground")
        status_label.configure(bg=section_bg)
        if current_fg and current_fg != "":
            status_label.configure(fg=current_fg)
    
    # Atualizar o campo de informações adicionais
    if info_text and placeholder_text:
        is_placeholder = info_text.get("1.0", "end-1c").strip() == placeholder_text
        if is_placeholder:
            info_text.config(fg=SHOPEE_GRAY, bg=input_bg)
        else:
            info_text.config(fg=input_fg, bg=input_bg)

# ===== SISTEMA DE SCROLL UNIVERSAL =====
def bind_mousewheel_to_all(widget, canvas):
    """Vincula o evento de scroll do mouse a um widget e todos os seus filhos"""
    def _on_mousewheel(event):
        if canvas and canvas.winfo_exists():
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
            except:
                pass  # Ignorar erros se o canvas não estiver mais disponível
    
    # Vincular ao widget atual
    try:
        widget.bind("<MouseWheel>", _on_mousewheel)
    except:
        pass
    
    # Vincular a todos os widgets filhos recursivamente
    try:
        for child in widget.winfo_children():
            bind_mousewheel_to_all(child, canvas)
    except:
        pass

def aplicar_scroll_universal():
    """Aplica scroll universal a todos os widgets da janela"""
    if scroll_canvas and scroll_canvas.winfo_exists():
        # Vincular scroll à janela principal e todos os widgets
        bind_mousewheel_to_all(root, scroll_canvas)
        bind_mousewheel_to_all(main_frame, scroll_canvas)
        
        # Garantir que novos widgets também tenham scroll
        def on_widget_added(event):
            if event.widget != main_frame:
                bind_mousewheel_to_all(event.widget, scroll_canvas)
        
        # Vincular evento de adição de novos widgets
        main_frame.bind('<Map>', on_widget_added, add='+')

def reaplicar_scroll_universal():
    """Reaplica o scroll universal - útil após adicionar novos widgets"""
    global janela_modal_aberta
    
    if scroll_canvas and scroll_canvas.winfo_exists():
        try:
            # Se uma janela modal está aberta, não aplicar scroll na janela principal
            if janela_modal_aberta:
                print("⏸️ Janela modal aberta - scroll da janela principal pausado")
                return
            
            # Verificar se a janela principal está em foco antes de aplicar
            if root.focus_get() is not None and str(root.focus_get()).startswith(str(root)):
                bind_mousewheel_to_all(root, scroll_canvas)
                bind_mousewheel_to_all(main_frame, scroll_canvas)
                print("✅ Scroll universal reaplicado na janela principal")
            else:
                print("⏭️ Janela principal não está em foco - scroll não reaplicado")
        except Exception as e:
            print(f"⚠️ Erro ao reaplicar scroll universal: {e}")

def get_window_key_from_display(display_text):
    """Extrai a chave da janela do texto de exibição"""
    if "Manhã" in display_text or "AM" in display_text:
        return "MANHA"
    elif "Tarde" in display_text or "SD" in display_text:
        return "TARDE"
    elif "Noite" in display_text or "PM" in display_text:
        return "NOITE"
    return None

def processar(expedicao_files, conferencia_file, output_dir, info_adicional, status_label, window_var):
    try:
        from analise_relatorios import main as processar_relatorio
        
        # Validar arquivos de expedição
        for f in expedicao_files:
            if not os.path.exists(f):
                raise FileNotFoundError(f"Arquivo de expedição não encontrado: {os.path.basename(f)}")
                
        # Validar arquivo de conferência
        if not os.path.exists(conferencia_file):
            raise FileNotFoundError("Arquivo de conferência não encontrado")
            
        # Validar diretório de saída
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Obter janela selecionada
        window_display = window_var.get()
        if window_display == "Selecione a Janela de Carregamento":
            raise ValueError("Por favor, selecione a janela de carregamento!")
            
        window_key = get_window_key_from_display(window_display)
        if not window_key:
            raise ValueError("Janela de carregamento inválida!")
            
        status_label.config(text='Processando...', foreground=SHOPEE_ORANGE)
        root.update()  # Forçar atualização da interface
        
        # Chama a função principal do script, passando os arquivos e diretório
        processar_relatorio(expedicao_files, conferencia_file, output_dir, info_adicional, window_key)
        
        # Mostrar mensagem de sucesso com detalhes
        msg = 'Relatórios gerados com sucesso!\n'
        msg += f'Local: {output_dir}'
        status_label.config(text=msg, foreground='#4CAF50')
        
        # ===== ENVIO AUTOMÁTICO DE EMAIL =====
        try:
            email_manager = EmailManager()
            config = email_manager.load_email_config()
            
            # Verificar se o email está configurado e tem destinatários
            if (config.get("remetente_email") and 
                config.get("remetente_senha") and 
                config.get("destinatarios")):
                
                print("📧 Iniciando envio automático de email...")
                
                status_label.config(text='Enviando email...', foreground=SHOPEE_ORANGE)
                root.update()
                
                # Definir caminhos dos arquivos gerados
                pdf_path = os.path.join(output_dir, 'relatorio_expedicao.pdf')
                csv_path = os.path.join(output_dir, 'resumo_expedicao.csv')
                xlsx_path = os.path.join(output_dir, 'relatorio_expedicao.xlsx')
                
                # Obter informação da janela para o email
                config_manager = ConfigManager()
                window_config = config_manager.load_config().get(window_key, {})
                janela_info = ""
                if window_config:
                    janela_info = config_manager.format_window_display(window_key, window_config)
                
                # Enviar email
                sucesso_email, mensagem_email = email_manager.enviar_email_relatorio(
                    pdf_path=pdf_path,
                    csv_path=csv_path, 
                    xlsx_path=xlsx_path,
                    janela_info=janela_info,
                    info_adicional=info_adicional
                )
                
                if sucesso_email:
                    print(f"✅ Email enviado com sucesso!")
                    status_label.config(text=f'{msg}\n✉️ Email enviado com sucesso!', foreground='#4CAF50')
                    messagebox.showinfo(
                        'Sucesso Completo', 
                        f'Relatórios gerados e email enviado com sucesso!\n\n'
                        f'📁 Local: {output_dir}\n'
                        f'✉️ {mensagem_email}\n\n'
                        f'Deseja abrir a pasta?'
                    )
                else:
                    print(f"❌ Falha no envio de email: {mensagem_email}")
                    status_label.config(text=f'{msg}\n⚠️ Erro no envio do email', foreground='#FF9800')
                    if messagebox.askyesno(
                        'Relatórios Gerados', 
                        f'Relatórios gerados com sucesso, mas houve um erro no envio do email:\n\n'
                        f'❌ {mensagem_email}\n\n'
                        f'💡 Verifique as configurações de email (credenciais, senha de app do Gmail).\n\n'
                        f'Deseja abrir a pasta dos relatórios?'
                    ):
                        os.startfile(output_dir) if os.name == 'nt' else os.system(f'xdg-open "{output_dir}"')
                    return
            else:
                print("⚠️ Configurações de email incompletas - envio automático desabilitado")
                
                # Email não configurado - apenas notificar
                if messagebox.askyesno(
                    'Relatórios Gerados', 
                    f'Relatórios gerados com sucesso!\n\n'
                    f'📁 Local: {output_dir}\n\n'
                    f'ℹ️ Email automático não configurado.\n'
                    f'Configure em "Configurações de Email" para envio automático.\n\n'
                    f'Deseja abrir a pasta?'
                ):
                    os.startfile(output_dir) if os.name == 'nt' else os.system(f'xdg-open "{output_dir}"')
                return
                
        except Exception as e:
            # Erro no sistema de email - relatórios foram gerados com sucesso
            print(f"❌ Erro no sistema de email: {str(e)}")
            
            status_label.config(text=f'{msg}\n⚠️ Erro no sistema de email', foreground='#FF9800')
            if messagebox.askyesno(
                'Relatórios Gerados', 
                f'Relatórios gerados com sucesso, mas houve um erro no sistema de email:\n\n'
                f'❌ {str(e)}\n\n'
                f'💡 Verifique as configurações de email (credenciais, conexão com internet).\n\n'
                f'Deseja abrir a pasta dos relatórios?'
            ):
                os.startfile(output_dir) if os.name == 'nt' else os.system(f'xdg-open "{output_dir}"')
            return
        
        # Perguntar se deseja abrir o diretório (apenas se email foi enviado com sucesso)
        if messagebox.askyesno('Sucesso', 'Deseja abrir a pasta dos relatórios?'):
            os.startfile(output_dir) if os.name == 'nt' else os.system(f'xdg-open "{output_dir}"')
        
    except Exception as e:
        erro = str(e)
        # Formatar mensagens de erro comuns
        if "não contém as colunas necessárias" in erro:
            erro = "Arquivo de conferência inválido!\nFaltam colunas necessárias."
        elif "está vazio" in erro:
            erro = "O arquivo de conferência está vazio!"
        elif "formato está correto" in erro:
            erro = "Formato do arquivo de conferência inválido!\nVerifique se é um CSV válido."
            
        status_label.config(text=f'Erro: {erro}', foreground='#F44336')
        messagebox.showerror('Erro', f'Ocorreu um erro ao gerar os relatórios:\n\n{erro}')

def selecionar_expedicao():
    global expedicao_var, expedicao_listbox, status_label
    files = filedialog.askopenfilenames(
        title='Selecione os arquivos de expedição',
        filetypes=[('Arquivos CSV', '*.csv')]
    )
    
    if files:
        try:
            # Importar função de validação
            from analise_relatorios import validar_arquivo_expedicao
            
            # Obter arquivos já existentes na lista
            arquivos_existentes = []
            for i in range(expedicao_listbox.size()):
                arquivo = expedicao_listbox.get(i)
                if not arquivo.endswith(')'):  # Ignorar arquivos com erro
                    arquivos_existentes.append(arquivo)
            
            # Validar cada arquivo novo
            arquivos_validos = []
            for file in files:
                nome_arquivo = os.path.basename(file)
                if nome_arquivo in arquivos_existentes:
                    continue  # Pular arquivos que já estão na lista
                    
                valido, mensagem = validar_arquivo_expedicao(file)
                if valido:
                    arquivos_validos.append(file)
                    expedicao_listbox.insert(tk.END, nome_arquivo)
                    expedicao_listbox.itemconfig(tk.END, {'fg': '#4CAF50'})  # Verde para arquivos válidos
                else:
                    expedicao_listbox.insert(tk.END, f"{nome_arquivo} (ERRO: {mensagem})")
                    expedicao_listbox.itemconfig(tk.END, {'fg': '#F44336'})  # Vermelho para arquivos inválidos
            
            # Atualizar a variável com todos os arquivos válidos (existentes + novos)
            todos_arquivos_validos = []
            for i in range(expedicao_listbox.size()):
                arquivo = expedicao_listbox.get(i)
                if not arquivo.endswith(')'):  # Ignorar arquivos com erro
                    # Se for um arquivo existente, usar o caminho completo
                    if arquivo in arquivos_existentes:
                        for f in expedicao_var.get().split(";"):
                            if arquivo == os.path.basename(f):
                                todos_arquivos_validos.append(f)
                                break
                    else:  # Se for um arquivo novo
                        for f in arquivos_validos:
                            if arquivo == os.path.basename(f):
                                todos_arquivos_validos.append(f)
                                break
            
            if todos_arquivos_validos:
                expedicao_var.set(";".join(todos_arquivos_validos))
                status_label.config(
                    text=f'{len(todos_arquivos_validos)} arquivo(s) válido(s) na lista',
                    foreground='#4CAF50'
                )
            else:
                expedicao_var.set('')
                status_label.config(
                    text='Nenhum arquivo válido na lista',
                    foreground='#F44336'
                )
                
        except Exception as e:
            status_label.config(
                text=f'Erro ao validar arquivos: {str(e)}',
                foreground='#F44336'
            )
            messagebox.showerror('Erro', f'Erro ao validar os arquivos:\n\n{str(e)}')
    else:
        if expedicao_listbox.size() == 0:
            status_label.config(
                text='Nenhum arquivo selecionado',
                foreground=DARK_TEXT
            )

def selecionar_conferencia():
    global conferencia_var, conferencia_listbox, status_label
    files = filedialog.askopenfilenames(
        title='Selecione os arquivos de conferência',
        filetypes=[('Arquivos CSV', '*.csv')]
    )
    
    if files:
        try:
            # Importar função de validação
            from analise_relatorios import validar_arquivo_conferencia
            
            # Obter arquivos já existentes na lista
            arquivos_existentes = []
            for i in range(conferencia_listbox.size()):
                arquivo = conferencia_listbox.get(i)
                if not arquivo.endswith(')'):  # Ignorar arquivos com erro
                    arquivos_existentes.append(arquivo)
            
            # Validar cada arquivo novo
            arquivos_validos = []
            for file in files:
                nome_arquivo = os.path.basename(file)
                if nome_arquivo in arquivos_existentes:
                    continue  # Pular arquivos que já estão na lista
                    
            valido, mensagem = validar_arquivo_conferencia(file)
            if valido:
                    arquivos_validos.append(file)
                    conferencia_listbox.insert(tk.END, nome_arquivo)
                    conferencia_listbox.itemconfig(tk.END, {'fg': '#4CAF50'})  # Verde para arquivos válidos
            else:
                conferencia_listbox.insert(tk.END, f"{nome_arquivo} (ERRO: {mensagem})")
                conferencia_listbox.itemconfig(tk.END, {'fg': '#F44336'})  # Vermelho para arquivos inválidos
            
            # Atualizar a variável com todos os arquivos válidos (existentes + novos)
            todos_arquivos_validos = []
            for i in range(conferencia_listbox.size()):
                arquivo = conferencia_listbox.get(i)
                if not arquivo.endswith(')'):  # Ignorar arquivos com erro
                    # Se for um arquivo existente, usar o caminho completo
                    if arquivo in arquivos_existentes:
                        for f in conferencia_var.get().split(";"):
                            if arquivo == os.path.basename(f):
                                todos_arquivos_validos.append(f)
                                break
                    else:  # Se for um arquivo novo
                        for f in arquivos_validos:
                            if arquivo == os.path.basename(f):
                                todos_arquivos_validos.append(f)
                                break
            
            if todos_arquivos_validos:
                conferencia_var.set(";".join(todos_arquivos_validos))
                status_label.config(
                    text=f'{len(todos_arquivos_validos)} arquivo(s) válido(s) na lista',
                    foreground='#4CAF50'
                )
            else:
                conferencia_var.set('')
                status_label.config(
                    text='Nenhum arquivo válido na lista',
                    foreground='#F44336'
                )
                
        except Exception as e:
            status_label.config(
                text=f'Erro ao validar arquivos: {str(e)}',
                foreground='#F44336'
            )
            messagebox.showerror('Erro', f'Erro ao validar os arquivos:\n\n{str(e)}')
    else:
        if conferencia_listbox.size() == 0:
            status_label.config(
            text='Nenhum arquivo selecionado',
            foreground=DARK_TEXT
        )

def selecionar_diretorio():
    global output_dir_var, output_dir_label
    dir_ = filedialog.askdirectory(title='Selecione o diretório de saída')
    output_dir_var.set(dir_)
    output_dir_label.config(text=dir_ if dir_ else 'Nenhum diretório selecionado')

def on_gerar():
    global expedicao_var, conferencia_var, output_dir_var, info_text, placeholder_text, status_label, window_var
    expedicao_files_str = expedicao_var.get()
    conferencia_files_str = conferencia_var.get()
    output_dir = output_dir_var.get()
    
    # Converter strings de arquivos em listas
    expedicao_files = expedicao_files_str.split(";") if expedicao_files_str else []
    conferencia_files = conferencia_files_str.split(";") if conferencia_files_str else []
    
    # Verificar se o texto é o placeholder antes de obter o valor
    if info_text.get('1.0', 'end').strip() == placeholder_text:
        info_adicional = ""
    else:
        info_adicional = info_text.get('1.0', 'end').strip()
    
    if not expedicao_files or not conferencia_files or not output_dir:
        status_label.config(text='Selecione todos os arquivos e diretório!', foreground='#F44336')
        return
        
    # Rodar processamento em thread separada para não travar a GUI
    threading.Thread(
        target=processar,
        args=(expedicao_files, conferencia_files[0], output_dir, info_adicional, status_label, window_var),  # Por enquanto, usando apenas o primeiro arquivo de conferência
        daemon=True
    ).start()

# Função para criar frames de seção
def create_section_frame(parent, title_text):
    frame = tk.Frame(parent, bg=DARK_BG)
    frame.pack(pady=15, fill='x')
    
    label = tk.Label(
        frame,
        text=title_text,
        font=('Segoe UI', 12, 'bold'),
        bg=DARK_BG,
        fg=DARK_TEXT
    )
    label.pack(anchor='w')
    
    return frame

def abrir_configuracao():
    global janela_modal_aberta
    
    # Marcar que uma janela modal está sendo aberta
    janela_modal_aberta = True
    print("🔍 Abrindo janela modal - scroll da janela principal será pausado")
    
    dialog = WindowConfigDialog(root)
    dialog.show()
    
    # Marcar que a janela modal foi fechada
    janela_modal_aberta = False
    
    # Após fechar o diálogo, restaurar foco e scroll na janela principal
    root.focus_set()
    root.after(100, lambda: print("🔍 Janela modal fechada - restaurando foco"))
    root.after(200, reaplicar_scroll_universal)

def abrir_configuracao_email():
    """Abre o diálogo de configuração de email"""
    global janela_modal_aberta
    
    # Marcar que uma janela modal está sendo aberta
    janela_modal_aberta = True
    print("🔍 Abrindo janela modal de email - scroll da janela principal será pausado")
    
    dialog = EmailConfigDialog(root)
    resultado = dialog.show()
    
    # Marcar que a janela modal foi fechada
    janela_modal_aberta = False
    
    # Após fechar o diálogo, restaurar foco e scroll na janela principal
    root.focus_set()
    root.after(100, lambda: print("🔍 Janela modal de email fechada - restaurando foco"))
    root.after(200, reaplicar_scroll_universal)
    
    if resultado:
        # Configuração salva com sucesso
        messagebox.showinfo(
            "Email Configurado", 
            "Configurações de email salvas com sucesso!\n\n"
            "O sistema agora enviará automaticamente os relatórios por email "
            "após cada processamento."
        )

def atualizar_janela_atual():
    global window_label
    config_manager = ConfigManager()
    window_key, window_config = config_manager.get_current_window()
    
    if window_config:
        window_label.config(
            text=config_manager.format_window_display(window_key, window_config),
            foreground='#4CAF50'
        )
    else:
        window_label.config(
            text="Fora do horário de expedição",
            foreground='#F44336'
        )
    
    # Agendar próxima atualização em 1 minuto
    root.after(60000, atualizar_janela_atual)

def remover_selecionados_expedicao():
    global expedicao_var, expedicao_listbox, status_label
    selecionados = expedicao_listbox.curselection()
    if not selecionados:
        return

    # Obter os caminhos completos dos arquivos
    caminhos_completos = expedicao_var.get().split(";") if expedicao_var.get() else []
    
    # Criar um conjunto de índices selecionados para busca mais rápida
    indices_selecionados = set(selecionados)
    
    # Criar listas para manter apenas os itens não selecionados
    novos_caminhos = []
    nomes_mantidos = []
    
    # Iterar sobre todos os itens da listbox
    for i in range(expedicao_listbox.size()):
        if i not in indices_selecionados:
            nome_arquivo = expedicao_listbox.get(i)
            nomes_mantidos.append(nome_arquivo)
            # Manter apenas os caminhos dos arquivos válidos
            if not nome_arquivo.endswith(')'):
                for caminho in caminhos_completos:
                    if os.path.basename(caminho) == nome_arquivo:
                        novos_caminhos.append(caminho)
                        break
    
    # Limpar a listbox
    expedicao_listbox.delete(0, tk.END)
    
    # Reinsere os itens mantidos
    for nome in nomes_mantidos:
        expedicao_listbox.insert(tk.END, nome)
        # Restaurar a cor do item
        if nome.endswith(')'): # Se for um arquivo com erro
            expedicao_listbox.itemconfig(tk.END, {'fg': '#F44336'})
        else:
            expedicao_listbox.itemconfig(tk.END, {'fg': '#4CAF50'})
    
    # Atualizar a variável com os caminhos restantes
    expedicao_var.set(";".join(novos_caminhos))
    
    # Atualizar status
    arquivos_validos = len([nome for nome in nomes_mantidos if not nome.endswith(')')])
    if arquivos_validos > 0:
        status_label.config(
            text=f'{arquivos_validos} arquivo(s) válido(s) na lista',
            foreground='#4CAF50'
        )
    else:
        status_label.config(
            text='Nenhum arquivo selecionado',
            foreground=DARK_TEXT
        )

def remover_selecionados_conferencia():
    global conferencia_var, conferencia_listbox, status_label
    selecionados = conferencia_listbox.curselection()
    if not selecionados:
        return

    # Obter os caminhos completos dos arquivos
    caminhos_completos = conferencia_var.get().split(";") if conferencia_var.get() else []
    
    # Criar um conjunto de índices selecionados para busca mais rápida
    indices_selecionados = set(selecionados)
    
    # Criar listas para manter apenas os itens não selecionados
    novos_caminhos = []
    nomes_mantidos = []
    
    # Iterar sobre todos os itens da listbox
    for i in range(conferencia_listbox.size()):
        if i not in indices_selecionados:
            nome_arquivo = conferencia_listbox.get(i)
            nomes_mantidos.append(nome_arquivo)
            # Manter apenas os caminhos dos arquivos válidos
            if not nome_arquivo.endswith(')'):
                for caminho in caminhos_completos:
                    if os.path.basename(caminho) == nome_arquivo:
                        novos_caminhos.append(caminho)
                        break
    
    # Limpar a listbox
    conferencia_listbox.delete(0, tk.END)
    
    # Reinsere os itens mantidos
    for nome in nomes_mantidos:
        conferencia_listbox.insert(tk.END, nome)
        # Restaurar a cor do item
        if nome.endswith(')'): # Se for um arquivo com erro
            conferencia_listbox.itemconfig(tk.END, {'fg': '#F44336'})
        else:
            conferencia_listbox.itemconfig(tk.END, {'fg': '#4CAF50'})
    
    # Atualizar a variável com os caminhos restantes
    conferencia_var.set(";".join(novos_caminhos))
    
    # Atualizar status
    arquivos_validos = len([nome for nome in nomes_mantidos if not nome.endswith(')')])
    if arquivos_validos > 0:
        status_label.config(
            text=f'{arquivos_validos} arquivo(s) válido(s) na lista',
            foreground='#4CAF50'
        )
    else:
        status_label.config(
            text='Nenhum arquivo selecionado',
            foreground=DARK_TEXT
        )

# ===== SISTEMA DE GERENCIAMENTO DE FOCO =====
def configurar_gerenciamento_foco():
    """Configura o sistema de gerenciamento de foco para scroll inteligente"""
    
    def on_focus_in(event):
        """Quando a janela principal ganha foco"""
        global janela_modal_aberta
        if event.widget == root and not janela_modal_aberta:
            print("🔍 Janela principal ganhou foco")
            root.after(100, reaplicar_scroll_universal)  # Pequeno delay para estabilizar
    
    def on_focus_out(event):
        """Quando a janela principal perde foco"""
        if event.widget == root:
            print("🔍 Janela principal perdeu foco")
    
    # Vincular eventos de foco
    root.bind('<FocusIn>', on_focus_in)
    root.bind('<FocusOut>', on_focus_out)
    
    # Também vincular ao clique na janela para garantir foco
    def on_click_window(event):
        """Quando usuário clica na janela"""
        global janela_modal_aberta
        if not janela_modal_aberta:
            root.focus_set()
            root.after(50, reaplicar_scroll_universal)
    
    root.bind('<Button-1>', on_click_window, add='+')

# Inicializar a interface
def inicializar_interface():
    global root, scroll_canvas, main_frame, top_frame, title_frame, title, logo_label
    global conferencia_label, output_dir_label, info_text, placeholder_text, status_label
    global expedicao_var, conferencia_var, output_dir_var, expedicao_listbox, conferencia_listbox, window_label, window_var

    # GUI principal com tema escuro
    root = tb.Window(themename='darkly')  # Usando tema escuro do ttkbootstrap
    root.title('Relatório de Expedição - Shopee Xpress')
    
    # Configurar tamanho inicial sem posição
    window_width = 900
    window_height = 1000
    root.geometry(f'{window_width}x{window_height}')
    root.configure(bg=DARK_BG)

    # Ícone da janela Shopee
    try:
        root.iconbitmap('icons8-comprador-16.ico')
    except Exception as e:
        print('Não foi possível definir o ícone da janela:', e)

    # ===== CENTRALIZAR JANELA NA TELA =====
    def centralizar_janela():
        """Centraliza a janela principal na tela - funciona para qualquer resolução"""
        try:
            # Atualizar widgets para obter dimensões corretas
            root.update_idletasks()
            
            # Obter dimensões da tela
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            print(f"📱 Resolução da tela detectada: {screen_width}x{screen_height}")
            
            # Verificar se a janela é maior que a tela disponível
            available_width = screen_width * 0.95  # 95% da largura da tela
            available_height = screen_height * 0.90  # 90% da altura da tela (deixar espaço para barra de tarefas)
            
            # Ajustar tamanho da janela se necessário
            final_width = min(window_width, int(available_width))
            final_height = min(window_height, int(available_height))
            
            # Calcular posição central
            center_x = max(0, int((screen_width - final_width) / 2))
            center_y = max(0, int((screen_height - final_height) / 2))
            
            # Para telas pequenas, posicionar um pouco mais alto
            if screen_height < 800:
                center_y = max(0, int(center_y * 0.8))  # 20% mais alto
            
            # Aplicar posição e tamanho centralizados
            root.geometry(f'{final_width}x{final_height}+{center_x}+{center_y}')
            
            # Verificar se houve ajuste de tamanho
            if final_width != window_width or final_height != window_height:
                print(f"⚠️ Tamanho ajustado para a tela: {final_width}x{final_height}")
            
            print(f'✅ Janela centralizada: {final_width}x{final_height} na posição ({center_x}, {center_y})')
            
            # Para telas muito pequenas, maximizar se necessário
            if screen_width < 1024 or screen_height < 768:
                print("📱 Tela pequena detectada - considerando maximização")
                # Não maximizar automaticamente, apenas notificar
                
        except Exception as e:
            print(f'⚠️ Erro ao centralizar janela: {e}')
            # Fallback - tentar centralização básica
            try:
                root.geometry(f'{window_width}x{window_height}')
                print("🔄 Aplicando centralização básica como fallback")
            except:
                pass
    
    # Centralizar após um pequeno delay para garantir que tudo esteja carregado
    root.after(100, centralizar_janela)

    # ===== FUNÇÃO PARA RECENTRALIZAR MANUALMENTE =====
    def recentralizar_janela_manual(event=None):
        """Permite recentralizar a janela manualmente"""
        centralizar_janela()
        return "break"  # Impede que o evento seja propagado
    
    # Vincular tecla de atalho Ctrl+Home para recentralizar
    root.bind('<Control-Home>', recentralizar_janela_manual)
    
    # Adicionar informação sobre o atalho no console
    print("💡 Dica: Use Ctrl+Home para recentralizar a janela a qualquer momento")

    # Frame superior
    top_frame = tk.Frame(root, bg=DARK_BG)
    top_frame.pack(fill='x', padx=10, pady=5)

    # Frame de rolagem
    scroll_canvas = tk.Canvas(root, bg=DARK_BG, highlightthickness=0)
    scroll_canvas.pack(side='left', fill='both', expand=True)

    scrollbar = ttk.Scrollbar(root, orient='vertical', command=scroll_canvas.yview)
    scrollbar.pack(side='right', fill='y')

    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    # Frame principal
    main_frame = tk.Frame(scroll_canvas, bg=DARK_BG, padx=40, pady=20)
    main_frame_id = scroll_canvas.create_window((0, 0), window=main_frame, anchor='nw')

    # Função para centralizar o conteúdo quando a janela é redimensionada
    def centralizar_conteudo(event=None):
        canvas_width = scroll_canvas.winfo_width()
        main_frame_width = main_frame.winfo_reqwidth()
        
        # Calcular nova posição x para centralizar
        if canvas_width > main_frame_width:
            new_x = (canvas_width - main_frame_width) / 2
        else:
            new_x = 0
        
        # Reposicionar o frame dentro do canvas
        scroll_canvas.coords(main_frame_id, new_x, 0)

    def on_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all'))
        centralizar_conteudo()  # Centralizar após configurar o tamanho

    main_frame.bind('<Configure>', on_configure)
    scroll_canvas.bind('<Configure>', centralizar_conteudo)  # Centralizar quando o canvas é redimensionado

    # ===== APLICAR SCROLL UNIVERSAL =====
    # Remover implementação antiga de scroll
    # scroll_canvas.bind("<MouseWheel>", _on_mousewheel)
    # main_frame.bind("<MouseWheel>", _on_mousewheel)
    
    # Aplicar novo sistema de scroll universal
    root.after(500, aplicar_scroll_universal)  # Aplicar após todos os widgets serem criados
    
    # Título com estilo Shopee
    title_frame = tk.Frame(main_frame, bg=DARK_BG)
    title_frame.pack(fill='x', pady=(0, 30))

    title = tk.Label(
        title_frame,
        text='Relatório de Expedição',
        font=('Segoe UI', 28, 'bold'),
        fg=SHOPEE_ORANGE,
        bg=DARK_BG
    )
    title.pack()

    # Carregar e redimensionar a logo
    logo_image = tk.PhotoImage(file='shopee_xpress_ajustado.png')
    logo_image = logo_image.subsample(4, 4)
    
    logo_label = tk.Label(
        title_frame,
        image=logo_image,
        bg=DARK_BG
    )
    logo_label.image = logo_image
    logo_label.pack(pady=(5, 0))

    # Frame superior com informações da janela e botão de configuração
    top_info_frame = tk.Frame(top_frame, bg=DARK_BG)
    top_info_frame.pack(fill='x', pady=5)
    
    # Label para mostrar a janela atual
    window_label = tk.Label(
        top_info_frame,
        text="Carregando...",
        font=('Segoe UI', 11),
        bg=DARK_BG,
        fg=DARK_TEXT
    )
    window_label.pack(side='left', padx=10)
    
    # Botão de configuração de email
    email_config_button = ttk.Button(
        top_info_frame,
        text="✉ Configurar Email",
        style='success.Outline.TButton',
        command=abrir_configuracao_email
    )
    email_config_button.pack(side='right', padx=(5, 10))
    
    # Botão de configuração de janelas
    config_button = ttk.Button(
        top_info_frame,
        text="⚙ Configurar Janelas",
        style='warning.Outline.TButton',
        command=abrir_configuracao
    )
    config_button.pack(side='right', padx=5)
    
    # Dropdown para seleção de janela
    config_manager = ConfigManager()
    config = config_manager.load_config()
    window_options = [config_manager.format_window_display(k, v) for k, v in config.items()]
    
    window_var = tk.StringVar()
    window_dropdown = ttk.Combobox(
        top_info_frame,
        textvariable=window_var,
        values=window_options,
        state='readonly',
        style='warning.TCombobox',
        width=30
    )
    window_dropdown.pack(side='right', padx=10)
    window_dropdown.set("Selecione a Janela de Carregamento")

    # Seção arquivos de expedição
    frame_expedicao = create_section_frame(main_frame, 'Arquivos de Expedição (Delivery Assignment):')
    expedicao_var = tk.StringVar()
    expedicao_listbox = tk.Listbox(
        frame_expedicao,
        height=5,
        font=('Segoe UI', 10),
        bg=DARK_HIGHLIGHT,
        fg=DARK_TEXT,
        selectbackground=SHOPEE_ORANGE,
        activestyle='none',
        relief='flat',
        highlightthickness=1,
        highlightbackground=SHOPEE_GRAY,
        selectmode=tk.EXTENDED
    )
    expedicao_listbox.pack(fill='x', pady=4)
    
    # Frame para os scrollbars
    scroll_frame = tk.Frame(frame_expedicao, bg=DARK_BG)
    scroll_frame.pack(fill='x', pady=(0, 4))
    
    # Scrollbar vertical
    scrollbar_y = ttk.Scrollbar(scroll_frame, orient='vertical', command=expedicao_listbox.yview)
    scrollbar_y.pack(side='right', fill='y')
    
    # Scrollbar horizontal
    scrollbar_x = ttk.Scrollbar(scroll_frame, orient='horizontal', command=expedicao_listbox.xview)
    scrollbar_x.pack(side='bottom', fill='x')
    
    # Configurar ambos os scrollbars
    expedicao_listbox.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
    
    # Frame para os botões de expedição
    btn_frame = tk.Frame(frame_expedicao, bg=DARK_BG)
    btn_frame.pack(fill='x', pady=2)
    
    # Botão para selecionar arquivos de expedição
    btn_expedicao = ttk.Button(
        btn_frame,
        text='Selecionar Arquivos',
        style='warning.TButton',
        command=selecionar_expedicao
    )
    btn_expedicao.pack(side='right', padx=2)
    
    # Botão para remover arquivos selecionados de expedição
    btn_remover = ttk.Button(
        btn_frame,
        text='Remover Selecionados',
        style='danger.Outline.TButton',
        command=remover_selecionados_expedicao
    )
    btn_remover.pack(side='right', padx=2)

    # Seção arquivo de conferência
    frame_conferencia = create_section_frame(main_frame, 'Arquivo de Conferência (Gestão Audit):')
    conferencia_var = tk.StringVar()
    conferencia_listbox = tk.Listbox(
        frame_conferencia,
        height=5,
        font=('Segoe UI', 10),
        bg=DARK_HIGHLIGHT,
        fg=DARK_TEXT,
        selectbackground=SHOPEE_ORANGE,
        activestyle='none',
        relief='flat',
        highlightthickness=1,
        highlightbackground=SHOPEE_GRAY,
        selectmode=tk.EXTENDED
    )
    conferencia_listbox.pack(fill='x', pady=4)
    
    # Frame para os scrollbars
    scroll_frame_conf = tk.Frame(frame_conferencia, bg=DARK_BG)
    scroll_frame_conf.pack(fill='x', pady=(0, 4))
    
    # Scrollbar vertical
    scrollbar_y_conf = ttk.Scrollbar(scroll_frame_conf, orient='vertical', command=conferencia_listbox.yview)
    scrollbar_y_conf.pack(side='right', fill='y')
    
    # Scrollbar horizontal
    scrollbar_x_conf = ttk.Scrollbar(scroll_frame_conf, orient='horizontal', command=conferencia_listbox.xview)
    scrollbar_x_conf.pack(side='bottom', fill='x')
    
    # Configurar ambos os scrollbars
    conferencia_listbox.configure(xscrollcommand=scrollbar_x_conf.set, yscrollcommand=scrollbar_y_conf.set)
    
    # Frame para os botões de conferência
    btn_frame_conf = tk.Frame(frame_conferencia, bg=DARK_BG)
    btn_frame_conf.pack(fill='x', pady=2)
    
    # Botão para selecionar arquivos de conferência
    btn_conferencia = ttk.Button(
        btn_frame_conf,
        text='Selecionar Arquivos',
        style='warning.TButton',
        command=selecionar_conferencia
    )
    btn_conferencia.pack(side='right', padx=2)
    
    # Botão para remover arquivos selecionados de conferência
    btn_remover_conf = ttk.Button(
        btn_frame_conf,
        text='Remover Selecionados',
        style='danger.Outline.TButton',
        command=remover_selecionados_conferencia
    )
    btn_remover_conf.pack(side='right', padx=2)

    # Seção diretório de saída
    frame_output = create_section_frame(main_frame, 'Diretório para salvar os relatórios:')
    output_dir_var = tk.StringVar()
    output_dir_label = tk.Label(
        frame_output,
        text='Nenhum diretório selecionado',
        font=('Segoe UI', 10),
        bg=DARK_HIGHLIGHT,
        fg=DARK_TEXT,
        anchor='w',
        relief='flat',
        highlightthickness=1,
        highlightbackground=SHOPEE_GRAY,
        padx=10,
        pady=8
    )
    output_dir_label.pack(fill='x', pady=4)
    btn_output = ttk.Button(
        frame_output,
        text='Selecionar Diretório',
        style='warning.TButton',
        command=selecionar_diretorio
    )
    btn_output.pack(anchor='e', pady=2)

    # Campo de texto para informações adicionais
    frame_info = create_section_frame(main_frame, 'Informações adicionais sobre o fechamento da expedição:')
    info_text = tk.Text(
        frame_info,
        height=4,
        font=('Segoe UI', 10),
        bg=DARK_HIGHLIGHT,
        fg=DARK_TEXT,
        relief='flat',
        highlightthickness=1,
        highlightbackground=SHOPEE_GRAY,
        padx=10,
        pady=8
    )
    info_text.pack(fill='x', pady=4)

    # Adicionar placeholder
    placeholder_text = "Mencione informações relevantes que podem ser requisitadas no futuro."
    info_text.insert("1.0", placeholder_text)
    info_text.config(fg=SHOPEE_GRAY)

    # Funções para gerenciar o placeholder
    def on_info_focus_in(event):
        if info_text.get("1.0", "end-1c") == placeholder_text:
            info_text.delete("1.0", "end")
            info_text.config(fg=DARK_TEXT)

    def on_info_focus_out(event):
        if info_text.get("1.0", "end-1c") == "":
            info_text.insert("1.0", placeholder_text)
            info_text.config(fg=SHOPEE_GRAY)

    info_text.bind("<FocusIn>", on_info_focus_in)
    info_text.bind("<FocusOut>", on_info_focus_out)

    # Botão principal
    btn_gerar = ttk.Button(
        main_frame,
        text='Gerar Relatórios',
        style='warning.TButton',
        width=25,
        command=on_gerar
    )
    btn_gerar.pack(pady=30)

    # Status
    status_label = tk.Label(
        main_frame,
        text='',
        font=('Segoe UI', 11),
        bg=DARK_BG,
        fg=DARK_TEXT
    )
    status_label.pack(pady=10)

    # Estilizar os botões
    style = ttk.Style()
    style.configure('TButton', 
                   font=('Segoe UI', 11, 'bold'),
                   padding=10)
    
    style.configure('warning.TButton', 
                   background=SHOPEE_ORANGE,
                   foreground='white',
                   borderwidth=0,
                   padding=10)
                   
    style.configure('danger.Outline.TButton',
                   background=DARK_BG,
                   foreground='#dc3545',
                   borderwidth=1,
                   bordercolor='#dc3545',
                   padding=10)
    
    style.configure('success.Outline.TButton',
                   background=DARK_BG,
                   foreground='#28a745',
                   borderwidth=1,
                   bordercolor='#28a745',
                   padding=10)
    
    style.configure('warning.Outline.TButton',
                   background=DARK_BG,
                   foreground=SHOPEE_ORANGE,
                   borderwidth=1,
                   bordercolor=SHOPEE_ORANGE,
                   padding=10)

    # Configurar hover para os botões
    style.map('warning.TButton',
             background=[('active', '#ff6e40')],
             foreground=[('active', 'white')])
             
    style.map('danger.Outline.TButton',
             background=[('active', '#dc3545')],
             foreground=[('active', 'white')])
    
    style.map('success.Outline.TButton',
             background=[('active', '#28a745')],
             foreground=[('active', 'white')])
    
    style.map('warning.Outline.TButton',
             background=[('active', SHOPEE_ORANGE)],
             foreground=[('active', 'white')])

    # Atualizar a interface com as cores do tema escuro
    atualizar_interface(
        root=root,
        scroll_canvas=scroll_canvas,
        main_frame=main_frame,
        top_frame=top_frame,
        title_frame=title_frame,
        title=title,
        logo_label=logo_label,
        conferencia_label=conferencia_label,
        output_dir_label=output_dir_label,
        info_text=info_text,
        placeholder_text=placeholder_text,
        status_label=status_label
    )

    # Iniciar atualização automática da janela atual
    atualizar_janela_atual()
    
    # ===== APLICAR SCROLL UNIVERSAL FINAL =====
    # Aplicar scroll universal uma segunda vez após tudo estar carregado
    root.after(1000, aplicar_scroll_universal)

    # ===== GERENCIAMENTO DE FOCO =====
    configurar_gerenciamento_foco()

# Inicializar e executar a interface
inicializar_interface()
root.mainloop() 