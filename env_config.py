"""
Utilitário para gerenciamento de variáveis de ambiente
Carrega configurações do arquivo .env de forma segura
"""

import os
from typing import Optional, List

class EnvConfig:
    """Gerenciador de configurações de ambiente"""
    
    def __init__(self, env_file: str = ".env"):
        """
        Inicializa o gerenciador de configurações
        
        Args:
            env_file: Caminho para o arquivo .env
        """
        self.env_file = env_file
        self.load_env_file()
    
    def load_env_file(self):
        """Carrega variáveis do arquivo .env se existir"""
        if os.path.exists(self.env_file):
            try:
                with open(self.env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # Ignorar comentários e linhas vazias
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Remover aspas se existirem
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            elif value.startswith("'") and value.endswith("'"):
                                value = value[1:-1]
                            
                            # Processar caracteres de escape
                            value = value.replace('\\n', '\n')
                            
                            os.environ[key] = value
            except Exception as e:
                print(f"⚠️ Erro ao carregar arquivo .env: {e}")
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Obtém valor de variável de ambiente
        
        Args:
            key: Nome da variável
            default: Valor padrão se não encontrada
            
        Returns:
            Valor da variável ou padrão
        """
        return os.environ.get(key, default)
    
    def get_list(self, key: str, separator: str = ',', default: Optional[List[str]] = None) -> List[str]:
        """
        Obtém lista de valores separados por um caractere
        
        Args:
            key: Nome da variável
            separator: Caractere separador
            default: Lista padrão se não encontrada
            
        Returns:
            Lista de valores
        """
        value = self.get(key)
        if value:
            return [item.strip() for item in value.split(separator) if item.strip()]
        return default or []
    
    def get_int(self, key: str, default: int = 0) -> int:
        """
        Obtém valor inteiro de variável de ambiente
        
        Args:
            key: Nome da variável
            default: Valor padrão se não encontrada ou inválida
            
        Returns:
            Valor inteiro
        """
        try:
            value = self.get(key)
            return int(value) if value else default
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Obtém valor booleano de variável de ambiente
        
        Args:
            key: Nome da variável
            default: Valor padrão se não encontrada
            
        Returns:
            Valor booleano
        """
        value = self.get(key, '').lower()
        if value in ('true', '1', 'yes', 'on'):
            return True
        elif value in ('false', '0', 'no', 'off'):
            return False
        return default
    
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção"""
        return self.get('ENVIRONMENT', 'development').lower() == 'production'
    
    def is_debug(self) -> bool:
        """Verifica se modo debug está ativado"""
        return self.get_bool('DEBUG', False)
    
    def create_env_from_config(self, config_data: dict) -> bool:
        """
        Cria arquivo .env a partir de configurações existentes
        
        Args:
            config_data: Dicionário com configurações
            
        Returns:
            True se criado com sucesso
        """
        try:
            # Verificar se .env já existe
            if os.path.exists(self.env_file):
                print(f"⚠️ Arquivo {self.env_file} já existe. Backup será criado.")
                # Criar backup
                backup_file = f"{self.env_file}.backup"
                if os.path.exists(backup_file):
                    os.remove(backup_file)
                os.rename(self.env_file, backup_file)
            
            # Criar novo arquivo .env
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.write("# ========================================\n")
                f.write("# CONFIGURAÇÕES DE EMAIL - SHOPEE RELATÓRIOS\n")
                f.write("# ========================================\n\n")
                
                # Email configurations
                f.write(f"REMETENTE_EMAIL={config_data.get('remetente_email', '')}\n")
                f.write(f"REMETENTE_SENHA={config_data.get('remetente_senha', '')}\n")
                
                destinatarios = ','.join(config_data.get('destinatarios', []))
                f.write(f"DESTINATARIOS={destinatarios}\n\n")
                
                f.write(f"SMTP_SERVER={config_data.get('smtp_server', 'smtp.gmail.com')}\n")
                f.write(f"SMTP_PORT={config_data.get('smtp_port', 587)}\n\n")
                
                f.write(f"ASSUNTO_PADRAO={config_data.get('assunto_padrao', '')}\n")
                
                # Escapar quebras de linha no corpo da mensagem
                corpo = config_data.get('corpo_mensagem', '').replace('\n', '\\n')
                f.write(f"CORPO_MENSAGEM={corpo}\n\n")
                
                f.write("# ========================================\n")
                f.write("# CONFIGURAÇÕES GERAIS\n")
                f.write("# ========================================\n\n")
                f.write("UNIDADE_NOME=Mauá LSP64\n")
                f.write("ENVIRONMENT=production\n")
                f.write("DEBUG=false\n")
            
            print(f"✅ Arquivo {self.env_file} criado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar arquivo .env: {e}")
            return False

# Instância global do gerenciador
env_config = EnvConfig()

def get_env_config() -> EnvConfig:
    """Retorna instância global do gerenciador de configurações"""
    return env_config 