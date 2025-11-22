#!/usr/bin/env python3
"""
Bot Discord PrenotaMI - Versão Notificador
Avisa diariamente às 20:00 (horário da Itália) para verificar vagas
"""

import discord
from discord.ext import commands, tasks
import os
from datetime import datetime, time
import pytz
import asyncio

# Configurações
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")  # Opcional

# Timezone da Itália
ITALY_TZ = pytz.timezone('Europe/Rome')

# Criar bot com intents necessários
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Variável global para controlar notificações
notifications_enabled = {}

@bot.event
async def on_ready():
    """Evento quando o bot está pronto"""
    print("=" * 60)
    print("BOT DISCORD PRENOTAMI INICIADO")
    print("=" * 60)
    print(f"Bot: {bot.user.name} (ID: {bot.user.id})")
    print(f"Servidores: {len(bot.guilds)}")
    print("=" * 60)
    print()
    print("Bot pronto para receber comandos!")
    print("Use !ajuda para ver os comandos disponíveis")
    print()
    
    # Iniciar task de verificação de horário
    if not check_time_task.is_running():
        check_time_task.start()

@bot.event
async def on_message(message):
    """Evento quando uma mensagem é recebida"""
    # Ignorar mensagens do próprio bot
    if message.author == bot.user:
        return
    
    # Se DISCORD_USER_ID está configurado, aceitar apenas desse usuário
    if DISCORD_USER_ID and str(message.author.id) != DISCORD_USER_ID:
        return
    
    # Processar comandos
    await bot.process_commands(message)


@bot.command(name="ajuda", aliases=["h"])
async def ajuda(ctx):
    """Mostra a lista de comandos disponíveis"""
    embed = discord.Embed(
        title="🤖 Bot PrenotaMI - Comandos",
        description="Notificador de horário para agendamento de passaporte",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📋 Comandos Básicos",
        value=(
            "`!ajuda` ou `!h` - Mostra esta mensagem\n"
            "`!info` - Informações sobre o bot\n"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔔 Comandos de Notificação",
        value=(
            "`!ativar` - Ativar notificações diárias às 20:00\n"
            "`!desativar` - Desativar notificações\n"
            "`!status` - Ver status das notificações\n"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔗 Link Útil",
        value="[Acessar PrenotaMI](https://prenotami.esteri.it)",
        inline=False
    )
    
    embed.set_footer(text="Bot desenvolvido para facilitar agendamentos consulares 🇮🇹")
    
    await ctx.send(embed=embed)


@bot.command(name="info")
async def info(ctx):
    """Mostra informações sobre o bot"""
    now_italy = datetime.now(ITALY_TZ)
    
    embed = discord.Embed(
        title="ℹ️ Informações do Bot",
        color=discord.Color.green()
    )
    
    embed.add_field(name="🤖 Bot", value=bot.user.name, inline=True)
    embed.add_field(name="🆔 ID", value=bot.user.id, inline=True)
    embed.add_field(name="📡 Status", value="🟢 Online", inline=True)
    
    embed.add_field(
        name="🕐 Horário Atual (Itália)",
        value=now_italy.strftime("%H:%M:%S - %d/%m/%Y"),
        inline=False
    )
    
    embed.add_field(
        name="🔔 Notificações",
        value="Diariamente às 20:00 (horário da Itália)",
        inline=False
    )
    
    embed.add_field(
        name="📝 Como Funciona",
        value=(
            "1. Use `!ativar` para receber notificações\n"
            "2. Todo dia às 20:00 você receberá um lembrete\n"
            "3. Acesse o site e verifique vagas disponíveis\n"
            "4. Agende manualmente se houver vaga"
        ),
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.command(name="ativar")
async def ativar(ctx):
    """Ativa notificações diárias"""
    user_id = ctx.author.id
    notifications_enabled[user_id] = True
    
    embed = discord.Embed(
        title="✅ Notificações Ativadas!",
        description=(
            "Você receberá um lembrete **diariamente às 20:00** (horário da Itália) "
            "para verificar vagas no PrenotaMI.\n\n"
            "🔗 Link: https://prenotami.esteri.it"
        ),
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="💡 Dica",
        value=(
            "O sistema PrenotaMI libera novas vagas diariamente às 20:00. "
            "Esteja pronto para agendar assim que receber a notificação!"
        ),
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.command(name="desativar")
async def desativar(ctx):
    """Desativa notificações diárias"""
    user_id = ctx.author.id
    notifications_enabled[user_id] = False
    
    embed = discord.Embed(
        title="🔕 Notificações Desativadas",
        description="Você não receberá mais lembretes diários.",
        color=discord.Color.orange()
    )
    
    embed.add_field(
        name="ℹ️ Reativar",
        value="Use `!ativar` para voltar a receber notificações.",
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.command(name="status")
async def status(ctx):
    """Mostra o status das notificações"""
    user_id = ctx.author.id
    enabled = notifications_enabled.get(user_id, False)
    
    now_italy = datetime.now(ITALY_TZ)
    next_notification = now_italy.replace(hour=20, minute=0, second=0, microsecond=0)
    
    # Se já passou das 20:00, próxima notificação é amanhã
    if now_italy.hour >= 20:
        from datetime import timedelta
        next_notification += timedelta(days=1)
    
    embed = discord.Embed(
        title="📊 Status das Notificações",
        color=discord.Color.blue() if enabled else discord.Color.grey()
    )
    
    embed.add_field(
        name="🔔 Notificações",
        value="✅ Ativadas" if enabled else "❌ Desativadas",
        inline=True
    )
    
    embed.add_field(
        name="🕐 Horário",
        value="20:00 (Itália)",
        inline=True
    )
    
    if enabled:
        embed.add_field(
            name="⏰ Próxima Notificação",
            value=next_notification.strftime("%d/%m/%Y às %H:%M"),
            inline=False
        )
    
    embed.add_field(
        name="🔗 Link PrenotaMI",
        value="https://prenotami.esteri.it",
        inline=False
    )
    
    await ctx.send(embed=embed)


@tasks.loop(minutes=1)
async def check_time_task():
    """Verifica se é hora de enviar notificações (20:00 horário da Itália)"""
    now_italy = datetime.now(ITALY_TZ)
    
    # Verificar se é 20:00
    if now_italy.hour == 20 and now_italy.minute == 0:
        await send_notifications()


async def send_notifications():
    """Envia notificações para todos os usuários que ativaram"""
    for user_id, enabled in notifications_enabled.items():
        if not enabled:
            continue
        
        try:
            user = await bot.fetch_user(user_id)
            
            embed = discord.Embed(
                title="🔔 Lembrete: Verificar Vagas PrenotaMI!",
                description=(
                    "**São 20:00 (horário da Itália)!**\n\n"
                    "O sistema PrenotaMI acabou de liberar novas vagas para agendamento. "
                    "Acesse agora para verificar disponibilidade!"
                ),
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="🔗 Acessar PrenotaMI",
                value="https://prenotami.esteri.it",
                inline=False
            )
            
            embed.add_field(
                name="📝 Passos",
                value=(
                    "1. Clique no link acima\n"
                    "2. Faça login\n"
                    "3. Selecione o serviço (Passaporte)\n"
                    "4. Verifique datas disponíveis\n"
                    "5. Agende se houver vaga!"
                ),
                inline=False
            )
            
            embed.add_field(
                name="💡 Dica",
                value="Seja rápido! As vagas acabam em poucos minutos.",
                inline=False
            )
            
            embed.set_footer(text="Boa sorte! 🍀🇮🇹")
            
            await user.send(embed=embed)
            print(f"[{datetime.now()}] Notificação enviada para usuário {user_id}")
            
        except Exception as e:
            print(f"[{datetime.now()}] Erro ao enviar notificação para {user_id}: {e}")
        
        # Aguardar 1 segundo entre envios para evitar rate limit
        await asyncio.sleep(1)


@check_time_task.before_loop
async def before_check_time():
    """Aguarda o bot estar pronto antes de iniciar o loop"""
    await bot.wait_until_ready()


# Iniciar o bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("ERRO: DISCORD_BOT_TOKEN não configurado!")
        print("Configure a variável de ambiente DISCORD_BOT_TOKEN")
        exit(1)
    
    bot.run(DISCORD_TOKEN)
