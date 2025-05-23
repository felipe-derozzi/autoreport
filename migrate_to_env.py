#!/usr/bin/env python3
"""
Script de migração de configurações para arquivo .env
Converte configurações do arquivo JSON para variáveis de ambiente
"""

import os
import json
import shutil
from datetime import datetime
from email_manager import EmailManager
from env_config import get_env_config

def main():
    """Função principal de migração"""
    print("🔄 Script de Migração para Variáveis de Ambiente")
    print("=" * 50)
    
    email_manager = EmailManager()
    env_config = get_env_config()
    
    # Verificar se .env já existe
    if os.path.exists('.env'):
        print("⚠️  Arquivo .env já existe!")
        resposta = input("Deseja sobrescrever? (s/N): ").lower().strip()
        if resposta not in ['s', 'sim', 'y', 'yes']:
            print("❌ Migração cancelada.")
            return
        
        # Fazer backup do .env atual
        backup_name = f".env.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy('.env', backup_name)
        print(f"📋 Backup criado: {backup_name}")
    
    # Carregar configurações existentes do JSON
    config_file = os.path.join("config", "email_config.json")
    
    if not os.path.exists(config_file):
        print("❌ Arquivo config/email_config.json não encontrado!")
        print("💡 Criando arquivo .env com configurações padrão...")
        create_default_env()
        return
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("📋 Configurações encontradas no JSON:")
        print(f"   - Email: {config.get('remetente_email', 'Não configurado')}")
        print(f"   - Destinatários: {len(config.get('destinatarios', []))} email(s)")
        print(f"   - Servidor SMTP: {config.get('smtp_server', 'Não configurado')}")
        
        # Verificar se há credenciais
        if not config.get('remetente_email') or not config.get('remetente_senha'):
            print("⚠️  Credenciais não encontradas no JSON!")
            print("💡 Será criado .env com template para você preencher.")
        
        # Migrar para .env
        success = env_config.create_env_from_config(config)
        
        if success:
            print("\n✅ Migração concluída com sucesso!")
            print("📁 Arquivo .env criado com suas configurações.")
            
            # Perguntar se quer limpar o JSON
            resposta = input("\n🧹 Deseja remover credenciais do arquivo JSON? (S/n): ").lower().strip()
            if resposta in ['', 's', 'sim', 'y', 'yes']:
                clean_json_config(config_file, config)
                print("✅ Credenciais removidas do arquivo JSON.")
            
            print("\n📋 Próximos passos:")
            print("1. ✅ Arquivo .gitignore já configurado")
            print("2. 📝 Edite o arquivo .env com suas credenciais reais")
            print("3. 🔒 NUNCA commite o arquivo .env para o Git")
            print("4. 🚀 Execute o programa normalmente")
            
        else:
            print("❌ Erro na migração. Verifique as mensagens acima.")
            
    except Exception as e:
        print(f"❌ Erro ao ler configurações JSON: {e}")

def create_default_env():
    """Cria arquivo .env com configurações padrão"""
    env_config = get_env_config()
    default_config = {
        'remetente_email': '',
        'remetente_senha': '',
        'destinatarios': [],
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'assunto_padrao': 'Relatório de Expedição - Shopee',
        'corpo_mensagem': 'Olá,\n\nSegue em anexo o relatório de expedição gerado automaticamente.\n\nDados do processamento:\n\n- Data/Hora: {data_hora}\n- Janela: {janela}\n\nAtenciosamente,\nSistema de Relatórios Shopee'
    }
    
    success = env_config.create_env_from_config(default_config)
    if success:
        print("✅ Arquivo .env criado com template padrão.")
        print("📝 Edite o arquivo .env com suas configurações.")

def clean_json_config(config_file, original_config):
    """Remove credenciais do arquivo JSON após migração"""
    try:
        # Criar backup do JSON original
        backup_name = f"{config_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy(config_file, backup_name)
        
        # Limpar credenciais
        clean_config = original_config.copy()
        clean_config['remetente_email'] = ""
        clean_config['remetente_senha'] = ""
        clean_config['destinatarios'] = []
        
        # Salvar JSON limpo
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(clean_config, f, indent=4, ensure_ascii=False)
        
        print(f"📋 Backup do JSON original: {backup_name}")
        
    except Exception as e:
        print(f"⚠️ Erro ao limpar arquivo JSON: {e}")

def check_git_status():
    """Verifica status do Git e arquivos que podem vazar credenciais"""
    print("\n🔍 Verificando arquivos sensíveis...")
    
    sensitive_files = [
        '.env',
        'config/email_config.json'
    ]
    
    for file in sensitive_files:
        if os.path.exists(file):
            # Verificar se arquivo tem credenciais
            if file.endswith('.json'):
                try:
                    with open(file, 'r') as f:
                        content = json.load(f)
                    if content.get('remetente_senha') or content.get('remetente_email'):
                        print(f"⚠️  {file} contém credenciais!")
                except:
                    pass
            elif file == '.env':
                print(f"🔒 {file} detectado (deve estar no .gitignore)")

if __name__ == "__main__":
    main()
    check_git_status()
    
    print("\n" + "=" * 50)
    print("🎯 Migração finalizada!")
    print("💡 Use: python gui_relatorio.py para executar o programa") 