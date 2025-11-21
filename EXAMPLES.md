# 📚 Exemplos de Uso - Bot PrenotaMI

Este documento apresenta exemplos práticos de uso do bot para diferentes cenários.

## Cenário 1: Primeira Configuração

Você acabou de baixar o bot e quer configurá-lo pela primeira vez.

```bash
# 1. Entrar na pasta do bot
cd prenotami_bot

# 2. Verificar se tudo está instalado corretamente
python3 test_bot.py

# 3. Criar arquivo de configuração
cp .env.example .env

# 4. Editar e adicionar suas credenciais
nano .env
# (Adicione seu email e senha, salve com Ctrl+O, saia com Ctrl+X)

# 5. Testar novamente
python3 test_bot.py

# 6. Fazer primeiro login e salvar sessão
python3 cli.py login
# (Resolva o reCAPTCHA no navegador que abrir)
```

**Resultado esperado**: Mensagem "✓ Login realizado com sucesso!" e cookies salvos.

---

## Cenário 2: Verificação Rápida Diária

Você quer apenas verificar se há vagas disponíveis hoje.

```bash
# Verificar disponibilidade agora
python3 cli.py check --service PASSAPORTO
```

**Exemplo de saída quando há vagas:**

```
============================================================
RESULTADO DA VERIFICAÇÃO
============================================================
Serviço: PASSAPORTO
Data: 2025-11-21 15:30:00
Disponível: SIM
Mensagem: Encontradas 8 datas disponíveis

Primeiras datas disponíveis:
  - 2025-12-05
  - 2025-12-08
  - 2025-12-12
  - 2025-12-15
```

**Exemplo de saída quando NÃO há vagas:**

```
============================================================
RESULTADO DA VERIFICAÇÃO
============================================================
Serviço: PASSAPORTO
Data: 2025-11-21 15:30:00
Disponível: NÃO
Mensagem: Nenhuma data disponível no momento
```

---

## Cenário 3: Monitoramento Automático (Recomendado)

Você quer que o bot fique verificando automaticamente e agende quando encontrar vaga.

### Opção A: Monitoramento durante o dia todo

```bash
# Verificar a cada 30 minutos e agendar automaticamente
python3 monitor.py --auto-book
```

**O que acontece:**
- Bot verifica disponibilidade a cada 30 minutos
- Quando encontrar vaga, agenda automaticamente
- Mostra notificação e para após agendar com sucesso
- Você pode parar com Ctrl+C a qualquer momento

### Opção B: Monitoramento intensivo no horário de liberação

```bash
# Verificar a cada 5 minutos próximo às 20:00 (horário da Itália)
python3 monitor.py --interval 5 --auto-book
```

**Melhor estratégia:**
- Iniciar às 19:45 (horário italiano)
- Usar intervalo de 5 minutos
- Sistema libera vagas às 20:00

### Opção C: Monitoramento com limite de tentativas

```bash
# Verificar 20 vezes (a cada 10 minutos = ~3 horas)
python3 monitor.py --interval 10 --auto-book --max-attempts 20
```

**Útil para:**
- Deixar rodando por tempo limitado
- Evitar uso excessivo de recursos

---

## Cenário 4: Verificar Status dos Agendamentos

Você quer ver se já tem algum agendamento ativo.

```bash
python3 cli.py status
```

**Exemplo quando você TEM agendamento:**

```
============================================================
STATUS DOS AGENDAMENTOS
============================================================

✓ Total de agendamentos: 1

1. PASSAPORTO
   Código: PRN123456789
   Data: 2025-12-15 10:30
   Status: Confermato

------------------------------------------------------------
ÚLTIMA VERIFICAÇÃO DE DISPONIBILIDADE
------------------------------------------------------------
Data: 2025-11-21 14:30:00
Serviço: PASSAPORTO
Status: Nenhuma data disponível no momento
```

**Exemplo quando NÃO tem agendamento:**

```
============================================================
STATUS DOS AGENDAMENTOS
============================================================

⚠ Você não possui agendamentos ativos
```

---

## Cenário 5: Agendamento Manual Assistido

Você quer que o bot verifique disponibilidade, mas prefere escolher a data manualmente.

```bash
# Verificar disponibilidade sem agendar automaticamente
python3 cli.py book --service PASSAPORTO --manual
```

**O que acontece:**
1. Bot faz login
2. Verifica disponibilidade
3. Se houver vagas, mostra as datas disponíveis
4. Navegador fica aberto para você escolher manualmente
5. Você seleciona a data e horário desejados

---

## Cenário 6: Renovar Sessão Expirada

Os cookies expiraram e você precisa fazer login novamente.

```bash
# Forçar novo login (ignorar cookies salvos)
python3 cli.py login --force
```

**Quando usar:**
- Mensagem "Cookies expirados"
- Erro de autenticação
- Após muito tempo sem usar o bot

---

## Cenário 7: Agendar para Outra Pessoa (Prenotação Múltipla)

Você quer agendar para você e um acompanhante.

**Importante**: O bot atual suporta apenas prenotação singola. Para prenotação múltipla, você precisará:

1. Usar o bot para verificar disponibilidade:
```bash
python3 cli.py check --service PASSAPORTO
```

2. Quando houver vagas, acessar manualmente o site:
```bash
python3 cli.py login --keep-open
```

3. No navegador que abrir, selecionar "Prenotação Múltipla" e preencher os dados do acompanhante.

---

## Cenário 8: Monitorar Múltiplos Serviços

Você quer monitorar disponibilidade de diferentes serviços.

### Terminal 1: Monitorar Passaporte
```bash
python3 monitor.py --service PASSAPORTO --interval 15 --auto-book
```

### Terminal 2: Monitorar Carta de Identidade
```bash
python3 monitor.py --service "CARTA D'IDENTITA'" --interval 15 --auto-book
```

**Nota**: Abra terminais separados para cada serviço.

---

## Cenário 9: Debugging e Resolução de Problemas

Algo não está funcionando e você quer investigar.

### Verificar instalação completa
```bash
python3 test_bot.py
```

### Testar login com navegador visível
```bash
python3 cli.py login --force --keep-open
```

### Verificar arquivos de status
```bash
# Ver último status de verificação
cat booking_status.json

# Ver se cookies existem
ls -la session_cookies.pkl
```

### Limpar sessão e recomeçar
```bash
# Remover cookies salvos
rm session_cookies.pkl

# Fazer novo login
python3 cli.py login --force
```

---

## Cenário 10: Uso Programático (Integração)

Você quer integrar o bot em outro script Python.

```python
#!/usr/bin/env python3
from prenotami_bot import PrenotaMIBot

# Criar instância do bot
bot = PrenotaMIBot(
    email="seu_email@exemplo.com",
    password="sua_senha",
    headless=False
)

try:
    # Fazer login
    if bot.login():
        print("Login bem-sucedido!")
        
        # Verificar disponibilidade
        result = bot.check_availability("PASSAPORTO")
        
        if result["available"]:
            print(f"Encontradas {len(result['dates'])} datas disponíveis!")
            
            # Tentar agendar
            booking = bot.book_appointment("PASSAPORTO", auto_select=True)
            
            if booking["success"]:
                print(f"Agendado! Código: {booking['booking_code']}")
        
        # Ver agendamentos
        appointments = bot.get_my_appointments()
        for apt in appointments:
            print(f"Agendamento: {apt['service']} em {apt['date']}")
            
finally:
    bot.close()
```

---

## Dicas Avançadas

### 1. Executar em Background (Linux/Mac)

```bash
# Iniciar em background
nohup python3 monitor.py --auto-book > monitor.log 2>&1 &

# Ver o processo
ps aux | grep monitor.py

# Ver o log em tempo real
tail -f monitor.log

# Parar o processo
pkill -f monitor.py
```

### 2. Agendar Execução Diária (Cron)

Adicione ao crontab para executar automaticamente:

```bash
# Editar crontab
crontab -e

# Adicionar linha (executar às 19:45 todos os dias)
45 19 * * * cd /caminho/para/prenotami_bot && python3 monitor.py --interval 5 --auto-book --max-attempts 10 >> /tmp/prenotami.log 2>&1
```

### 3. Notificações por Email

Modifique o `monitor.py` para enviar email quando encontrar vaga:

```python
import smtplib
from email.message import EmailMessage

def send_notification(message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'PrenotaMI: Vaga Disponível!'
    msg['From'] = 'seu_email@gmail.com'
    msg['To'] = 'seu_email@gmail.com'
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('seu_email@gmail.com', 'sua_senha_app')
        smtp.send_message(msg)

# Adicionar após encontrar vaga disponível
if availability["available"]:
    send_notification(f"Vaga encontrada para {service}!")
```

---

## Perguntas Frequentes

### Quanto tempo devo deixar o bot rodando?

**Recomendação**: Execute próximo às 20:00 (horário italiano) quando o sistema libera novas vagas. Use `--max-attempts 20` para limitar a 20 verificações (~10 horas com intervalo de 30 min).

### O bot pode ser detectado como bot pelo site?

O bot usa técnicas para parecer um navegador normal, mas o site usa reCAPTCHA. Por isso, o primeiro login é manual. Após salvar os cookies, o bot funciona normalmente.

### Posso usar em modo headless (sem interface gráfica)?

Sim, mas não é recomendado para o primeiro login (por causa do reCAPTCHA). Após salvar os cookies, você pode editar o código e usar `headless=True`.

### Quantas vezes por dia devo verificar?

O sistema libera vagas às 20:00. Recomendamos:
- **1-2 verificações manuais** por dia: `python3 cli.py check`
- **Monitoramento intensivo**: Apenas próximo às 20:00 com intervalo de 5-10 minutos
- **Evite**: Verificações excessivas (a cada minuto) que podem sobrecarregar o sistema

---

**Precisa de mais ajuda?** Consulte o README.md completo ou o QUICKSTART.md para início rápido.
