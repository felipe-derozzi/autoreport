# Sistema de Email Automático - Relatório de Expedição

## 📧 Visão Geral

O sistema de email automático foi implementado para enviar automaticamente os relatórios de expedição (PDF, CSV, XLSX) para a supervisão e equipe após cada processamento realizado na ferramenta.

## 🚀 Principais Funcionalidades

### 1. **Configuração Completa de Email**
- Interface intuitiva para configurar email do remetente (Gmail)
- Gerenciamento de destinatários (adicionar/remover)
- Personalização de assunto e corpo da mensagem
- Teste de conexão SMTP

### 2. **Envio Automático**
- Envio automático após geração bem-sucedida dos relatórios
- Anexa automaticamente todos os 3 arquivos gerados (PDF, CSV, XLSX)
- Inclui informações do turno/janela no email
- Adiciona informações extras fornecidas pelo usuário

### 3. **Tratamento de Erros**
- Sistema robusto de tratamento de erros
- Notificações claras sobre problemas de envio
- Relatórios sempre são gerados mesmo se o email falhar

## ⚙️ Como Configurar

### Passo 1: Configurar Email do Remetente
1. Na interface principal, clique em **"✉ Configurar Email"**
2. Preencha seu email do Gmail
3. **IMPORTANTE**: Use uma **Senha de App** do Gmail, não sua senha normal
   - Acesse: Conta Google > Segurança > Verificação em duas etapas > Senhas de app
   - Crie uma senha específica para esta aplicação
4. Clique em **"Testar Conexão"** para verificar se está funcionando

### Passo 2: Adicionar Destinatários
1. Na seção "Destinatários", digite o email da supervisão/equipe
2. Clique em **"Adicionar"**
3. Repita para cada membro da equipe
4. Use **"Remover Selecionado"** para remover emails da lista

### Passo 3: Personalizar Mensagem
1. Edite o **Assunto** padrão conforme necessário
2. Personalize o **Corpo da mensagem** usando as variáveis:
   - `{data_hora}`: Data e hora do processamento
   - `{janela}`: Informação da janela/turno selecionado
3. Clique em **"Salvar Configurações"**

## 📋 Fluxo de Funcionamento

1. **Processamento Normal**: Usuário gera relatórios como sempre
2. **Geração Concluída**: Sistema gera os 3 arquivos (PDF, CSV, XLSX)
3. **Verificação de Email**: Sistema verifica se email está configurado
4. **Envio Automático**: 
   - Se configurado: Envia email com anexos automaticamente
   - Se não configurado: Exibe notificação para configurar
5. **Notificação de Resultado**: Informa sucesso ou erro do envio

## 📁 Estrutura de Arquivos

### Novos Arquivos Criados:
- `email_manager.py`: Gerenciamento completo do sistema de email
- `email_config_dialog.py`: Interface de configuração de email
- `config/email_config.json`: Arquivo de configurações salvas

### Arquivos Modificados:
- `gui_relatorio.py`: Interface principal atualizada
- `requirements.txt`: Dependências adicionadas

## 🔧 Configurações Técnicas

### Dependências Adicionadas:
```
secure-smtplib
email-validator
```

### Configurações SMTP:
- Servidor: `smtp.gmail.com`
- Porta: `587`
- Segurança: `TLS/STARTTLS`

## 🛡️ Segurança

- **Senhas de App**: Sistema projetado para usar Senhas de App do Gmail
- **Armazenamento Local**: Configurações salvas localmente em arquivo JSON
- **Validação de Email**: Formato de email validado antes de salvar
- **Teste de Conexão**: Verificação prévia da autenticação

## 📬 Template de Email Padrão

```
Assunto: Relatório de Expedição - Shopee

Corpo:
Olá,

Segue em anexo o relatório de expedição gerado automaticamente.

Dados do processamento:
- Data/Hora: [data_hora]
- Janela: [janela]
- Arquivos gerados: CSV, XLSX, PDF

Atenciosamente,
Sistema de Relatórios Shopee
```

## 🚨 Solução de Problemas

### Erro de Autenticação:
- Verifique se está usando Senha de App, não senha normal
- Confirme se a verificação em duas etapas está ativada no Gmail

### Email não enviado:
- Verifique conexão com internet
- Teste a conexão SMTP na configuração
- Confirme se há destinatários cadastrados

### Relatórios gerados mas email falhou:
- Sistema garante que relatórios sejam sempre gerados
- Email é uma funcionalidade adicional
- Verifique configurações e tente novamente

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique as mensagens de erro exibidas na interface
2. Use a função "Testar Conexão" para diagnosticar problemas
3. Revise este documento para configurações corretas

---

**Sistema implementado com foco na experiência do usuário e confiabilidade operacional.** 