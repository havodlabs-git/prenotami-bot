# 🚀 Guia Rápido - Bot PrenotaMI

## Configuração Inicial (5 minutos)

### 1. Configure suas credenciais

```bash
cd prenotami_bot
cp .env.example .env
nano .env
```

Edite o arquivo e adicione seu email e senha do PrenotaMI:

```env
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha_aqui
```

Salve com `Ctrl+O`, `Enter`, e saia com `Ctrl+X`.

### 2. Primeiro login (salvar sessão)

```bash
python3 cli.py login
```

O navegador abrirá automaticamente. Resolva o reCAPTCHA e clique em "AVANTI". O bot salvará os cookies para uso futuro.

## Uso Diário

### Verificar se você tem agendamentos

```bash
python3 cli.py status
```

### Verificar disponibilidade agora

```bash
python3 cli.py check
```

### Monitorar e agendar automaticamente

```bash
python3 monitor.py --auto-book
```

Este comando:
- ✓ Verifica disponibilidade a cada 30 minutos
- ✓ Agenda automaticamente quando encontrar vaga
- ✓ Mostra notificação quando conseguir agendar
- ✓ Para automaticamente após agendar com sucesso

**Para parar**: Pressione `Ctrl+C`

## Dicas Importantes

### 🕐 Melhor horário para conseguir vaga

O sistema libera novos agendamentos **diariamente às 20:00** (horário da Itália).

**Recomendação**: Inicie o monitoramento às 19:45:

```bash
python3 monitor.py --interval 5 --auto-book
```

### 📋 Comandos mais usados

| Comando | O que faz |
|---------|-----------|
| `python3 cli.py status` | Ver seus agendamentos |
| `python3 cli.py check` | Verificar disponibilidade agora |
| `python3 monitor.py --auto-book` | Monitorar e agendar automaticamente |
| `python3 monitor.py --interval 10` | Verificar a cada 10 minutos |

### ⚠️ Problemas comuns

**"Já existe uma prenotação"**
- Você só pode ter 1 agendamento por serviço
- Cancele o anterior no site antes de agendar novamente

**"Cookies expirados"**
- Normal após alguns dias
- Execute `python3 cli.py login` novamente

**"Nenhuma data disponível"**
- Vagas esgotam rápido
- Use o monitoramento contínuo próximo às 20:00

## Exemplo de Uso Completo

```bash
# 1. Configurar (primeira vez)
cp .env.example .env
nano .env  # Adicionar email e senha

# 2. Fazer login inicial
python3 cli.py login

# 3. Verificar status atual
python3 cli.py status

# 4. Iniciar monitoramento automático
python3 monitor.py --interval 5 --auto-book
```

## Precisa de Ajuda?

Leia o **README.md** completo para documentação detalhada:

```bash
cat README.md
```

---

**Boa sorte com seu agendamento!** 🍀
