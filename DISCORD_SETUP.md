# 🤖 Guia de Configuração - Bot Discord PrenotaMI

Este guia explica como criar e configurar um bot do Discord para controlar o PrenotaMI Bot via mensagens diretas (DM).

## 📋 O Que Você Vai Conseguir

Após seguir este guia, você poderá:

- ✅ Receber notificações no Discord quando houver vagas disponíveis
- ✅ Verificar status dos agendamentos via comando
- ✅ Iniciar/parar monitoramento automático
- ✅ Agendar automaticamente via Discord
- ✅ Controlar tudo via DM (mensagem direta)

## 🚀 Passo 1: Criar o Bot no Discord

### 1.1. Acessar o Portal de Desenvolvedores

1. Acesse: https://discord.com/developers/applications
2. Faça login com sua conta Discord
3. Clique em **"New Application"**
4. Dê um nome ao bot (ex: "PrenotaMI Bot")
5. Clique em **"Create"**

### 1.2. Configurar o Bot

1. No menu lateral, clique em **"Bot"**
2. Clique em **"Add Bot"** → **"Yes, do it!"**
3. Em **"Privileged Gateway Intents"**, ative:
   - ✅ **MESSAGE CONTENT INTENT**
   - ✅ **SERVER MEMBERS INTENT** (opcional)
   - ✅ **PRESENCE INTENT** (opcional)
4. Clique em **"Save Changes"**

### 1.3. Copiar o Token do Bot

1. Na seção **"TOKEN"**, clique em **"Reset Token"**
2. Confirme clicando em **"Yes, do it!"**
3. Clique em **"Copy"** para copiar o token
4. **⚠️ IMPORTANTE**: Guarde este token em segurança! Não compartilhe com ninguém.

## 🔗 Passo 2: Adicionar o Bot à Sua Conta

### 2.1. Gerar Link de Convite

1. No menu lateral, clique em **"OAuth2"** → **"URL Generator"**
2. Em **"SCOPES"**, selecione:
   - ✅ **bot**
3. Em **"BOT PERMISSIONS"**, selecione:
   - ✅ **Send Messages**
   - ✅ **Read Messages/View Channels**
   - ✅ **Read Message History**
   - ✅ **Embed Links**
4. Copie a URL gerada no final da página

### 2.2. Adicionar o Bot

1. Cole a URL copiada no navegador
2. Selecione **"Adicionar ao servidor"** ou **"Adicionar a DM"**
3. Para usar em DM, você pode:
   - Criar um servidor privado só para você
   - Ou adicionar o bot e depois enviar DM para ele

**Dica**: Crie um servidor privado chamado "Meu Bot" para facilitar.

## ⚙️ Passo 3: Configurar o Bot Localmente

### 3.1. Adicionar Token ao .env

Edite o arquivo `.env` e adicione o token do Discord:

```bash
nano .env
```

Adicione a linha:

```env
# Token do Bot Discord
DISCORD_BOT_TOKEN=seu_token_aqui_copiado_do_portal

# (Opcional) ID do usuário autorizado
DISCORD_USER_ID=seu_user_id_aqui
```

**Como descobrir seu User ID:**

1. No Discord, vá em **Configurações** → **Avançado**
2. Ative **"Modo Desenvolvedor"**
3. Clique com botão direito no seu nome
4. Clique em **"Copiar ID"**
5. Cole no `.env` como `DISCORD_USER_ID`

### 3.2. Exemplo de .env Completo

```env
# Credenciais PrenotaMI
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha_aqui

# Token do Bot Discord
DISCORD_BOT_TOKEN=SEU_TOKEN_AQUI

# ID do usuário autorizado (opcional)
DISCORD_USER_ID=123456789012345678

# Configurações
CHECK_INTERVAL_MINUTES=30
HEADLESS_MODE=true
```

## ▶️ Passo 4: Iniciar o Bot

### 4.1. Executar o Bot

```bash
cd prenotami_bot
python3 discord_bot.py
```

**Saída esperada:**

```
============================================================
BOT DISCORD PRENOTAMI INICIADO
============================================================
Bot: PrenotaMI Bot (ID: 123456789012345678)
Servidores: 1
Intervalo de verificação: 30 minutos
============================================================

Bot pronto para receber comandos!
Use !ajuda para ver os comandos disponíveis
```

### 4.2. Manter o Bot Rodando

Para manter o bot rodando em background:

```bash
# Opção 1: Usando nohup
nohup python3 discord_bot.py > discord_bot.log 2>&1 &

# Opção 2: Usando screen
screen -S discord_bot
python3 discord_bot.py
# Pressione Ctrl+A, depois D para desanexar

# Para voltar à sessão:
screen -r discord_bot
```

## 💬 Passo 5: Usar o Bot no Discord

### 5.1. Enviar DM para o Bot

1. No Discord, encontre o bot na lista de membros
2. Clique com botão direito → **"Mensagem"**
3. Ou vá no servidor e envie mensagem em qualquer canal

### 5.2. Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `!ajuda` | Lista todos os comandos | `!ajuda` |
| `!status` | Ver agendamentos ativos | `!status` |
| `!verificar` | Verificar disponibilidade agora | `!verificar` |
| `!agendar` | Tentar agendar automaticamente | `!agendar` |
| `!iniciar` | Iniciar monitoramento automático | `!iniciar` |
| `!parar` | Parar monitoramento | `!parar` |
| `!info` | Informações sobre o bot | `!info` |

### 5.3. Fluxo de Uso Recomendado

**Primeira vez:**

```
!ajuda
!status
!verificar
```

**Monitoramento automático:**

```
!iniciar
```

O bot verificará automaticamente a cada 30 minutos e enviará notificação quando encontrar vaga.

**Quando receber notificação de vaga:**

```
!agendar
```

**Para parar o monitoramento:**

```
!parar
```

## 📱 Exemplo de Uso Completo

### Cenário: Monitorar e Agendar via Discord

```
Você: !info
Bot: [Mostra status do bot]

Você: !status
Bot: ⚠️ Você não possui agendamentos ativos

Você: !verificar
Bot: ⚠️ Sem Vagas
     Nenhuma data disponível no momento

Você: !iniciar
Bot: ▶️ Monitoramento Iniciado
     O bot verificará a cada 30 minutos

[30 minutos depois...]

Bot: 🎉 VAGA DISPONÍVEL ENCONTRADA!
     Encontradas 5 datas disponíveis
     📅 2025-12-05
     📅 2025-12-08
     Use !agendar AGORA!

Você: !agendar
Bot: ✅ Agendamento Realizado!
     Código: PRN123456789

Você: !status
Bot: ✅ Total de agendamentos: 1
     1. PASSAPORTO
     Código: PRN123456789
     Data: 2025-12-05 10:30
```

## 🔒 Segurança

### Proteger Seu Bot

1. **Nunca compartilhe o token**: O token dá controle total sobre o bot
2. **Use DISCORD_USER_ID**: Restringe o bot apenas para você
3. **Servidor privado**: Crie um servidor só seu para o bot
4. **Regenerar token**: Se o token vazar, regenere imediatamente no portal

### Regenerar Token (Se Necessário)

1. Acesse https://discord.com/developers/applications
2. Selecione seu bot
3. Vá em **"Bot"** → **"Reset Token"**
4. Copie o novo token
5. Atualize o `.env` com o novo token
6. Reinicie o bot

## 🛠️ Solução de Problemas

### Problema: "Token inválido"

**Solução:**
1. Verifique se copiou o token corretamente
2. Certifique-se de que não há espaços extras no `.env`
3. Regenere o token no portal se necessário

### Problema: "Bot não responde"

**Solução:**
1. Verifique se o bot está online (luz verde no Discord)
2. Certifique-se de que ativou **MESSAGE CONTENT INTENT**
3. Verifique se o bot tem permissões para ler/enviar mensagens

### Problema: "Você não está autorizado"

**Solução:**
1. Verifique se configurou `DISCORD_USER_ID` corretamente
2. Remova essa linha do `.env` para permitir todos os usuários
3. Certifique-se de copiar o ID correto (modo desenvolvedor ativado)

### Problema: Bot desconecta sozinho

**Solução:**
1. Use `nohup` ou `screen` para manter em background
2. Verifique logs: `tail -f discord_bot.log`
3. Certifique-se de que o servidor não está hibernando

## 📊 Monitoramento e Logs

### Ver Logs em Tempo Real

```bash
# Se usando nohup
tail -f discord_bot.log

# Se usando screen
screen -r discord_bot
```

### Verificar se o Bot Está Rodando

```bash
# Ver processo
ps aux | grep discord_bot.py

# Parar o bot
pkill -f discord_bot.py
```

## 🚀 Recursos Avançados

### Executar Automaticamente ao Iniciar (Systemd)

Crie um serviço systemd:

```bash
sudo nano /etc/systemd/system/prenotami-discord.service
```

Conteúdo:

```ini
[Unit]
Description=PrenotaMI Discord Bot
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/caminho/para/prenotami_bot
ExecStart=/usr/bin/python3 /caminho/para/prenotami_bot/discord_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ativar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable prenotami-discord
sudo systemctl start prenotami-discord
sudo systemctl status prenotami-discord
```

### Múltiplos Usuários

Para permitir que várias pessoas usem o bot:

1. Remova `DISCORD_USER_ID` do `.env`
2. Ou crie uma lista de IDs autorizados no código

## 📝 Checklist de Configuração

- [ ] Criar aplicação no Discord Developer Portal
- [ ] Criar bot e copiar token
- [ ] Ativar MESSAGE CONTENT INTENT
- [ ] Gerar URL de convite
- [ ] Adicionar bot ao servidor/DM
- [ ] Adicionar token ao `.env`
- [ ] (Opcional) Adicionar DISCORD_USER_ID ao `.env`
- [ ] Testar bot com `python3 discord_bot.py`
- [ ] Enviar `!ajuda` no Discord
- [ ] Testar comando `!status`
- [ ] Testar comando `!verificar`
- [ ] Configurar execução em background

## 🎉 Pronto!

Seu bot Discord está configurado e pronto para uso! Agora você pode:

- ✅ Receber notificações instantâneas no Discord
- ✅ Controlar o bot de qualquer lugar
- ✅ Monitorar vagas automaticamente
- ✅ Agendar via comando simples

**Dica Final**: Deixe o bot rodando em um servidor ou computador que fique sempre ligado para receber notificações 24/7.

---

**Precisa de ajuda?** Consulte o README.md principal ou EXAMPLES.md para mais informações.
