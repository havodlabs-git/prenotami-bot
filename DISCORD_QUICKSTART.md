# ⚡ Guia Rápido - Bot Discord (5 minutos)

## 1️⃣ Criar Bot no Discord

1. Acesse: https://discord.com/developers/applications
2. Clique em **"New Application"** → Nome: "PrenotaMI Bot"
3. Menu **"Bot"** → **"Add Bot"**
4. Ative **"MESSAGE CONTENT INTENT"**
5. Clique em **"Reset Token"** → **"Copy"** (guarde o token!)

## 2️⃣ Adicionar Bot ao Servidor

1. Menu **"OAuth2"** → **"URL Generator"**
2. Selecione: **bot**
3. Permissões: **Send Messages**, **Read Messages**, **Embed Links**
4. Copie a URL gerada
5. Cole no navegador e adicione a um servidor seu

## 3️⃣ Configurar Localmente

```bash
# Editar .env
nano .env
```

Adicione:
```env
DISCORD_BOT_TOKEN=seu_token_copiado_aqui
```

## 4️⃣ Iniciar Bot

```bash
python3 discord_bot.py
```

## 5️⃣ Usar no Discord

Envie DM para o bot ou use em qualquer canal:

```
!ajuda          # Ver comandos
!status         # Ver agendamentos
!verificar      # Verificar vagas agora
!iniciar        # Monitorar automaticamente
!agendar        # Agendar quando houver vaga
```

## 🎯 Uso Típico

```
!iniciar        # Deixa monitorando
[Bot avisa quando houver vaga]
!agendar        # Agenda automaticamente
```

## 🔧 Manter Rodando em Background

```bash
nohup python3 discord_bot.py > discord_bot.log 2>&1 &
```

---

**Mais detalhes?** Leia o **DISCORD_SETUP.md** completo.
