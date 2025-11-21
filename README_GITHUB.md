# 🤖 PrenotaMI Bot - Agendamento Automático de Passaporte

Bot automatizado para monitorar e agendar renovação de passaporte no sistema **PrenotaMI** do Consulado Geral da Itália em Paris.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

---

## ✨ Funcionalidades

- ✅ **Login automático** com sessão persistente
- ✅ **Monitoramento 24/7** de disponibilidade
- ✅ **Agendamento automático** quando houver vaga
- ✅ **Bot Discord** com comandos DM
- ✅ **Notificações instantâneas** no Discord
- ✅ **Interface CLI** para controle local
- ✅ **Deploy fácil** em Railway/Render

---

## 🚀 Deploy Rápido (10 minutos)

### Opção 1: Railway (Recomendado)

1. Clique no botão acima ou acesse: https://railway.app
2. Faça login com GitHub
3. **New Project** → **Deploy from GitHub repo**
4. Selecione este repositório
5. Configure as variáveis de ambiente:

```env
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha
DISCORD_BOT_TOKEN=seu_token_discord
DISCORD_USER_ID=seu_id_discord
CHECK_INTERVAL_MINUTES=30
HEADLESS_MODE=true
```

6. Aguarde o deploy (3-5 minutos)
7. Teste no Discord: `!ajuda`

### Opção 2: Render

1. Acesse: https://render.com
2. **New +** → **Web Service**
3. Conecte este repositório
4. Environment: **Docker**
5. Configure as mesmas variáveis acima
6. Deploy!

📖 **Guia completo**: Veja `DEPLOY.md`

---

## 💬 Comandos Discord

| Comando | Descrição |
|---------|-----------|
| `!ajuda` | Ver todos os comandos |
| `!status` | Ver seus agendamentos |
| `!verificar` | Verificar disponibilidade |
| `!iniciar` | Iniciar monitoramento automático |
| `!parar` | Parar monitoramento |
| `!agendar` | Agendar automaticamente |

---

## 🖥️ Uso Local

### Instalação

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/prenotami-bot.git
cd prenotami-bot

# Instalar dependências
pip install -r requirements.txt

# Configurar
cp .env.example .env
nano .env  # Adicionar credenciais
```

### Executar

**Bot Discord:**
```bash
python3 discord_bot.py
```

**Interface CLI:**
```bash
python3 cli.py status
python3 cli.py check
python3 monitor.py --auto-book
```

---

## 📚 Documentação

- **START_HERE.md** - Comece aqui
- **DEPLOY.md** - Guia completo de deploy
- **DEPLOY_QUICKSTART.md** - Deploy rápido
- **DISCORD_SETUP.md** - Configurar bot Discord
- **EXAMPLES.md** - Exemplos práticos
- **README.md** - Documentação completa

---

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `PRENOTAMI_EMAIL` | Email do PrenotaMI | ✅ |
| `PRENOTAMI_PASSWORD` | Senha do PrenotaMI | ✅ |
| `DISCORD_BOT_TOKEN` | Token do bot Discord | ✅ |
| `DISCORD_USER_ID` | ID do usuário autorizado | ❌ |
| `CHECK_INTERVAL_MINUTES` | Intervalo de verificação | ❌ (padrão: 30) |
| `HEADLESS_MODE` | Modo sem interface gráfica | ❌ (padrão: true) |

### Criar Bot Discord

1. Acesse: https://discord.com/developers/applications
2. **New Application** → Nome: "PrenotaMI Bot"
3. Menu **Bot** → **Add Bot**
4. Ativar **MESSAGE CONTENT INTENT**
5. Copiar **TOKEN**
6. Adicionar bot via URL (veja `INVITE_URLS.txt`)

---

## 🎯 Como Funciona

1. Bot faz login no sistema PrenotaMI
2. Monitora disponibilidade a cada X minutos
3. Quando encontra vaga, envia notificação no Discord
4. Pode agendar automaticamente com comando `!agendar`
5. Mantém você informado via Discord 24/7

---

## 💡 Dicas

### Melhor Horário

O sistema PrenotaMI libera vagas **diariamente às 20:00** (horário da Itália).

**Recomendação**: Inicie monitoramento às 19:45

```
!iniciar
```

### Intervalo de Verificação

Para aumentar chances próximo às 20:00:

```env
CHECK_INTERVAL_MINUTES=5
```

⚠️ Não use intervalos muito curtos fora do horário de liberação.

---

## 🔒 Segurança

- ✅ Credenciais armazenadas como variáveis de ambiente
- ✅ Cookies salvos localmente (não compartilhados)
- ✅ Token Discord privado
- ✅ Código aberto para auditoria
- ✅ Sem coleta de dados

---

## 🛠️ Tecnologias

- **Python 3.11**
- **Selenium** - Automação do navegador
- **Discord.py** - Bot Discord
- **Docker** - Containerização
- **Railway/Render** - Hospedagem

---

## 📊 Status

- ✅ **Funcional**: 100%
- ✅ **Documentado**: Completo
- ✅ **Testado**: Sim
- ✅ **Deploy**: Pronto

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:

- Reportar bugs
- Sugerir melhorias
- Enviar pull requests
- Melhorar documentação

---

## ⚖️ Aviso Legal

Este bot é uma ferramenta de automação pessoal e **não é afiliado** ao Ministério das Relações Exteriores da Itália ou ao Consulado Geral da Itália em Paris.

Use de forma responsável e ética. Não sobrecarregue o sistema com verificações excessivas.

---

## 📄 Licença

Este projeto é disponibilizado como código aberto para uso pessoal e educacional.

---

## 📞 Suporte

- 📖 Documentação completa: Veja arquivos `.md` no repositório
- 🐛 Reportar bug: Abra uma issue
- 💬 Dúvidas: Consulte `EXAMPLES.md` e `DEPLOY.md`

---

**Desenvolvido para facilitar o processo de agendamento consular** 🇮🇹🇫🇷

⭐ Se este projeto foi útil, considere dar uma estrela!
