#!/usr/bin/env python3
"""
Bot do Discord para controlar o PrenotaMI Bot
Permite verificar status, disponibilidade e receber notificações via Discord
"""

import os
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from prenotami_bot import PrenotaMIBot


# Carregar variáveis de ambiente
load_dotenv()

# Configurações
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PRENOTAMI_EMAIL = os.getenv("PRENOTAMI_EMAIL")
PRENOTAMI_PASSWORD = os.getenv("PRENOTAMI_PASSWORD")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
AUTHORIZED_USER_ID = os.getenv("DISCORD_USER_ID")  # Opcional: ID do usuário autorizado

# Intents necessários para o bot
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

# Criar bot com prefixo de comando
bot = commands.Bot(command_prefix="!", intents=intents)

# Estado global
monitoring_active = False
monitoring_task = None
prenotami_bot = None
authorized_user = None


def is_authorized(ctx):
    """Verifica se o usuário está autorizado a usar o bot"""
    if AUTHORIZED_USER_ID:
        return str(ctx.author.id) == AUTHORIZED_USER_ID
    return True  # Se não configurado, permite todos


@bot.event
async def on_ready():
    """Evento quando o bot está pronto"""
    print("="*60)
    print("BOT DISCORD PRENOTAMI INICIADO")
    print("="*60)
    print(f"Bot: {bot.user.name} (ID: {bot.user.id})")
    print(f"Servidores: {len(bot.guilds)}")
    print(f"Intervalo de verificação: {CHECK_INTERVAL_MINUTES} minutos")
    print("="*60)
    print("\nBot pronto para receber comandos!")
    print("Use !ajuda para ver os comandos disponíveis\n")


@bot.event
async def on_message(message):
    """Evento quando uma mensagem é recebida"""
    # Ignorar mensagens do próprio bot
    if message.author == bot.user:
        return
    
    # Processar comandos
    await bot.process_commands(message)


@bot.command(name="ajuda", aliases=["h"])
async def ajuda(ctx):
    """Mostra a lista de comandos disponíveis"""
    embed = discord.Embed(
        title="🤖 Bot PrenotaMI - Comandos",
        description="Bot para monitorar e agendar renovação de passaporte",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📊 !status",
        value="Ver seus agendamentos ativos",
        inline=False
    )
    
    embed.add_field(
        name="🔍 !verificar",
        value="Verificar disponibilidade agora",
        inline=False
    )
    
    embed.add_field(
        name="▶️ !iniciar",
        value="Iniciar monitoramento automático",
        inline=False
    )
    
    embed.add_field(
        name="⏸️ !parar",
        value="Parar monitoramento automático",
        inline=False
    )
    
    embed.add_field(
        name="📅 !agendar",
        value="Tentar agendar automaticamente",
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ !info",
        value="Informações sobre o bot",
        inline=False
    )
    
    embed.add_field(
        name="❓ !ajuda",
        value="Mostrar esta mensagem",
        inline=False
    )
    
    embed.set_footer(text="Bot PrenotaMI v1.0")
    
    await ctx.send(embed=embed)


@bot.command(name="info")
async def info(ctx):
    """Mostra informações sobre o bot"""
    if not is_authorized(ctx):
        await ctx.send("❌ Você não está autorizado a usar este bot.")
        return
    
    embed = discord.Embed(
        title="ℹ️ Informações do Bot",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Status",
        value="🟢 Online" if bot.is_ready() else "🔴 Offline",
        inline=True
    )
    
    embed.add_field(
        name="Monitoramento",
        value="✅ Ativo" if monitoring_active else "⏸️ Parado",
        inline=True
    )
    
    embed.add_field(
        name="Intervalo",
        value=f"{CHECK_INTERVAL_MINUTES} minutos",
        inline=True
    )
    
    # Verificar último status
    status_file = Path("booking_status.json")
    if status_file.exists():
        with open(status_file, 'r') as f:
            last_status = json.load(f)
        
        if "timestamp" in last_status:
            timestamp = datetime.fromisoformat(last_status["timestamp"])
            embed.add_field(
                name="Última Verificação",
                value=timestamp.strftime("%d/%m/%Y %H:%M:%S"),
                inline=False
            )
        
        if "message" in last_status:
            embed.add_field(
                name="Último Resultado",
                value=last_status["message"],
                inline=False
            )
    
    embed.set_footer(text="Bot PrenotaMI v1.0 - Consulado da Itália em Paris")
    
    await ctx.send(embed=embed)


@bot.command(name="status")
async def status(ctx):
    """Verifica status dos agendamentos"""
    if not is_authorized(ctx):
        await ctx.send("❌ Você não está autorizado a usar este bot.")
        return
    
    await ctx.send("🔄 Verificando seus agendamentos...")
    
    try:
        # Criar bot PrenotaMI
        # Usar headless mode se configurado
        headless = os.getenv("HEADLESS_MODE", "true").lower() == "true"
        bot_instance = PrenotaMIBot(PRENOTAMI_EMAIL, PRENOTAMI_PASSWORD, headless=headless)
        
        # Fazer login
        if not bot_instance.login():
            await ctx.send("❌ Erro ao fazer login no PrenotaMI. Verifique suas credenciais.")
            bot_instance.close()
            return
        
        # Buscar agendamentos
        appointments = bot_instance.get_my_appointments()
        
        if not appointments:
            embed = discord.Embed(
                title="📋 Status dos Agendamentos",
                description="⚠️ Você não possui agendamentos ativos",
                color=discord.Color.orange()
            )
        else:
            embed = discord.Embed(
                title="📋 Status dos Agendamentos",
                description=f"✅ Total de agendamentos: {len(appointments)}",
                color=discord.Color.green()
            )
            
            for i, apt in enumerate(appointments, 1):
                embed.add_field(
                    name=f"{i}. {apt['service']}",
                    value=f"**Código:** {apt['booking_code']}\n"
                          f"**Data:** {apt['date']}\n"
                          f"**Status:** {apt['status']}",
                    inline=False
                )
        
        embed.set_footer(text=f"Verificado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        await ctx.send(embed=embed)
        
        bot_instance.close()
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao verificar status: {str(e)}")


@bot.command(name="verificar", aliases=["check"])
async def verificar(ctx, servico: str = "PASSAPORTO"):
    """Verifica disponibilidade de agendamentos"""
    if not is_authorized(ctx):
        await ctx.send("❌ Você não está autorizado a usar este bot.")
        return
    
    await ctx.send(f"🔍 Verificando disponibilidade para {servico}...")
    
    try:
        # Criar bot PrenotaMI
        # Usar headless mode se configurado
        headless = os.getenv("HEADLESS_MODE", "true").lower() == "true"
        bot_instance = PrenotaMIBot(PRENOTAMI_EMAIL, PRENOTAMI_PASSWORD, headless=headless)
        
        # Fazer login
        if not bot_instance.login():
            await ctx.send("❌ Erro ao fazer login no PrenotaMI.")
            bot_instance.close()
            return
        
        # Verificar disponibilidade
        result = bot_instance.check_availability(servico)
        
        if result["available"]:
            embed = discord.Embed(
                title="🎉 Vagas Disponíveis!",
                description=result["message"],
                color=discord.Color.green()
            )
            
            if result["dates"]:
                dates_text = "\n".join([f"📅 {date}" for date in result["dates"][:10]])
                embed.add_field(
                    name="Primeiras datas disponíveis:",
                    value=dates_text,
                    inline=False
                )
            
            embed.add_field(
                name="💡 Dica",
                value="Use `!agendar` para tentar agendar automaticamente!",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="⚠️ Sem Vagas",
                description=result["message"],
                color=discord.Color.orange()
            )
            
            embed.add_field(
                name="💡 Dica",
                value="Use `!iniciar` para monitorar automaticamente.\n"
                      "O sistema libera novas vagas às 20:00 (horário da Itália).",
                inline=False
            )
        
        embed.set_footer(text=f"Verificado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        await ctx.send(embed=embed)
        
        bot_instance.close()
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao verificar disponibilidade: {str(e)}")


@bot.command(name="agendar", aliases=["book"])
async def agendar(ctx, servico: str = "PASSAPORTO"):
    """Tenta agendar automaticamente"""
    if not is_authorized(ctx):
        await ctx.send("❌ Você não está autorizado a usar este bot.")
        return
    
    await ctx.send(f"📅 Tentando agendar {servico}...")
    
    try:
        # Criar bot PrenotaMI
        # Usar headless mode se configurado
        headless = os.getenv("HEADLESS_MODE", "true").lower() == "true"
        bot_instance = PrenotaMIBot(PRENOTAMI_EMAIL, PRENOTAMI_PASSWORD, headless=headless)
        
        # Fazer login
        if not bot_instance.login():
            await ctx.send("❌ Erro ao fazer login no PrenotaMI.")
            bot_instance.close()
            return
        
        # Tentar agendar
        result = bot_instance.book_appointment(servico, auto_select=True)
        
        if result["success"]:
            embed = discord.Embed(
                title="✅ Agendamento Realizado!",
                description="Seu agendamento foi confirmado com sucesso!",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="Código de Agendamento",
                value=f"`{result.get('booking_code', 'N/A')}`",
                inline=False
            )
            
            embed.add_field(
                name="📝 Importante",
                value="Verifique seu email para confirmação.\n"
                      "Use `!status` para ver detalhes do agendamento.",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="⚠️ Agendamento Não Realizado",
                description=result["message"],
                color=discord.Color.orange()
            )
        
        embed.set_footer(text=f"Tentativa em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        await ctx.send(embed=embed)
        
        bot_instance.close()
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao agendar: {str(e)}")


@bot.command(name="iniciar", aliases=["start", "monitor"])
async def iniciar(ctx):
    """Inicia o monitoramento automático"""
    global monitoring_active, monitoring_task
    
    if not is_authorized(ctx):
        await ctx.send("❌ Você não está autorizado a usar este bot.")
        return
    
    if monitoring_active:
        await ctx.send("⚠️ Monitoramento já está ativo!")
        return
    
    monitoring_active = True
    
    embed = discord.Embed(
        title="▶️ Monitoramento Iniciado",
        description="O bot agora verificará disponibilidade automaticamente.",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="Intervalo",
        value=f"{CHECK_INTERVAL_MINUTES} minutos",
        inline=True
    )
    
    embed.add_field(
        name="Serviço",
        value="PASSAPORTO",
        inline=True
    )
    
    embed.add_field(
        name="📢 Notificações",
        value="Você receberá uma mensagem quando houver vagas disponíveis!",
        inline=False
    )
    
    await ctx.send(embed=embed)
    
    # Iniciar task de monitoramento
    if not monitor_loop.is_running():
        monitor_loop.start(ctx)


@bot.command(name="parar", aliases=["stop"])
async def parar(ctx):
    """Para o monitoramento automático"""
    global monitoring_active
    
    if not is_authorized(ctx):
        await ctx.send("❌ Você não está autorizado a usar este bot.")
        return
    
    if not monitoring_active:
        await ctx.send("⚠️ Monitoramento já está parado!")
        return
    
    monitoring_active = False
    
    if monitor_loop.is_running():
        monitor_loop.cancel()
    
    embed = discord.Embed(
        title="⏸️ Monitoramento Parado",
        description="O monitoramento automático foi interrompido.",
        color=discord.Color.orange()
    )
    
    embed.add_field(
        name="💡 Dica",
        value="Use `!iniciar` para retomar o monitoramento.",
        inline=False
    )
    
    await ctx.send(embed=embed)


@tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
async def monitor_loop(ctx):
    """Loop de monitoramento automático"""
    if not monitoring_active:
        return
    
    try:
        # Criar bot PrenotaMI
        # Usar headless mode se configurado
        headless = os.getenv("HEADLESS_MODE", "true").lower() == "true"
        bot_instance = PrenotaMIBot(PRENOTAMI_EMAIL, PRENOTAMI_PASSWORD, headless=headless)
        
        # Fazer login
        if not bot_instance.login():
            await ctx.send("⚠️ Erro ao fazer login durante monitoramento.")
            bot_instance.close()
            return
        
        # Verificar disponibilidade
        result = bot_instance.check_availability("PASSAPORTO")
        
        if result["available"]:
            # Notificar usuário
            embed = discord.Embed(
                title="🎉 VAGA DISPONÍVEL ENCONTRADA!",
                description=result["message"],
                color=discord.Color.gold()
            )
            
            if result["dates"]:
                dates_text = "\n".join([f"📅 {date}" for date in result["dates"][:5]])
                embed.add_field(
                    name="Datas disponíveis:",
                    value=dates_text,
                    inline=False
                )
            
            embed.add_field(
                name="⚡ Ação Rápida",
                value="Use `!agendar` AGORA para tentar agendar automaticamente!",
                inline=False
            )
            
            embed.set_footer(text=f"Encontrado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            await ctx.send(embed=embed)
            await ctx.send("@here")  # Notificação sonora
        
        bot_instance.close()
        
    except Exception as e:
        await ctx.send(f"⚠️ Erro durante monitoramento: {str(e)}")


def main():
    """Função principal"""
    if not DISCORD_TOKEN:
        print("❌ Erro: Configure a variável DISCORD_BOT_TOKEN no arquivo .env")
        return
    
    if not PRENOTAMI_EMAIL or not PRENOTAMI_PASSWORD:
        print("❌ Erro: Configure PRENOTAMI_EMAIL e PRENOTAMI_PASSWORD no arquivo .env")
        return
    
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("❌ Erro: Token do Discord inválido")
    except Exception as e:
        print(f"❌ Erro ao iniciar bot: {e}")


if __name__ == "__main__":
    main()
