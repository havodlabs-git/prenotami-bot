# 📝 Informações para Configurar o Bot no Discord Developer Portal

Use estas informações para preencher os campos no Discord Developer Portal.

---

## 🤖 General Information

### **Name**
```
PrenotaMIBot
```

### **Description** (máximo 400 caracteres)
```
Bot automatizado para monitorar e agendar renovação de passaporte no sistema PrenotaMI do Consulado Geral da Itália em Paris. Receba notificações instantâneas quando houver vagas disponíveis e agende via comandos simples no Discord. Funciona em DM para controle pessoal e privado.
```

**Caracteres usados**: 299/400 ✅

### **Tags** (máximo 5)
```
1. utility
2. automation
3. notifications
4. scheduling
5. personal
```

**Alternativas de tags:**
- `productivity`
- `tools`
- `bot`
- `helper`
- `alerts`

---

## 🔐 Bot Configuration

### **Application ID**
```
1441508569110417590
```
✅ Já configurado

### **Public Key**
```
dab60be1ab8d82d963a2ed07461b5895af350e3af9ad2a2417b81f3cf24955a9
```
✅ Já configurado

### **Token**
⚠️ **IMPORTANTE**: Copie o token e adicione ao arquivo `.env`:
```env
DISCORD_BOT_TOKEN=seu_token_aqui
```

---

## ⚙️ Bot Settings

### **Privileged Gateway Intents**

Ative os seguintes intents:

- ✅ **PRESENCE INTENT** (opcional)
- ✅ **SERVER MEMBERS INTENT** (opcional)
- ✅ **MESSAGE CONTENT INTENT** ⚠️ **OBRIGATÓRIO**

**Por que MESSAGE CONTENT INTENT é obrigatório:**
O bot precisa ler o conteúdo das mensagens para processar comandos como `!status`, `!verificar`, etc.

---

## 🔗 OAuth2 Configuration

### **Scopes** (para gerar URL de convite)

Selecione:
- ✅ **bot**
- ✅ **applications.commands** (opcional, para slash commands futuros)

### **Bot Permissions**

Permissões mínimas necessárias:

**Text Permissions:**
- ✅ **Send Messages** (enviar mensagens)
- ✅ **Send Messages in Threads** (opcional)
- ✅ **Embed Links** (enviar embeds formatados)
- ✅ **Attach Files** (opcional, para enviar arquivos)
- ✅ **Read Message History** (ler histórico)
- ✅ **Add Reactions** (opcional)

**Permissão calculada:** `274877975552` (ou use a calculadora do Discord)

### **Generated OAuth2 URL**

Após selecionar scopes e permissões, copie a URL gerada. Exemplo:

```
https://discord.com/api/oauth2/authorize?client_id=1441508569110417590&permissions=274877975552&scope=bot
```

---

## 🌐 URLs (Opcional)

### **Interactions Endpoint URL**
```
(deixe vazio por enquanto)
```
Só necessário se usar Slash Commands via HTTP em vez de Gateway.

### **Linked Roles Verification URL**
```
(deixe vazio)
```
Não aplicável para este bot.

### **Terms of Service URL**
```
(opcional - deixe vazio ou crie uma página)
```

Sugestão se quiser criar:
```
https://github.com/seu-usuario/prenotami-bot/blob/main/TERMS.md
```

### **Privacy Policy URL**
```
(opcional - deixe vazio ou crie uma página)
```

Sugestão se quiser criar:
```
https://github.com/seu-usuario/prenotami-bot/blob/main/PRIVACY.md
```

---

## 🎨 Branding (Opcional)

### **App Icon**

Você pode criar um ícone personalizado ou usar um emoji. Sugestões:

- 🇮🇹 Bandeira da Itália
- 📅 Calendário
- 🤖 Robô
- 🛂 Passaporte

**Tamanho recomendado:** 512x512 pixels, formato PNG

### **Banner** (opcional)
Disponível apenas para bots verificados.

---

## 📊 Install Settings

### **Install Link**

Escolha uma das opções:

**Opção 1: Discord Provided Link** (Recomendado)
- Deixe o Discord gerar o link automaticamente
- Mais fácil de gerenciar

**Opção 2: Custom URL**
- Use a URL OAuth2 gerada anteriormente

### **Default Install Settings**

**Guild Install:**
- ✅ Ativado (permite adicionar a servidores)
- Scopes: `bot`
- Permissions: `274877975552`

**User Install:**
- ✅ Ativado (permite usar em DM)
- Scopes: `bot`
- Permissions: `274877975552`

⚠️ **IMPORTANTE**: Certifique-se de ativar **User Install** para permitir uso em DM!

---

## 🔒 Bot Visibility

### **Public Bot**
```
✅ Ativado
```
Permite que outras pessoas adicionem o bot (se você quiser compartilhar).

**OU**

```
❌ Desativado
```
Apenas você pode adicionar o bot (uso pessoal).

**Recomendação**: Deixe **desativado** se for apenas para uso pessoal.

### **Requires OAuth2 Code Grant**
```
❌ Desativado
```
Não é necessário para este bot.

---

## 🚀 Como Adicionar o Bot

### Método 1: Via URL OAuth2

1. Copie a URL gerada no OAuth2 URL Generator
2. Cole no navegador
3. Selecione onde adicionar:
   - **Servidor**: Escolha um servidor seu
   - **DM**: Selecione "Adicionar ao DM" ou "Usar como aplicativo"

### Método 2: Via Install Link

1. Vá em **Installation** no Developer Portal
2. Copie o **Install Link**
3. Cole no navegador e siga os passos

---

## ✅ Checklist de Configuração

Use este checklist para garantir que tudo está configurado:

- [ ] Nome do bot definido: **PrenotaMIBot**
- [ ] Descrição adicionada (299 caracteres)
- [ ] Tags adicionadas (5 tags)
- [ ] **MESSAGE CONTENT INTENT** ativado ⚠️ **CRÍTICO**
- [ ] Token copiado e salvo no `.env`
- [ ] Permissões configuradas (Send Messages, Embed Links, etc.)
- [ ] URL OAuth2 gerada
- [ ] **User Install** ativado (para DM)
- [ ] Bot adicionado ao servidor ou DM
- [ ] Teste: enviar `!ajuda` no Discord

---

## 🧪 Testar o Bot

Após configurar tudo:

1. **Iniciar o bot localmente:**
   ```bash
   cd prenotami_bot
   python3 discord_bot.py
   ```

2. **No Discord, enviar:**
   ```
   !ajuda
   ```

3. **Resposta esperada:**
   O bot deve responder com um embed mostrando todos os comandos.

4. **Testar outros comandos:**
   ```
   !info
   !status
   !verificar
   ```

---

## 🔧 Solução de Problemas

### Bot não responde aos comandos

**Verificar:**
1. ✅ **MESSAGE CONTENT INTENT** está ativado?
2. ✅ Bot tem permissão para enviar mensagens?
3. ✅ Token está correto no `.env`?
4. ✅ Bot está online (luz verde no Discord)?

### "Missing Permissions"

**Solução:**
1. Remova o bot do servidor/DM
2. Regenere a URL OAuth2 com as permissões corretas
3. Adicione o bot novamente

### Bot desconecta

**Verificar:**
1. Token está correto
2. Internet está estável
3. Use `nohup` ou `screen` para manter rodando

---

## 📱 Usar em DM (Mensagem Direta)

### Passo a Passo:

1. **Adicionar o bot:**
   - Use a URL OAuth2 com **User Install** ativado
   - Ou adicione a um servidor primeiro

2. **Enviar DM:**
   - Clique com botão direito no bot
   - Selecione **"Mensagem"**
   - Envie `!ajuda`

3. **Alternativa:**
   - Crie um servidor privado só seu
   - Adicione o bot ao servidor
   - Use os comandos em qualquer canal

---

## 🎯 Configuração Recomendada para Uso Pessoal

```
✅ MESSAGE CONTENT INTENT: Ativado
✅ Public Bot: Desativado (apenas você)
✅ User Install: Ativado (para DM)
✅ Permissões: Send Messages + Embed Links
✅ Token: Salvo no .env
```

---

## 📞 Suporte

Se tiver problemas:

1. Verifique o **DISCORD_SETUP.md** para guia detalhado
2. Leia o **DISCORD_QUICKSTART.md** para configuração rápida
3. Consulte a seção de solução de problemas no **README.md**

---

**Seu Application ID:** `1441508569110417590`  
**Seu Public Key:** `dab60be1ab8d82d963a2ed07461b5895af350e3af9ad2a2417b81f3cf24955a9`

✅ **Pronto para configurar!**
