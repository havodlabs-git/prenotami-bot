# Bot PrenotaMI - Agendamento Automático de Passaporte

Bot automatizado para monitorar e agendar renovação de passaporte no sistema **PrenotaMI** do Consulado Geral da Itália em Paris.

## 📍 Funcionalidades

O bot oferece as seguintes funcionalidades principais:

- **Login automático** com salvamento de sessão (cookies)
- **Verificação de disponibilidade** de slots para agendamento
- **Monitoramento contínuo** com intervalo configurável
- **Agendamento automático** quando encontrar vaga disponível
- **Consulta de status** dos agendamentos existentes
- **Interface de linha de comando** simples e intuitiva
- **🆕 Bot do Discord** para controle via mensagens diretas (DM)

## 🚀 Instalação

### Pré-requisitos

O sistema requer os seguintes componentes:

- Python 3.11 ou superior
- Google Chrome ou Chromium instalado
- Conta registrada no PrenotaMI (https://prenotami.esteri.it)

### Instalação das Dependências

Execute o seguinte comando para instalar as bibliotecas necessárias:

```bash
sudo pip3 install selenium webdriver-manager python-dotenv schedule
```

### Configuração

Crie um arquivo `.env` na pasta do projeto com suas credenciais:

```bash
cp .env.example .env
nano .env
```

Edite o arquivo `.env` e configure suas credenciais:

```env
PRENOTAMI_EMAIL=seu_email@exemplo.com
PRENOTAMI_PASSWORD=sua_senha_aqui
CHECK_INTERVAL_MINUTES=30
HEADLESS_MODE=false
```

## 📖 Uso

### Interface de Linha de Comando (CLI)

O bot possui uma interface de linha de comando com vários comandos úteis.

#### 1. Verificar Status dos Agendamentos

Este comando mostra todos os seus agendamentos ativos no sistema:

```bash
python3 cli.py status
```

**Exemplo de saída:**

```
============================================================
STATUS DOS AGENDAMENTOS
============================================================

✓ Total de agendamentos: 1

1. PASSAPORTO
   Código: ABC123456
   Data: 2025-12-15 10:30
   Status: Confermato
```

#### 2. Verificar Disponibilidade

Verifica se há slots disponíveis para um serviço específico:

```bash
python3 cli.py check --service PASSAPORTO
```

**Opções disponíveis para `--service`:**
- `PASSAPORTO` (padrão)
- `CARTA D'IDENTITA'`
- `VISTI`

**Exemplo de saída:**

```
============================================================
RESULTADO DA VERIFICAÇÃO
============================================================
Serviço: PASSAPORTO
Data: 2025-11-21 14:30:00
Disponível: SIM
Mensagem: Encontradas 15 datas disponíveis

Primeiras datas disponíveis:
  - 2025-12-01
  - 2025-12-03
  - 2025-12-05
```

#### 3. Agendar Horário

Tenta agendar automaticamente um horário quando houver disponibilidade:

```bash
# Agendamento automático (seleciona primeira data disponível)
python3 cli.py book --service PASSAPORTO

# Apenas verificar sem agendar (agendamento manual)
python3 cli.py book --service PASSAPORTO --manual
```

#### 4. Testar Login

Realiza login no sistema e salva os cookies para uso futuro:

```bash
# Login normal
python3 cli.py login

# Forçar novo login (ignorar cookies salvos)
python3 cli.py login --force

# Manter navegador aberto após login
python3 cli.py login --keep-open
```

### Monitoramento Contínuo

O script `monitor.py` verifica periodicamente a disponibilidade e pode agendar automaticamente quando encontrar vaga.

### 🤖 Bot do Discord (NOVO!)

Agora você pode controlar o bot via Discord e receber notificações em tempo real!

**Vantagens:**
- ✅ Receber notificações instantâneas quando houver vagas
- ✅ Controlar de qualquer lugar (celular, computador)
- ✅ Comandos simples via mensagem
- ✅ Monitoramento 24/7 com notificações

**Guias:**
- **DISCORD_QUICKSTART.md**: Configuração rápida (5 minutos)
- **DISCORD_SETUP.md**: Guia completo e detalhado

**Comandos principais:**
```
!ajuda          # Ver todos os comandos
!status         # Ver seus agendamentos
!verificar      # Verificar disponibilidade agora
!iniciar        # Iniciar monitoramento automático
!agendar        # Agendar quando houver vaga
```

**Iniciar o bot Discord:**
```bash
python3 discord_bot.py
```

#### Monitoramento Básico

Verifica disponibilidade a cada 30 minutos (padrão):

```bash
python3 monitor.py
```

#### Monitoramento com Agendamento Automático

Agenda automaticamente quando encontrar vaga:

```bash
python3 monitor.py --auto-book
```

#### Opções Avançadas

```bash
# Verificar a cada 15 minutos
python3 monitor.py --interval 15

# Máximo de 10 tentativas
python3 monitor.py --max-attempts 10

# Monitorar serviço específico
python3 monitor.py --service "CARTA D'IDENTITA'"

# Combinação de opções
python3 monitor.py --service PASSAPORTO --interval 20 --auto-book --max-attempts 50
```

**Parâmetros disponíveis:**

| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| `--service` | Serviço a monitorar | `PASSAPORTO` |
| `--interval` | Intervalo entre verificações (minutos) | `30` |
| `--auto-book` | Agendar automaticamente quando encontrar vaga | `false` |
| `--max-attempts` | Número máximo de tentativas | Infinito |

**Para interromper o monitoramento**, pressione `Ctrl+C`.

## 🔐 Segurança e Privacidade

O bot implementa várias medidas de segurança:

- **Credenciais locais**: Email e senha são armazenados apenas no arquivo `.env` local
- **Cookies persistentes**: Após o primeiro login, a sessão é salva localmente para evitar logins repetidos
- **Sem compartilhamento**: Nenhuma informação é enviada para servidores externos
- **Código aberto**: Todo o código está disponível para auditoria

### Importante sobre o reCAPTCHA

O sistema PrenotaMI utiliza **reCAPTCHA** para proteção contra bots. Por isso:

1. **No primeiro login**, você precisará resolver o reCAPTCHA manualmente no navegador
2. O bot aguardará você completar o CAPTCHA e clicar em "AVANTI"
3. Após o login bem-sucedido, os **cookies são salvos** automaticamente
4. **Nos próximos usos**, o bot reutilizará os cookies salvos, evitando o CAPTCHA

## 📁 Estrutura de Arquivos

```
prenotami_bot/
├── prenotami_bot.py          # Classe principal do bot
├── cli.py                    # Interface de linha de comando
├── monitor.py                # Script de monitoramento contínuo
├── discord_bot.py            # Bot do Discord (🆕 NOVO!)
├── test_bot.py               # Script de testes
├── .env                      # Configurações (criar a partir do .env.example)
├── .env.example              # Exemplo de configuração
├── README.md                 # Documentação completa
├── QUICKSTART.md             # Guia rápido
├── EXAMPLES.md               # Exemplos práticos
├── DISCORD_SETUP.md          # Guia completo do Discord
├── DISCORD_QUICKSTART.md     # Guia rápido do Discord
├── SUMMARY.md                # Resumo executivo
├── session_cookies.pkl       # Cookies salvos (gerado automaticamente)
└── booking_status.json       # Status das verificações (gerado automaticamente)
```

## 🔧 Solução de Problemas

### Problema: "Erro: Configure as variáveis no arquivo .env"

**Solução**: Certifique-se de criar o arquivo `.env` com suas credenciais:

```bash
cp .env.example .env
nano .env
```

### Problema: "Cookies expirados, realizando login manual"

**Solução**: Isso é normal. Os cookies expiram após algum tempo. Basta resolver o reCAPTCHA novamente e o bot salvará novos cookies.

### Problema: "Timeout ao tentar fazer login"

**Possíveis causas e soluções:**

1. **Internet lenta**: Aumente o timeout no código ou verifique sua conexão
2. **Site fora do ar**: Verifique se https://prenotami.esteri.it está acessível
3. **Credenciais incorretas**: Verifique email e senha no arquivo `.env`

### Problema: "Já existe uma prenotação para este serviço"

**Explicação**: O sistema PrenotaMI permite apenas **uma prenotação ativa por serviço**. Você precisa cancelar a prenotação existente antes de criar uma nova.

**Solução**: Acesse "I miei appuntamenti" no site e cancele a prenotação anterior.

### Problema: Navegador não abre

**Solução**: Verifique se o Chrome/Chromium está instalado:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install chromium-browser

# Verificar instalação
chromium-browser --version
```

## 🎯 Dicas de Uso

### Melhor horário para verificar disponibilidade

Segundo a documentação oficial do PrenotaMI:

> "Poiché ogni 24 ore, dalle ore 20:00 in poi, il sistema apre uma giornata di nuovi appuntamenti..."

**Tradução**: O sistema libera novos agendamentos diariamente a partir das **20:00 (horário local italiano)**.

**Recomendação**: Execute o monitoramento contínuo a partir das 19:45 (horário da Itália) para ter mais chances de conseguir vaga:

```bash
# Iniciar monitoramento às 19:45 com verificação a cada 5 minutos
python3 monitor.py --interval 5 --auto-book
```

### Estratégia de monitoramento

Para maximizar suas chances de conseguir um agendamento:

1. **Execute o monitor diariamente** próximo às 20:00 (horário italiano)
2. Use **intervalo curto** (5-10 minutos) durante o horário de liberação
3. Ative o **agendamento automático** (`--auto-book`) para não perder vagas
4. Mantenha o **navegador visível** (não use modo headless) para resolver CAPTCHAs se necessário

### Verificação rápida

Para uma verificação rápida sem monitoramento contínuo:

```bash
python3 cli.py check --service PASSAPORTO
```

## 📝 Notas Importantes

### Limitações do Sistema PrenotaMI

O sistema oficial possui as seguintes limitações:

- **Uma prenotação por serviço**: Você só pode ter um agendamento ativo por tipo de serviço
- **Prenotação múltipla limitada**: Máximo de 1 acompanhante adicional para PASSAPORTO e CARTA D'IDENTITA'
- **Visti apenas individual**: Serviço de VISTI não permite prenotação múltipla
- **Cancelamento irreversível**: Prenotações canceladas não podem ser restauradas

### Tipos de Prenotação

| Serviço | Prenotação Singola | Prenotação Multipla | Máx. Acompanhantes |
|---------|-------------------|---------------------|-------------------|
| PASSAPORTO | ✓ | ✓ | 1 |
| CARTA D'IDENTITA' | ✓ | ✓ | 1 |
| VISTI | ✓ | ✗ | 0 |

## 🤝 Suporte

Este bot foi desenvolvido como ferramenta auxiliar para facilitar o processo de agendamento. Para questões oficiais sobre o sistema PrenotaMI, entre em contato com:

**Consolato Generale d'Italia a Parigi**
- Website: https://consparigi.esteri.it
- PrenotaMI: https://prenotami.esteri.it

## ⚖️ Aviso Legal

Este bot é uma ferramenta de automação pessoal e **não é afiliado ao Ministério das Relações Exteriores da Itália** ou ao Consulado Geral da Itália em Paris.

O uso deste bot é de **responsabilidade exclusiva do usuário**. Certifique-se de:

- Usar o bot de forma responsável e ética
- Não sobrecarregar o sistema com verificações excessivas
- Respeitar os termos de uso do site PrenotaMI
- Verificar sempre as informações diretamente no site oficial

## 📄 Licença

Este projeto é disponibilizado como código aberto para uso pessoal e educacional.

---

**Desenvolvido para facilitar o processo de agendamento consular** 🇮🇹🇫🇷
