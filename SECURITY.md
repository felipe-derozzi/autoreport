# 🔒 Segurança e Proteção de Dados

## 📋 Visão Geral de Segurança

Este projeto implementa **múltiplas camadas de proteção** para garantir que suas credenciais e dados sensíveis nunca sejam expostos inadvertidamente.

## 🛡️ Sistema de Proteção Implementado

### **1. Variáveis de Ambiente (.env)**
```bash
# ✅ Configuração segura
REMETENTE_EMAIL=seu.email@shopee.com
REMETENTE_SENHA=sua_senha_de_app_gmail
DESTINATARIOS=supervisor@shopee.com,equipe@shopee.com
```

**Benefícios:**
- 🔒 Credenciais **nunca** aparecem no código
- 🚫 Arquivo `.env` **bloqueado** pelo `.gitignore`
- ♻️ Carregamento automático na execução
- 🔄 Fallback seguro para configurações JSON

### **2. Arquivo .gitignore Robusto**
```gitignore
# 🚫 Arquivos NUNCA enviados para Git
.env                        # Suas credenciais
config/email_config.json    # Configurações com dados sensíveis
build/                      # Arquivos de compilação
dist/                       # Executável gerado
*.log                       # Logs com possíveis dados sensíveis
```

### **3. Migração Automática Segura**
O sistema detecta automaticamente configurações antigas e oferece migração:

```bash
# Execute para migrar configurações existentes
python migrate_to_env.py

# ✅ O que acontece:
# 1. Backup do arquivo original
# 2. Criação do .env com suas configurações
# 3. Limpeza de credenciais do JSON
# 4. Configuração automática de segurança
```

## 🚨 Alertas de Segurança Críticos

### **❌ NUNCA FAÇA ISSO:**
```bash
# ⛔ PERIGO! Isso expõe suas credenciais
git add .env
git add config/email_config.json
git commit -m "configurações de email"
git push
```

### **✅ SEMPRE FAÇA ISSO:**
```bash
# 🔍 Verificar antes de cada commit
git status --ignored

# 🛡️ Verificar se .gitignore está funcionando
git check-ignore .env  # Deve retornar ".env"

# 📝 Commitar apenas arquivos seguros
git add README.md gui_relatorio.py
git commit -m "feature: nova funcionalidade"
```

## 🔧 Configuração Inicial Segura

### **Passo 1: Configurar .env**
1. Copie o template:
   ```bash
   cp .env.example .env
   ```

2. Edite com suas credenciais reais:
   ```bash
   # Windows
   notepad .env
   
   # Linux/Mac
   nano .env
   ```

3. **IMPORTANTE**: Use Senha de App do Gmail (não sua senha normal)

### **Passo 2: Verificar Proteção**
```bash
# Verificar se .env está protegido
git status --ignored | grep ".env"

# Resultado esperado:
# !! .env
```

### **Passo 3: Testar Funcionamento**
```bash
# Execute o programa para testar
python gui_relatorio.py

# Vá em "Configurar Email" > "Testar Conexão"
# Deve usar automaticamente as credenciais do .env
```

## 🔄 Cenários de Uso

### **📦 Novo Usuário (Clone do GitHub)**
```bash
# 1. Clone o repositório
git clone [repository-url]
cd relatorio_automatico

# 2. Configure ambiente
cp .env.example .env
nano .env  # Edite com suas credenciais

# 3. Execute
python gui_relatorio.py
```

### **🔄 Usuário Existente (Migração)**
```bash
# 1. Baixe as atualizações
git pull

# 2. Execute migração automática
python migrate_to_env.py

# 3. Suas credenciais foram migradas com segurança!
```

### **👥 Trabalho em Equipe**
```bash
# ✅ Cada desenvolvedor tem seu próprio .env
# ✅ Credenciais nunca são compartilhadas via Git
# ✅ Configurações de projeto vão no .env.example (público)
```

## 🚧 Níveis de Segurança

### **🟢 Nível 1: Básico**
- ✅ Arquivo `.env` criado
- ✅ `.gitignore` configurado
- ✅ Credenciais fora do código

### **🟡 Nível 2: Intermediário**
- ✅ Migração de configurações antigas
- ✅ Backup automático
- ✅ Verificação de arquivos sensíveis

### **🔴 Nível 3: Avançado**
- ✅ Carregamento automático de variáveis
- ✅ Fallback seguro
- ✅ Detecção de credenciais em JSON
- ✅ Limpeza automática de arquivos sensíveis

## 🔍 Auditoria de Segurança

### **Verificações Automáticas**
O sistema inclui verificações automáticas:

```python
# Verificar fonte das configurações
email_manager.get_config_source()
# Retorna: "Variáveis de Ambiente (.env)" ✅

# Verificar se está usando .env
email_manager.is_using_env()
# Retorna: True ✅
```

### **Checklist de Segurança**
```bash
# ✅ Arquivo .env existe e tem credenciais?
[ ] .env criado com REMETENTE_EMAIL e REMETENTE_SENHA

# ✅ .gitignore está protegendo arquivos sensíveis?
[ ] git check-ignore .env retorna ".env"
[ ] git status --ignored mostra .env na lista

# ✅ Não há credenciais hardcodadas no código?
[ ] Buscar por "@" em arquivos .py (emails hardcodados)
[ ] Buscar por "password" em arquivos de configuração

# ✅ Backup das configurações importantes?
[ ] Configurações de janelas/turnos preservadas
[ ] Templates de email personalizados salvos
```

## 🆘 Recuperação de Emergência

### **Se você commitou credenciais por acidente:**

```bash
# 1. PARE IMEDIATAMENTE
git reset --soft HEAD~1  # Desfaz último commit (mantém alterações)

# 2. Remover credenciais do arquivo
echo "" > config/email_config.json

# 3. Adicionar ao .gitignore se não estiver
echo "config/email_config.json" >> .gitignore

# 4. Commit seguro
git add .gitignore
git commit -m "security: protect sensitive config files"

# 5. Se já fez push, mude IMEDIATAMENTE as senhas
```

### **Se perdeu o arquivo .env:**

```bash
# 1. Recriar do template
cp .env.example .env

# 2. Ou usar o backup automático
cp .env.backup.YYYYMMDD_HHMMSS .env

# 3. Ou executar migração novamente
python migrate_to_env.py
```

## 📞 Suporte de Segurança

Para questões de segurança:

1. **Verifique** o `.gitignore` está funcionando
2. **Execute** `python migrate_to_env.py` para diagnóstico
3. **Confirme** que `git status --ignored` mostra `.env`
4. **Teste** a conexão via interface do programa

---

## 🎯 Resumo de Segurança

| Aspecto | Status | Descrição |
|---------|---------|-----------|
| **Credenciais** | 🔒 Protegidas | Armazenadas em `.env` |
| **Git** | 🚫 Bloqueado | `.gitignore` ativo |
| **Backup** | ♻️ Automático | Criado na migração |
| **Validação** | ✅ Ativa | Verificação automática |
| **Migração** | 🔄 Inteligente | Detecta e converte |

**🎖️ Sua segurança é nossa prioridade!** 