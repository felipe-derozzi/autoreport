import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
import json
from datetime import datetime
from env_config import get_env_config

class EmailManager:
    def __init__(self):
        self.config_dir = "config"
        self.email_config_file = os.path.join(self.config_dir, "email_config.json")
        self.email_template_file = os.path.join(self.config_dir, "email_config_template.json")
        self.env = get_env_config()
        
        # Configurações padrão agora vêm do template
        self.default_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "remetente_email": "",
            "remetente_senha": "",
            "destinatarios": [],
            "assunto_padrao": "Relatório de Expedição - Shopee",
            "corpo_mensagem": """Olá,

Segue em anexo o relatório de expedição gerado automaticamente.

Dados do processamento:
- Data/Hora: {data_hora}
- Janela: {janela}
- Arquivos gerados: CSV, XLSX, PDF

Atenciosamente,
Sistema de Relatórios Shopee"""
        }
    
    def ensure_config_exists(self):
        """Garante que o diretório e arquivo de configuração de email existam"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        # Se não existe configuração e nem .env, criar template
        if not os.path.exists(self.email_config_file) and not os.path.exists('.env'):
            self.save_email_config(self.default_config)
    
    def load_email_config(self):
        """Carrega as configurações de email (prioritiza .env sobre JSON)"""
        try:
            # Primeiro, tenta carregar do .env (mais seguro)
            config = self._load_from_env()
            
            # Se .env não tem configurações completas, tenta JSON como fallback
            if not self._is_config_complete(config):
                json_config = self._load_from_json()
                # Merge: .env sobrescreve JSON onde existir
                for key, value in config.items():
                    if value:  # Só sobrescreve se .env tem valor
                        json_config[key] = value
                config = json_config
            
            return config
            
        except Exception as e:
            print(f"Erro ao carregar configurações de email: {str(e)}")
            return self.default_config
    
    def _load_from_env(self):
        """Carrega configurações das variáveis de ambiente"""
        return {
            "smtp_server": self.env.get("SMTP_SERVER", "smtp.gmail.com"),
            "smtp_port": self.env.get_int("SMTP_PORT", 587),
            "remetente_email": self.env.get("REMETENTE_EMAIL", ""),
            "remetente_senha": self.env.get("REMETENTE_SENHA", ""),
            "destinatarios": self.env.get_list("DESTINATARIOS"),
            "assunto_padrao": self.env.get("ASSUNTO_PADRAO", "Relatório de Expedição - Shopee"),
            "corpo_mensagem": self.env.get("CORPO_MENSAGEM", self.default_config["corpo_mensagem"])
        }
    
    def _load_from_json(self):
        """Carrega configurações do arquivo JSON (fallback)"""
        if not os.path.exists(self.email_config_file):
            return self.default_config.copy()
        
        with open(self.email_config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # Merge com configurações padrão para garantir que todas as chaves existam
            merged_config = self.default_config.copy()
            merged_config.update(config)
            return merged_config
    
    def _is_config_complete(self, config):
        """Verifica se a configuração está completa"""
        required_fields = ["remetente_email", "remetente_senha"]
        return all(config.get(field) for field in required_fields)
    
    def save_email_config(self, config):
        """Salva as configurações de email no arquivo JSON (para compatibilidade)"""
        try:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)
            
            # Se temos credenciais, oferecer para criar .env
            if config.get("remetente_email") and config.get("remetente_senha"):
                self._offer_env_migration(config)
            
            with open(self.email_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações de email: {e}")
            return False
    
    def _offer_env_migration(self, config):
        """Oferece migração para arquivo .env se detectar credenciais no JSON"""
        if os.path.exists('.env'):
            return  # .env já existe
        
        try:
            print("🔒 Detectadas credenciais no arquivo JSON.")
            print("💡 Recomendo migrar para arquivo .env para maior segurança.")
            
            # Criar .env automaticamente se não existir
            success = self.env.create_env_from_config(config)
            if success:
                print("✅ Arquivo .env criado! Suas credenciais agora estão mais seguras.")
                print("⚠️  IMPORTANTE: Adicione o arquivo .env ao .gitignore!")
                
                # Limpar credenciais do JSON após migração
                config_clean = config.copy()
                config_clean["remetente_email"] = ""
                config_clean["remetente_senha"] = ""
                config_clean["destinatarios"] = []
                
                with open(self.email_config_file, 'w', encoding='utf-8') as f:
                    json.dump(config_clean, f, indent=4, ensure_ascii=False)
                print("🧹 Credenciais removidas do arquivo JSON por segurança.")
                
        except Exception as e:
            print(f"⚠️ Erro na migração para .env: {e}")
    
    def validar_email(self, email):
        """Valida formato de email básico"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def testar_conexao(self, email, senha, smtp_server="smtp.gmail.com", smtp_port=587):
        """Testa a conexão SMTP com as credenciais fornecidas"""
        try:
            # Criar conexão SSL
            context = ssl.create_default_context()
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)
                server.login(email, senha)
                return True, "Conexão testada com sucesso!"
        except smtplib.SMTPAuthenticationError:
            return False, "Erro de autenticação. Verifique email e senha."
        except smtplib.SMTPConnectError:
            return False, "Erro de conexão com o servidor SMTP."
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"
    
    def enviar_email_relatorio(self, pdf_path, csv_path, xlsx_path, janela_info="", info_adicional=""):
        """
        Envia o email com os relatórios em anexo
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            csv_path: Caminho para o arquivo CSV
            xlsx_path: Caminho para o arquivo XLSX
            janela_info: Informação sobre a janela (turno)
            info_adicional: Informações adicionais do processamento
        
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        try:
            config = self.load_email_config()
            
            # Validar configurações básicas
            if not config["remetente_email"] or not config["remetente_senha"]:
                return False, "Configurações de email não definidas. Configure o remetente primeiro."
            
            if not config["destinatarios"]:
                return False, "Nenhum destinatário configurado."
            
            # Verificar se os arquivos existem
            anexos = []
            if pdf_path and os.path.exists(pdf_path):
                anexos.append(("relatorio_expedicao.pdf", pdf_path))
            if csv_path and os.path.exists(csv_path):
                anexos.append(("resumo_expedicao.csv", csv_path))
            if xlsx_path and os.path.exists(xlsx_path):
                anexos.append(("relatorio_expedicao.xlsx", xlsx_path))
            
            if not anexos:
                return False, "Nenhum arquivo de relatório foi encontrado para anexar."
            
            print(f"📎 Preparando email com {len(anexos)} anexo(s)")
            
            # Preparar informações para o corpo da mensagem
            data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M")
            
            # Formatear corpo da mensagem
            corpo_formatado = config["corpo_mensagem"].format(
                data_hora=data_hora,
                janela=janela_info if janela_info else "Não especificada"
            )
            
            # Adicionar informações extras se fornecidas
            if info_adicional and info_adicional.strip():
                corpo_formatado += f"\n\nInformações adicionais:\n{info_adicional.strip()}"
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = config["remetente_email"]
            msg['To'] = ", ".join(config["destinatarios"])
            msg['Subject'] = config["assunto_padrao"]
            
            # Adicionar corpo da mensagem
            msg.attach(MIMEText(corpo_formatado, 'plain', 'utf-8'))
            
            # Adicionar anexos
            for nome_arquivo, caminho_arquivo in anexos:
                try:
                    with open(caminho_arquivo, "rb") as anexo:
                        part = MIMEApplication(anexo.read())
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename="{nome_arquivo}"'
                        )
                        msg.attach(part)
                except Exception as e:
                    print(f"❌ Erro ao anexar arquivo {nome_arquivo}: {str(e)}")
            
            # Configurar SSL e enviar
            context = ssl.create_default_context()
            
            print(f"📧 Conectando ao servidor Gmail...")
            
            with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
                server.starttls(context=context)
                server.login(config["remetente_email"], config["remetente_senha"])
                
                # Enviar para todos os destinatários
                server.send_message(msg)
            
            destinatarios_str = ", ".join(config["destinatarios"])
            return True, f"Email enviado com sucesso para: {destinatarios_str}"
            
        except smtplib.SMTPAuthenticationError as e:
            return False, f"Erro de autenticação Gmail. Verifique a senha de app: {str(e)}"
        except smtplib.SMTPRecipientsRefused as e:
            return False, f"Destinatários rejeitados pelo servidor: {str(e)}"
        except smtplib.SMTPServerDisconnected as e:
            return False, f"Conexão com servidor perdida: {str(e)}"
        except Exception as e:
            return False, f"Erro inesperado ao enviar email: {str(e)}"
    
    def adicionar_destinatario(self, email):
        """Adiciona um destinatário à lista"""
        if not self.validar_email(email):
            return False, "Formato de email inválido."
        
        config = self.load_email_config()
        if email not in config["destinatarios"]:
            config["destinatarios"].append(email)
            if self.save_email_config(config):
                return True, "Destinatário adicionado com sucesso."
            else:
                return False, "Erro ao salvar configuração."
        else:
            return False, "Email já está na lista de destinatários."
    
    def remover_destinatario(self, email):
        """Remove um destinatário da lista"""
        config = self.load_email_config()
        if email in config["destinatarios"]:
            config["destinatarios"].remove(email)
            if self.save_email_config(config):
                return True, "Destinatário removido com sucesso."
            else:
                return False, "Erro ao salvar configuração."
        else:
            return False, "Email não encontrado na lista de destinatários."
    
    def atualizar_configuracoes_smtp(self, remetente_email, remetente_senha, assunto="", corpo_mensagem=""):
        """Atualiza as configurações SMTP e mensagem"""
        if not self.validar_email(remetente_email):
            return False, "Formato de email do remetente inválido."
        
        config = self.load_email_config()
        config["remetente_email"] = remetente_email
        config["remetente_senha"] = remetente_senha
        
        if assunto:
            config["assunto_padrao"] = assunto
        if corpo_mensagem:
            config["corpo_mensagem"] = corpo_mensagem
        
        if self.save_email_config(config):
            return True, "Configurações atualizadas com sucesso."
        else:
            return False, "Erro ao salvar configurações."
    
    def get_config_source(self):
        """Retorna a fonte das configurações atuais"""
        env_config = self._load_from_env()
        if self._is_config_complete(env_config):
            return "Variáveis de Ambiente (.env)"
        elif os.path.exists(self.email_config_file):
            return "Arquivo JSON (config/email_config.json)"
        else:
            return "Configurações Padrão"
    
    def is_using_env(self):
        """Verifica se está usando variáveis de ambiente"""
        env_config = self._load_from_env()
        return self._is_config_complete(env_config) 