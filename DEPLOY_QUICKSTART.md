# ⚡ Deploy Rápido - 10 Minutos

## 🚂 Railway (Recomendado)

### 1. Preparar Código

```bash
cd prenotami_bot

# Criar repositório Git
git init
git add .
git commit -m "Initial commit"

# Criar no GitHub e push
# (siga instruções do GitHub)
```

### 2. Deploy no Railway

1. Acesse: https://railway.app
2. Login com GitHub
3. **New Project** → **Deploy from GitHub repo**
4. Selecione seu repositório
5. Aguarde build (3-5 min)

### 3. Configurar Variáveis

No Railway, vá em **Variables** e adicione:

```env
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha
DISCORD_BOT_TOKEN=seu_token
DISCORD_USER_ID=seu_id
CHECK_INTERVAL_MINUTES=30
HEADLESS_MODE=true
```

### 4. Testar

No Discord:
```
!ajuda
!status
!iniciar
```

---

## 🎨 Render (Sem Cartão)

### 1. Preparar Código

(Mesmo processo do Railway)

### 2. Deploy no Render

1. Acesse: https://render.com
2. Login com GitHub
3. **New +** → **Web Service**
4. Conecte repositório
5. Configure:
   - Environment: **Docker**
   - Plan: **Free**

### 3. Configurar Variáveis

(Mesmas variáveis do Railway)

### 4. Manter Ativo

Use UptimeRobot para fazer ping:
- https://uptimerobot.com
- Adicionar monitor HTTP
- URL do seu app Render
- Intervalo: 5 minutos

---

## ✅ Checklist

- [ ] Código no GitHub
- [ ] Deploy feito (Railway ou Render)
- [ ] Variáveis configuradas
- [ ] Logs mostram "Bot pronto"
- [ ] Testado no Discord: `!ajuda`
- [ ] Monitoramento configurado (se Render)

---

**Pronto! Bot rodando 24/7!** 🚀

Guia completo: `DEPLOY.md`
