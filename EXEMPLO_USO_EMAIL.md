# 📧 Exemplo Prático - Sistema de Email Automático

## 🎯 Cenário de Uso

**Situação:** João é responsável pelo relatório de expedição do turno da manhã e precisa enviá-lo automaticamente para sua supervisora Maria e o coordenador Pedro.

## 📝 Passo a Passo Completo

### Etapa 1: Primeira Configuração (Só faz uma vez)

1. **Abrir a configuração de email:**
   - Execute a aplicação normalmente
   - No topo da tela, clique no botão **"✉ Configurar Email"**

2. **Configurar o remetente:**
   - Email: `joao.expedição@shopee.com.br`
   - Senha de App: `abcd efgh ijkl mnop` (obtida no Gmail)
   - Clique em **"Testar Conexão"** ✅

3. **Adicionar destinatários:**
   ```
   maria.supervisora@shopee.com.br    [Adicionar]
   pedro.coordenador@shopee.com.br    [Adicionar]
   equipe.logistica@shopee.com.br     [Adicionar]
   ```

4. **Personalizar a mensagem:**
   - **Assunto:** `Relatório Expedição Manhã - {data_hora}`
   - **Corpo:**
   ```
   Bom dia equipe,

   Segue em anexo o relatório de expedição da {janela}.

   📊 Dados do processamento:
   - Data/Hora: {data_hora}
   - Turno: {janela}
   - Arquivos: PDF (completo), CSV (dados), XLSX (planilha)

   📋 Informações do fechamento:
   [Automaticamente incluídas as informações adicionais digitadas]

   Qualquer dúvida, estou à disposição.

   Att,
   João - Expedição Manhã
   ```

5. **Salvar configurações** ✅

### Etapa 2: Uso Diário (Processo normal)

1. **Processar relatório normalmente:**
   - Selecionar arquivos de expedição (Assignment)
   - Selecionar arquivo de conferência (Audit)
   - Escolher pasta de destino
   - Adicionar informações extras (ex: "Atraso de 30min devido chuva")
   - Clicar em **"Gerar Relatórios"**

2. **Sistema processa automaticamente:**
   ```
   ⏳ Processando...
   ✅ Relatórios gerados com sucesso!
   📧 Enviando email...
   ✅ Email enviado com sucesso para: maria.supervisora@shopee.com.br, pedro.coordenador@shopee.com.br, equipe.logistica@shopee.com.br
   ```

3. **Email enviado automaticamente contém:**
   - **Anexos:** 
     - `relatorio_expedicao.pdf` (relatório completo)
     - `resumo_expedicao.csv` (dados em CSV)
     - `relatorio_expedicao.xlsx` (planilha formatada)
   - **Assunto:** `Relatório Expedição Manhã - 15/12/2024 às 09:30`
   - **Corpo personalizado** com todas as informações

## 📬 Exemplo de Email Recebido

```
De: joao.expedição@shopee.com.br
Para: maria.supervisora@shopee.com.br, pedro.coordenador@shopee.com.br, equipe.logistica@shopee.com.br
Assunto: Relatório Expedição Manhã - 15/12/2024 às 09:30

Bom dia equipe,

Segue em anexo o relatório de expedição da Manhã (Madrugada) - 04:00 às 09:00.

📊 Dados do processamento:
- Data/Hora: 15/12/2024 às 09:30
- Turno: Manhã (Madrugada) - 04:00 às 09:00
- Arquivos: PDF (completo), CSV (dados), XLSX (planilha)

📋 Informações do fechamento:
Atraso de 30min devido chuva forte. Todas as rotas foram expedidas com sucesso.
Observação: Rota 1234 ficou no piso por problema no sistema.

Qualquer dúvida, estou à disposição.

Att,
João - Expedição Manhã

📎 Anexos:
- relatorio_expedicao.pdf (1.2 MB)
- resumo_expedicao.csv (45 KB)  
- relatorio_expedicao.xlsx (892 KB)
```

## 🚨 Situações Especiais

### Se o email falhar:
```
⚠️ Relatórios gerados com sucesso, mas houve um erro no envio do email:
❌ Erro de autenticação. Verifique as credenciais do remetente.

Deseja abrir a pasta dos relatórios?
[Sim] [Não]
```
➡️ **Resultado:** Relatórios são salvos normalmente, email pode ser reenviado depois

### Se email não estiver configurado:
```
ℹ️ Relatórios gerados com sucesso!
📁 Local: C:\Relatorios\2024-12-15_09-30

ℹ️ Email automático não configurado.
Configure em "Configurações de Email" para envio automático.

Deseja abrir a pasta?
[Sim] [Não]
```
➡️ **Resultado:** Sistema funciona normalmente, apenas sem envio automático

## 💡 Dicas de Uso

### ✅ Boas práticas:
- Configure uma vez e use sempre
- Teste a conexão depois de configurar
- Use emails corporativos quando possível
- Personalize a mensagem para sua equipe

### ⚠️ Evite:
- Usar senha normal do Gmail (use Senha de App)
- Deixar campos em branco na configuração
- Adicionar emails inválidos na lista

### 🔧 Manutenção:
- Atualize destinatários quando necessário
- Revise a mensagem periodicamente
- Mantenha backup das configurações

---

**Com essa configuração, o relatório será enviado automaticamente toda vez que for processado, economizando tempo e garantindo que toda a equipe receba as informações pontualmente!** 🚀 