# 🚀 Guia de Deploy - Bot PrenotaMI na Nuvem

Este guia explica como hospedar o bot Discord na nuvem para que funcione 24/7, mesmo quando seu computador estiver desligado.

---

## 🌐 Opções de Hospedagem

### Recomendadas (Gratuitas)

| Serviço | Plano Gratuito | Vantagens | Limitações |
|---------|----------------|-----------|------------|
| **Railway** | $5 crédito/mês | Fácil setup, Docker | Requer cartão |
| **Render** | 750h/mês | Sem cartão, simples | Hiberna após inatividade |
| **Fly.io** | 3 VMs pequenas | Bom para Docker | Configuração mais técnica |

**Recomendação**: Use **Railway** se tiver cartão (não cobra até esgotar créditos gratuitos) ou **Render** se não tiver.

---

## 📋 Pré-requisitos

Antes de fazer deploy, você precisa:

1. ✅ Conta no serviço de hospedagem (Railway ou Render)
2. ✅ Bot Discord configurado (Application ID, Token)
3. ✅ Credenciais do PrenotaMI (email e senha)
4. ✅ Conta GitHub (para conectar o repositório)

---

## 🚂 Opção 1: Deploy no Railway (Recomendado)

### Vantagens
- ✅ Setup mais simples
- ✅ Suporte nativo a Docker
- ✅ Logs em tempo real
- ✅ Variáveis de ambiente fáceis
- ✅ $5 de crédito gratuito por mês

### Passo a Passo

#### 1. Criar Conta no Railway

1. Acesse: https://railway.app
2. Clique em **"Start a New Project"**
3. Faça login com GitHub

#### 2. Preparar Repositório GitHub

**Opção A: Criar novo repositório**

```bash
cd prenotami_bot

# Inicializar Git
git init

# Criar .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
.env
*.pkl
*.json
*.log
.vscode/
.idea/
EOF

# Adicionar arquivos
git add .
git commit -m "Initial commit - PrenotaMI Bot"

# Criar repositório no GitHub e conectar
# (siga instruções do GitHub)
git remote add origin https://github.com/seu-usuario/prenotami-bot.git
git branch -M main
git push -u origin main
```

**Opção B: Fork do repositório existente**

Se você já tem o código em um repositório, apenas conecte-o ao Railway.

#### 3. Criar Projeto no Railway

1. No Railway, clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Autorize o Railway a acessar seus repositórios
4. Selecione o repositório `prenotami-bot`
5. Railway detectará automaticamente o `Dockerfile`

#### 4. Configurar Variáveis de Ambiente

No Railway, vá em **Variables** e adicione:

```env
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha_aqui
DISCORD_BOT_TOKEN=seu_token_discord
DISCORD_USER_ID=seu_id_discord
CHECK_INTERVAL_MINUTES=30
HEADLESS_MODE=true
```

**⚠️ IMPORTANTE**: Nunca commite o arquivo `.env` no Git!

#### 5. Deploy

1. Railway iniciará o deploy automaticamente
2. Aguarde o build (pode levar 3-5 minutos)
3. Verifique os logs em **"Deployments"**

#### 6. Verificar Status

Nos logs, você deve ver:

```
============================================================
BOT DISCORD PRENOTAMI INICIADO
============================================================
Bot: PrenotaMIBot (ID: ...)
Bot pronto para receber comandos!
```

#### 7. Testar no Discord

Envie uma mensagem para o bot:
```
!ajuda
```

### Monitoramento no Railway

- **Logs**: Clique em **"View Logs"** para ver logs em tempo real
- **Métricas**: Veja uso de CPU e memória
- **Restart**: Clique em **"Restart"** se necessário

---

## 🎨 Opção 2: Deploy no Render

### Vantagens
- ✅ Não requer cartão de crédito
- ✅ 750 horas gratuitas por mês
- ✅ Setup simples
- ✅ SSL automático

### Limitações
- ⚠️ Hiberna após 15 minutos de inatividade (plano gratuito)
- ⚠️ Pode levar 30-60s para "acordar"

### Passo a Passo

#### 1. Criar Conta no Render

1. Acesse: https://render.com
2. Clique em **"Get Started"**
3. Faça login com GitHub

#### 2. Preparar Repositório GitHub

(Mesmo processo do Railway - veja acima)

#### 3. Criar Web Service

1. No Render Dashboard, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: `prenotami-bot`
   - **Environment**: `Docker`
   - **Plan**: `Free`

#### 4. Configurar Variáveis de Ambiente

Em **Environment**, adicione:

```env
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha_aqui
DISCORD_BOT_TOKEN=seu_token_discord
DISCORD_USER_ID=seu_id_discord
CHECK_INTERVAL_MINUTES=30
HEADLESS_MODE=true
```

#### 5. Deploy

1. Clique em **"Create Web Service"**
2. Render iniciará o build automaticamente
3. Aguarde 5-10 minutos (primeira vez é mais lento)

#### 6. Manter o Bot Ativo (Importante!)

Como o plano gratuito hiberna, você tem duas opções:

**Opção A: Usar um serviço de ping**

Use um serviço como UptimeRobot para fazer ping a cada 5 minutos:

1. Acesse: https://uptimerobot.com
2. Adicione um monitor HTTP
3. URL: `https://seu-app.onrender.com`
4. Intervalo: 5 minutos

**Opção B: Upgrade para plano pago** ($7/mês - sem hibernação)

#### 7. Verificar Logs

No Render:
1. Clique no seu serviço
2. Vá em **"Logs"**
3. Verifique se o bot iniciou corretamente

---

## 🐳 Opção 3: Deploy Manual com Docker

Se você tem um VPS (DigitalOcean, Linode, AWS, etc.):

### 1. Instalar Docker no Servidor

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. Clonar Repositório

```bash
git clone https://github.com/seu-usuario/prenotami-bot.git
cd prenotami-bot
```

### 3. Criar arquivo .env

```bash
nano .env
```

Adicione suas variáveis:
```env
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha_aqui
DISCORD_BOT_TOKEN=seu_token_discord
DISCORD_USER_ID=seu_id_discord
CHECK_INTERVAL_MINUTES=30
HEADLESS_MODE=true
```

### 4. Build e Run

```bash
# Build da imagem
docker build -t prenotami-bot .

# Executar container
docker run -d \
  --name prenotami-bot \
  --env-file .env \
  --restart unless-stopped \
  prenotami-bot
```

### 5. Verificar Logs

```bash
docker logs -f prenotami-bot
```

### 6. Comandos Úteis

```bash
# Parar o bot
docker stop prenotami-bot

# Iniciar o bot
docker start prenotami-bot

# Reiniciar o bot
docker restart prenotami-bot

# Ver logs
docker logs prenotami-bot

# Remover container
docker rm -f prenotami-bot
```

---

## 🔧 Configuração Avançada

### Ajustar Intervalo de Verificação

Por padrão, o bot verifica a cada 30 minutos. Para mudar:

```env
CHECK_INTERVAL_MINUTES=15  # Verificar a cada 15 minutos
```

**⚠️ Atenção**: Intervalos muito curtos podem sobrecarregar o sistema PrenotaMI.

### Restringir Acesso ao Bot

Para permitir apenas você usar o bot:

```env
DISCORD_USER_ID=seu_id_aqui
```

**Como descobrir seu ID:**
1. Discord → Configurações → Avançado
2. Ativar "Modo Desenvolvedor"
3. Clicar com botão direito no seu nome → "Copiar ID"

### Modo Headless

O bot roda em modo headless (sem interface gráfica) por padrão na nuvem:

```env
HEADLESS_MODE=true
```

---

## 📊 Monitoramento e Manutenção

### Verificar Status do Bot

**No Discord:**
```
!info
```

**Nos Logs (Railway/Render):**
- Procure por "Bot pronto para receber comandos"
- Verifique se não há erros de autenticação

### Logs Importantes

**Sucesso:**
```
✓ Login realizado com sucesso!
✓ Cookies salvos
Bot pronto para receber comandos!
```

**Erros Comuns:**
```
✗ Erro ao fazer login no PrenotaMI
  → Verifique PRENOTAMI_EMAIL e PRENOTAMI_PASSWORD

❌ Token inválido
  → Verifique DISCORD_BOT_TOKEN

⚠️ Cookies expirados
  → Normal após alguns dias, bot fará novo login
```

### Reiniciar o Bot

**Railway:**
1. Dashboard → Seu projeto
2. Clique em **"Restart"**

**Render:**
1. Dashboard → Seu serviço
2. Manual Deploy → **"Clear build cache & deploy"**

**Docker (VPS):**
```bash
docker restart prenotami-bot
```

---

## 🔒 Segurança

### Boas Práticas

1. ✅ **Nunca** commite o arquivo `.env` no Git
2. ✅ Use variáveis de ambiente do serviço de hospedagem
3. ✅ Mantenha o token Discord privado
4. ✅ Use `DISCORD_USER_ID` para restringir acesso
5. ✅ Regenere o token se houver vazamento

### Proteger Credenciais

**No Git:**
```bash
# Adicionar .env ao .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
```

**Verificar se .env não está no repositório:**
```bash
git ls-files | grep .env
# Não deve retornar nada
```

---

## 🆘 Solução de Problemas

### Bot não inicia

**Verificar:**
1. Variáveis de ambiente configuradas corretamente?
2. Token Discord está correto?
3. Logs mostram algum erro?

**Solução:**
```bash
# Ver logs completos
# Railway: View Logs
# Render: Logs tab
# Docker: docker logs prenotami-bot
```

### Bot desconecta frequentemente

**Possíveis causas:**
1. Plano gratuito hibernando (Render)
2. Erro de autenticação no PrenotaMI
3. Problema de rede

**Solução:**
- Use serviço de ping (UptimeRobot)
- Verifique credenciais PrenotaMI
- Considere upgrade para plano pago

### "Cookies expirados"

**Normal!** O bot fará novo login automaticamente.

Se persistir:
1. Verifique credenciais PrenotaMI
2. Teste login manual localmente
3. Verifique se conta não está bloqueada

### Build falha

**Erro comum:** "Chromium not found"

**Solução:** O Dockerfile já inclui Chromium. Se falhar:
1. Verifique se o Dockerfile está no repositório
2. Force rebuild (clear cache)
3. Verifique logs de build

---

## 💰 Custos

### Railway
- **Gratuito**: $5 crédito/mês (~500h de uso)
- **Hobby**: $5/mês (sem limites)
- **Estimativa**: Bot usa ~$2-3/mês

### Render
- **Gratuito**: 750h/mês (suficiente para 24/7)
- **Starter**: $7/mês (sem hibernação)

### VPS (DigitalOcean, Linode)
- **Básico**: $5-6/mês
- **Vantagem**: Controle total, múltiplos apps

---

## ✅ Checklist de Deploy

### Antes do Deploy
- [ ] Repositório GitHub criado
- [ ] `.gitignore` configurado (sem .env)
- [ ] `Dockerfile` no repositório
- [ ] `requirements.txt` atualizado
- [ ] Bot Discord configurado (TOKEN copiado)
- [ ] Credenciais PrenotaMI prontas

### Durante o Deploy
- [ ] Conta criada no serviço (Railway/Render)
- [ ] Repositório conectado
- [ ] Variáveis de ambiente configuradas
- [ ] Build completado com sucesso
- [ ] Logs mostram "Bot pronto"

### Após o Deploy
- [ ] Testar `!ajuda` no Discord
- [ ] Testar `!status`
- [ ] Testar `!verificar`
- [ ] Configurar monitoramento (UptimeRobot se Render)
- [ ] Salvar URLs de acesso aos logs

---

## 🎯 Próximos Passos

1. **Escolher serviço**: Railway (com cartão) ou Render (sem cartão)
2. **Criar repositório GitHub** com o código
3. **Seguir guia** específico do serviço escolhido
4. **Configurar variáveis** de ambiente
5. **Fazer deploy** e verificar logs
6. **Testar no Discord** com `!ajuda`
7. **Iniciar monitoramento** com `!iniciar`

---

## 📞 Suporte

Se tiver problemas:

1. **Verificar logs** do serviço de hospedagem
2. **Testar localmente** primeiro: `python3 discord_bot.py`
3. **Consultar documentação**:
   - Railway: https://docs.railway.app
   - Render: https://render.com/docs
4. **Verificar status** do Discord: https://discordstatus.com

---

**Seu bot estará rodando 24/7 na nuvem!** 🚀☁️

*Desenvolvido para facilitar o agendamento consular*
