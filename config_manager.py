import json
import os
from datetime import datetime, time, timedelta

class ConfigManager:
    def __init__(self):
        self.config_dir = "config"
        self.config_file = os.path.join(self.config_dir, "windows_config.json")
        self.default_config = {
            "MANHA": {
                "nome": "Manhã (Madrugada)",
                "inicio": "04:00",
                "fim": "09:00"
            },
            "TARDE": {
                "nome": "Tarde",
                "inicio": "13:00",
                "fim": "18:00"
            },
            "NOITE": {
                "nome": "Noite",
                "inicio": "19:00",
                "fim": "23:00"
            }
        }
    
    def ensure_config_exists(self):
        """Garante que o diretório e arquivo de configuração existam"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        if not os.path.exists(self.config_file):
            self.save_config(self.default_config)
    
    def load_config(self):
        """Carrega as configurações do arquivo"""
        try:
            if not os.path.exists(self.config_file):
                self.ensure_config_exists()
                return self.default_config
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configurações: {str(e)}")
            return self.default_config
    
    def save_config(self, config):
        """Salva as configurações no arquivo"""
        try:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {str(e)}")
            return False
    
    def get_current_window(self):
        """Retorna a janela atual baseada no horário do sistema"""
        try:
            config = self.load_config()
            current_time = datetime.now().time()
            
            for window_key, window_config in config.items():
                start = datetime.strptime(window_config["inicio"], "%H:%M").time()
                end = datetime.strptime(window_config["fim"], "%H:%M").time()
                
                if start <= current_time <= end:
                    return window_key, window_config
            
            return None, None
        except Exception as e:
            print(f"Erro ao determinar janela atual: {str(e)}")
            return None, None
    
    def format_window_display(self, window_key, window_config):
        """Formata o texto de exibição da janela"""
        return f"{window_config['nome']} - {window_config['inicio']} às {window_config['fim']}"
    
    def get_window_by_delivery_date(self, delivery_date_str, current_window_key):
        """
        Determina a janela correta de uma rota baseado no Delivery Date
        Args:
            delivery_date_str: Data de entrega no formato YYYY-MM-DD
            current_window_key: Chave da janela atual (MANHA, TARDE, NOITE)
        Returns:
            tuple: (window_key, is_other_window)
            window_key: Chave da janela identificada
            is_other_window: True se a rota pertence a outra janela
        """
        try:
            # Converter delivery_date para datetime
            delivery_date = datetime.strptime(delivery_date_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            
            # Se delivery_date é anterior a hoje, é uma rota da janela da manhã (D-1)
            if delivery_date < today:
                return "MANHA", (current_window_key != "MANHA")
            
            # Se delivery_date é hoje
            if delivery_date == today:
                current_time = datetime.now().time()
                config = self.load_config()
                
                # Determinar janela baseado no horário atual
                for window_key, window_config in config.items():
                    start = datetime.strptime(window_config["inicio"], "%H:%M").time()
                    end = datetime.strptime(window_config["fim"], "%H:%M").time()
                    
                    if start <= current_time <= end:
                        return window_key, False
                
                # Se não estiver em nenhuma janela, usar a próxima janela disponível
                for window_key, window_config in config.items():
                    start = datetime.strptime(window_config["inicio"], "%H:%M").time()
                    if current_time < start:
                        return window_key, (current_window_key != window_key)
            
            # Se delivery_date é futuro, é uma rota irregular
            return current_window_key, True
            
        except Exception as e:
            print(f"Erro ao determinar janela por delivery date: {str(e)}")
            return current_window_key, False
    
    def get_window_name(self, window_key):
        """Retorna o nome amigável da janela"""
        try:
            config = self.load_config()
            return config[window_key]["nome"]
        except:
            return window_key
    
    def is_previous_window(self, window_key_a, window_key_b):
        """Verifica se uma janela é anterior a outra"""
        try:
            config = self.load_config()
            windows_order = ["MANHA", "TARDE", "NOITE"]
            idx_a = windows_order.index(window_key_a)
            idx_b = windows_order.index(window_key_b)
            return idx_a < idx_b
        except:
            return False 