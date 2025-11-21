# 🚀 Guia Final - Deploy do Bot na Nuvem (24/7)

## 📋 O Que Você Vai Fazer

Hospedar o bot Discord em um servidor na nuvem para que funcione **24 horas por dia, 7 dias por semana**, mesmo com seu computador desligado.

---

## ⚡ Opção Rápida: Railway (10 minutos)

### Por que Railway?
- ✅ Mais fácil de configurar
- ✅ $5 de crédito gratuito por mês (suficiente para o bot)
- ✅ Suporte nativo a Docker
- ✅ Logs em tempo real
- ✅ Deploy automático via Git

### Passo 1: Criar Repositório no GitHub

1. **Acesse GitHub**: https://github.com/new

2. **Criar repositório**:
   - Nome: `prenotami-bot`
   - Descrição: "Bot para agendamento PrenotaMI"
   - Visibilidade: **Private** (recomendado)
   - ✅ Não adicione README, .gitignore ou licença

3. **No seu computador**, abra o terminal na pasta do bot:

```bash
cd prenotami_bot

# Inicializar Git
git init

# Adicionar todos os arquivos
git add .

# Fazer primeiro commit
git commit -m "Initial commit - PrenotaMI Bot"

# Conectar ao GitHub (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/prenotami-bot.git

# Enviar código
git branch -M main
git push -u origin main
```

**✅ Pronto!** Seu código está no GitHub.

### Passo 2: Criar Conta no Railway

1. **Acesse**: https://railway.app

2. **Clique em "Start a New Project"**

3. **Login com GitHub**: Clique em "Login with GitHub"

4. **Autorize o Railway** a acessar seus repositórios

### Passo 3: Fazer Deploy

1. **No Railway Dashboard**, clique em **"New Project"**

2. **Selecione "Deploy from GitHub repo"**

3. **Escolha o repositório** `prenotami-bot`

4. **Railway detectará automaticamente** o `Dockerfile` e iniciará o build

5. **Aguarde 3-5 minutos** para o build completar

### Passo 4: Configurar Variáveis de Ambiente

1. **No Railway**, clique no seu projeto

2. **Vá em "Variables"** (ícone de engrenagem)

3. **Clique em "New Variable"** e adicione **uma por uma**:

```
PRENOTAMI_EMAIL
seu_email@exemplo.com

PRENOTAMI_PASSWORD
sua_senha_aqui

DISCORD_BOT_TOKEN
seu_token_discord_aqui

DISCORD_USER_ID
seu_id_discord_aqui

CHECK_INTERVAL_MINUTES
30

HEADLESS_MODE
true
```

**⚠️ IMPORTANTE**: 
- Copie e cole exatamente como está
- Não adicione aspas ou espaços extras
- `DISCORD_USER_ID` é opcional (deixe vazio para permitir todos)

4. **Clique em "Deploy"** ou aguarde o redeploy automático

### Passo 5: Verificar Status

1. **No Railway**, clique em **"Deployments"**

2. **Clique no deployment mais recente**

3. **Veja os logs**. Você deve ver:

```
============================================================
BOT DISCORD PRENOTAMI INICIADO
============================================================
Bot: PrenotaMIBot (ID: ...)
Bot pronto para receber comandos!
```

**✅ Se ver isso, o bot está funcionando!**

### Passo 6: Testar no Discord

1. **Abra o Discord**

2. **Envie mensagem para o bot**:
```
!ajuda
```

3. **O bot deve responder** com a lista de comandos

4. **Teste outros comandos**:
```
!info
!status
!verificar
```

### Passo 7: Iniciar Monitoramento

```
!iniciar
```

**Pronto!** O bot agora monitora automaticamente e enviará notificação quando houver vaga.

---

## 🎨 Opção Alternativa: Render (Sem Cartão)

### Por que Render?
- ✅ Não requer cartão de crédito
- ✅ 750 horas gratuitas por mês
- ✅ Setup simples

### Limitação:
- ⚠️ Hiberna após 15 minutos de inatividade (plano gratuito)
- Solução: Usar UptimeRobot para manter ativo

### Passo 1: Criar Repositório no GitHub

(Mesmo processo do Railway - veja acima)

### Passo 2: Criar Conta no Render

1. **Acesse**: https://render.com

2. **Clique em "Get Started"**

3. **Login com GitHub**

### Passo 3: Criar Web Service

1. **No Render Dashboard**, clique em **"New +"**

2. **Selecione "Web Service"**

3. **Conecte seu repositório GitHub** `prenotami-bot`

4. **Configure**:
   - **Name**: `prenotami-bot`
   - **Environment**: `Docker`
   - **Region**: Escolha o mais próximo
   - **Branch**: `main`
   - **Plan**: `Free`

5. **Clique em "Create Web Service"**

### Passo 4: Configurar Variáveis de Ambiente

1. **No Render**, vá em **"Environment"**

2. **Adicione as variáveis** (mesmas do Railway):

```
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha
DISCORD_BOT_TOKEN=seu_token
DISCORD_USER_ID=seu_id
CHECK_INTERVAL_MINUTES=30
HEADLESS_MODE=true
```

3. **Clique em "Save Changes"**

### Passo 5: Aguardar Deploy

- Primeira vez pode levar **5-10 minutos**
- Acompanhe em **"Logs"**

### Passo 6: Manter o Bot Ativo (IMPORTANTE!)

Como o plano gratuito hiberna, use **UptimeRobot**:

1. **Acesse**: https://uptimerobot.com

2. **Criar conta gratuita**

3. **Add New Monitor**:
   - Monitor Type: **HTTP(s)**
   - Friendly Name: `PrenotaMI Bot`
   - URL: `https://seu-app.onrender.com` (copie do Render)
   - Monitoring Interval: **5 minutes**

4. **Create Monitor**

**✅ Pronto!** O bot será "pingado" a cada 5 minutos e não hibernará.

### Passo 7: Testar

(Mesmo processo do Railway)

---

## 🔧 Atualizar o Bot Após Deploy

### Quando você fizer mudanças no código:

```bash
cd prenotami_bot

# Fazer mudanças no código...

# Adicionar mudanças
git add .

# Commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

**Railway/Render farão deploy automático!**

---

## 📊 Monitorar o Bot

### Ver Logs

**Railway:**
1. Dashboard → Seu projeto
2. Clique em "Deployments"
3. Clique no deployment ativo
4. Veja logs em tempo real

**Render:**
1. Dashboard → Seu serviço
2. Clique em "Logs"
3. Logs aparecem em tempo real

### Verificar Status no Discord

```
!info
```

Mostra:
- Status do bot (online/offline)
- Monitoramento (ativo/parado)
- Última verificação

### Reiniciar o Bot

**Railway:**
- Dashboard → Projeto → **"Restart"**

**Render:**
- Dashboard → Serviço → Manual Deploy → **"Clear build cache & deploy"**

---

## 🆘 Solução de Problemas

### Bot não inicia

**Sintomas:** Logs mostram erro ou bot não responde no Discord

**Verificar:**
1. ✅ Todas as variáveis de ambiente estão configuradas?
2. ✅ `DISCORD_BOT_TOKEN` está correto?
3. ✅ `MESSAGE CONTENT INTENT` está ativado no Discord Developer Portal?

**Solução:**
```bash
# Ver logs completos
# Railway: Deployments → Ver logs
# Render: Logs tab

# Verificar se variáveis estão corretas
# Railway: Variables
# Render: Environment
```

### "Token inválido"

**Causa:** Token Discord incorreto

**Solução:**
1. Acesse: https://discord.com/developers/applications/1441508569110417590
2. Menu **Bot** → **Reset Token**
3. Copie o novo token
4. Atualize variável `DISCORD_BOT_TOKEN` no Railway/Render
5. Reinicie o bot

### "Erro ao fazer login no PrenotaMI"

**Causa:** Credenciais PrenotaMI incorretas

**Solução:**
1. Verifique `PRENOTAMI_EMAIL` e `PRENOTAMI_PASSWORD`
2. Teste login manual no site: https://prenotami.esteri.it
3. Atualize variáveis se necessário
4. Reinicie o bot

### Bot desconecta frequentemente

**Causa:** Plano gratuito hibernando (Render)

**Solução:**
1. Configure UptimeRobot (veja acima)
2. Ou faça upgrade para plano pago ($7/mês)

### Build falha

**Sintomas:** Deploy não completa, erro de build

**Verificar:**
1. ✅ `Dockerfile` está no repositório?
2. ✅ `requirements.txt` está correto?
3. ✅ Todos os arquivos `.py` estão no repositório?

**Solução:**
```bash
# Verificar arquivos
git ls-files

# Deve listar:
# Dockerfile
# requirements.txt
# discord_bot.py
# prenotami_bot.py
# etc.

# Se faltar algum:
git add arquivo_faltando.py
git commit -m "Add missing file"
git push
```

---

## 💰 Custos Estimados

### Railway
- **Gratuito**: $5 crédito/mês
- **Uso do bot**: ~$2-3/mês
- **Sobra**: $2-3/mês para outros projetos
- **Quando acabar crédito**: Upgrade para $5/mês

### Render
- **Gratuito**: 750h/mês (31 dias × 24h = 744h)
- **Suficiente**: Para rodar 24/7
- **Com UptimeRobot**: Permanece gratuito
- **Upgrade**: $7/mês (sem hibernação)

**Recomendação**: Comece com Railway (mais fácil) ou Render (sem cartão).

---

## ✅ Checklist Final

### Antes do Deploy
- [ ] Código no GitHub (repositório criado)
- [ ] `.gitignore` configurado (sem .env)
- [ ] `Dockerfile` no repositório
- [ ] `requirements.txt` atualizado
- [ ] Bot Discord configurado (TOKEN copiado)
- [ ] MESSAGE CONTENT INTENT ativado
- [ ] Credenciais PrenotaMI prontas

### Durante o Deploy
- [ ] Conta criada (Railway ou Render)
- [ ] Repositório conectado
- [ ] Variáveis de ambiente configuradas (6 variáveis)
- [ ] Build completado com sucesso
- [ ] Logs mostram "Bot pronto para receber comandos"

### Após o Deploy
- [ ] Testado `!ajuda` no Discord
- [ ] Testado `!info`
- [ ] Testado `!status`
- [ ] Testado `!verificar`
- [ ] Iniciado monitoramento: `!iniciar`
- [ ] UptimeRobot configurado (se Render)
- [ ] URLs de logs salvos para referência

---

## 🎯 Próximos Passos

1. ✅ **Deploy feito** → Bot rodando 24/7
2. ✅ **Testado no Discord** → Comandos funcionando
3. ✅ **Monitoramento ativo** → `!iniciar`
4. 📅 **Aguardar notificação** → Bot avisará quando houver vaga
5. ⚡ **Agendar rapidamente** → `!agendar` quando receber notificação

---

## 💡 Dicas Finais

### Melhor Horário
Sistema libera vagas às **20:00 (horário da Itália)**.

**Estratégia:**
- Deixe `!iniciar` rodando sempre
- Bot verificará automaticamente
- Você receberá notificação no Discord
- Use `!agendar` imediatamente

### Intervalo de Verificação

Para aumentar chances próximo às 20:00, edite variável:

```
CHECK_INTERVAL_MINUTES=10
```

Mas **não use menos de 5 minutos** para não sobrecarregar o sistema.

### Notificações no Celular

1. Instale Discord no celular
2. Ative notificações para DMs
3. Receberá alerta quando bot encontrar vaga
4. Pode usar `!agendar` direto do celular!

---

## 📞 Precisa de Ajuda?

### Documentação
- **DEPLOY.md** - Guia completo detalhado
- **DEPLOY_QUICKSTART.md** - Versão resumida
- **README.md** - Documentação geral
- **DISCORD_SETUP.md** - Configurar Discord

### Logs
- Railway: Dashboard → Deployments → Logs
- Render: Dashboard → Logs

### Suporte dos Serviços
- Railway: https://docs.railway.app
- Render: https://render.com/docs
- Discord: https://discord.com/developers/docs

---

**Parabéns! Seu bot está rodando 24/7 na nuvem!** 🎉☁️

Agora você receberá notificações instantâneas quando houver vagas disponíveis, não importa onde esteja!

**Boa sorte com seu agendamento!** 🍀🇮🇹
