# 🚀 COMECE AQUI - Bot PrenotaMI

**Bem-vindo ao Bot PrenotaMI!** Este documento vai guiá-lo do início ao fim.

---

## 📦 O Que Você Tem

Um bot completo para automatizar o agendamento de renovação de passaporte no sistema PrenotaMI do Consulado da Itália em Paris, com duas interfaces:

1. **🖥️ Interface CLI** (Linha de Comando)
2. **💬 Bot Discord** (Controle via DM - NOVO!)

---

## ⚡ Início Rápido (5 minutos)

### Opção A: Usar via Linha de Comando

```bash
# 1. Configurar credenciais
cp .env.example .env
nano .env  # Adicionar email e senha

# 2. Testar instalação
python3 test_bot.py

# 3. Fazer primeiro login
python3 cli.py login

# 4. Verificar disponibilidade
python3 cli.py check

# 5. Iniciar monitoramento
python3 monitor.py --auto-book
```

📖 **Guia completo**: `QUICKSTART.md`

### Opção B: Usar via Discord (RECOMENDADO!)

```bash
# 1. Configurar credenciais PrenotaMI
cp .env.example .env
nano .env  # Adicionar email e senha

# 2. Adicionar token do Discord ao .env
# (veja INVITE_URLS.txt para instruções)

# 3. Iniciar bot Discord
python3 discord_bot.py

# 4. No Discord, enviar:
!ajuda
!iniciar
```

📖 **Guia completo**: `DISCORD_QUICKSTART.md`

---

## 📚 Documentação Disponível

### Para Iniciantes

| Arquivo | Descrição | Tempo |
|---------|-----------|-------|
| **START_HERE.md** | Este arquivo - comece aqui! | 2 min |
| **QUICKSTART.md** | Guia rápido CLI | 5 min |
| **DISCORD_QUICKSTART.md** | Guia rápido Discord | 5 min |
| **INVITE_URLS.txt** | URLs prontas para adicionar bot | 1 min |

### Documentação Completa

| Arquivo | Descrição |
|---------|-----------|
| **README.md** | Documentação completa do projeto |
| **DISCORD_SETUP.md** | Guia detalhado de configuração Discord |
| **DISCORD_APP_INFO.md** | Informações para Developer Portal |
| **EXAMPLES.md** | 10 exemplos práticos de uso |
| **SUMMARY.md** | Resumo executivo do projeto |

### Scripts

| Arquivo | Descrição |
|---------|-----------|
| `prenotami_bot.py` | Classe principal do bot |
| `cli.py` | Interface de linha de comando |
| `monitor.py` | Monitoramento contínuo |
| `discord_bot.py` | Bot do Discord |
| `test_bot.py` | Script de testes |
| `generate_invite_url.py` | Gerador de URLs de convite |

---

## 🎯 Qual Interface Escolher?

### Use CLI se você:
- ✅ Prefere terminal/linha de comando
- ✅ Quer controle local direto
- ✅ Não usa Discord

### Use Discord se você:
- ✅ Quer receber notificações no celular
- ✅ Prefere interface visual (embeds)
- ✅ Quer controlar de qualquer lugar
- ✅ Usa Discord regularmente

**💡 Dica**: Você pode usar **ambos** ao mesmo tempo!

---

## 🔧 Configuração Inicial (Obrigatória)

### 1. Instalar Dependências

```bash
sudo pip3 install selenium webdriver-manager python-dotenv discord.py
```

### 2. Configurar Credenciais

Edite o arquivo `.env`:

```env
# Obrigatório
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha_aqui

# Opcional (apenas para Discord)
DISCORD_BOT_TOKEN=seu_token_aqui
DISCORD_USER_ID=seu_id_aqui

# Configurações
CHECK_INTERVAL_MINUTES=30
HEADLESS_MODE=false
```

### 3. Testar Instalação

```bash
python3 test_bot.py
```

**Resultado esperado**: Todos os testes devem passar ✅

---

## 🤖 Configurar Bot Discord (Opcional mas Recomendado)

### Passo 1: Configurar no Developer Portal

Você já tem:
- ✅ Application ID: `1441508569110417590`
- ✅ Public Key: `dab60be1ab8d82d963a2ed07461b5895af350e3af9ad2a2417b81f3cf24955a9`

**Falta fazer:**

1. Ativar **MESSAGE CONTENT INTENT**:
   - Acesse: https://discord.com/developers/applications/1441508569110417590
   - Menu **Bot** → **Privileged Gateway Intents**
   - ✅ Ativar **MESSAGE CONTENT INTENT**
   - Salvar mudanças

2. Copiar o **TOKEN**:
   - Menu **Bot** → **Reset Token**
   - Copiar o token
   - Adicionar ao `.env`: `DISCORD_BOT_TOKEN=token_aqui`

3. Ativar **User Install** (para DM):
   - Menu **Installation**
   - **Default Install Settings**
   - ✅ Ativar **User Install**
   - Salvar

### Passo 2: Adicionar o Bot

Abra uma destas URLs no navegador:

**Para DM (Recomendado):**
```
https://discord.com/api/oauth2/authorize?client_id=1441508569110417590&permissions=274877975552&scope=bot%20applications.commands&integration_type=1
```

**Para Servidor:**
```
https://discord.com/api/oauth2/authorize?client_id=1441508569110417590&permissions=274877975552&scope=bot
```

📄 **Mais URLs**: Veja `INVITE_URLS.txt`

### Passo 3: Iniciar o Bot

```bash
python3 discord_bot.py
```

### Passo 4: Testar no Discord

Envie uma mensagem para o bot:
```
!ajuda
```

---

## 💬 Comandos Discord

| Comando | Descrição |
|---------|-----------|
| `!ajuda` | Ver todos os comandos |
| `!info` | Informações sobre o bot |
| `!status` | Ver seus agendamentos |
| `!verificar` | Verificar disponibilidade agora |
| `!iniciar` | Iniciar monitoramento automático |
| `!parar` | Parar monitoramento |
| `!agendar` | Tentar agendar automaticamente |

---

## 🖥️ Comandos CLI

| Comando | Descrição |
|---------|-----------|
| `python3 cli.py status` | Ver agendamentos |
| `python3 cli.py check` | Verificar disponibilidade |
| `python3 cli.py book` | Tentar agendar |
| `python3 cli.py login` | Fazer login e salvar sessão |
| `python3 monitor.py --auto-book` | Monitorar e agendar |
| `python3 test_bot.py` | Testar instalação |

---

## 🎯 Fluxo de Uso Recomendado

### Primeira Vez (CLI)

```bash
# 1. Configurar
cp .env.example .env
nano .env

# 2. Testar
python3 test_bot.py

# 3. Login inicial (resolver CAPTCHA)
python3 cli.py login

# 4. Verificar status
python3 cli.py status
```

### Primeira Vez (Discord)

```bash
# 1. Configurar .env com credenciais PrenotaMI e Discord
nano .env

# 2. Iniciar bot
python3 discord_bot.py

# 3. No Discord:
!ajuda
!status
!iniciar
```

### Uso Diário

**Via Discord:**
```
!iniciar     # Deixa monitorando
[Bot avisa quando houver vaga]
!agendar     # Agenda automaticamente
```

**Via CLI:**
```bash
python3 monitor.py --auto-book
```

---

## ⏰ Melhor Horário para Conseguir Vaga

O sistema PrenotaMI libera novos agendamentos **diariamente às 20:00** (horário da Itália).

**Estratégia:**
1. Iniciar monitoramento às **19:45**
2. Usar intervalo de **5 minutos**
3. Deixar rodando por **2-3 horas**

**Discord:**
```
!iniciar
```

**CLI:**
```bash
python3 monitor.py --interval 5 --auto-book --max-attempts 30
```

---

## 🔒 Segurança

### Dados Locais
- ✅ Credenciais armazenadas apenas no `.env` local
- ✅ Cookies salvos apenas no seu computador
- ✅ Nenhum dado enviado para servidores externos
- ✅ Token Discord é privado (nunca compartilhe!)

### Proteção do Token Discord
⚠️ **NUNCA compartilhe o token do Discord!**

Se o token vazar:
1. Acesse Developer Portal
2. Menu **Bot** → **Reset Token**
3. Copie o novo token
4. Atualize o `.env`

---

## 🛠️ Solução de Problemas

### CLI não funciona

```bash
# Verificar instalação
python3 test_bot.py

# Verificar credenciais
cat .env

# Fazer novo login
python3 cli.py login --force
```

### Discord não responde

**Checklist:**
- [ ] MESSAGE CONTENT INTENT ativado?
- [ ] Token correto no `.env`?
- [ ] Bot está online (luz verde)?
- [ ] Bot tem permissões?

**Solução:**
```bash
# Ver logs
python3 discord_bot.py

# Verificar se bot está rodando
ps aux | grep discord_bot
```

### "Nenhuma data disponível"

**Normal!** Vagas esgotam rápido.

**Solução:**
- Use monitoramento contínuo
- Execute próximo às 20:00 (horário da Itália)
- Use intervalo curto (5-10 minutos)

---

## 📞 Precisa de Ajuda?

### Documentação por Tópico

| Problema | Consulte |
|----------|----------|
| Configuração inicial | `QUICKSTART.md` |
| Configurar Discord | `DISCORD_SETUP.md` |
| Exemplos práticos | `EXAMPLES.md` |
| Informações técnicas | `README.md` |
| Resumo do projeto | `SUMMARY.md` |

### Arquivos de Referência

| Arquivo | Quando Usar |
|---------|-------------|
| `INVITE_URLS.txt` | Adicionar bot ao Discord |
| `DISCORD_APP_INFO.md` | Configurar Developer Portal |
| `.env.example` | Ver exemplo de configuração |

---

## ✅ Checklist Completo

### Configuração Básica
- [ ] Instalar dependências
- [ ] Criar arquivo `.env`
- [ ] Adicionar email e senha PrenotaMI
- [ ] Executar `python3 test_bot.py`
- [ ] Fazer primeiro login: `python3 cli.py login`

### Configuração Discord (Opcional)
- [ ] Ativar MESSAGE CONTENT INTENT
- [ ] Copiar token do bot
- [ ] Adicionar token ao `.env`
- [ ] Ativar User Install
- [ ] Adicionar bot via URL
- [ ] Iniciar: `python3 discord_bot.py`
- [ ] Testar: `!ajuda` no Discord

### Primeiro Uso
- [ ] Verificar status: `!status` ou `python3 cli.py status`
- [ ] Verificar disponibilidade: `!verificar` ou `python3 cli.py check`
- [ ] Iniciar monitoramento: `!iniciar` ou `python3 monitor.py --auto-book`

---

## 🎉 Pronto!

Você está pronto para usar o bot! Escolha sua interface preferida:

**🖥️ CLI:**
```bash
python3 monitor.py --auto-book
```

**💬 Discord:**
```bash
python3 discord_bot.py
# No Discord: !iniciar
```

---

## 🚀 Próximos Passos

1. **Ler o guia rápido** da sua interface escolhida
2. **Fazer o primeiro login** e resolver o CAPTCHA
3. **Iniciar monitoramento** próximo às 20:00 (horário da Itália)
4. **Aguardar notificação** quando houver vaga
5. **Agendar automaticamente** quando o bot avisar

---

**Boa sorte com seu agendamento!** 🍀🇮🇹

*Desenvolvido para facilitar o processo de agendamento consular*
