#!/usr/bin/env python3
"""
Interface de linha de comando para o bot PrenotaMI
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from prenotami_bot import PrenotaMIBot


def cmd_status(args):
    """Comando: Verificar status dos agendamentos"""
    load_dotenv()
    
    email = os.getenv("PRENOTAMI_EMAIL")
    password = os.getenv("PRENOTAMI_PASSWORD")
    
    if not email or not password:
        print("✗ Erro: Configure as variáveis no arquivo .env")
        return 1
    
    bot = PrenotaMIBot(email, password, headless=False)
    
    try:
        if bot.login():
            print("\n" + "="*60)
            print("STATUS DOS AGENDAMENTOS")
            print("="*60)
            
            appointments = bot.get_my_appointments()
            
            if not appointments:
                print("\n⚠ Você não possui agendamentos ativos")
            else:
                print(f"\n✓ Total de agendamentos: {len(appointments)}\n")
                
                for i, apt in enumerate(appointments, 1):
                    print(f"{i}. {apt['service']}")
                    print(f"   Código: {apt['booking_code']}")
                    print(f"   Data: {apt['date']}")
                    print(f"   Status: {apt['status']}")
                    print()
            
            # Mostrar último status salvo
            if Path(bot.STATUS_FILE).exists():
                print("-" * 60)
                print("ÚLTIMA VERIFICAÇÃO DE DISPONIBILIDADE")
                print("-" * 60)
                
                with open(bot.STATUS_FILE, 'r') as f:
                    last_status = json.load(f)
                
                if "timestamp" in last_status:
                    timestamp = datetime.fromisoformat(last_status["timestamp"])
                    print(f"Data: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                
                if "service" in last_status:
                    print(f"Serviço: {last_status['service']}")
                
                if "message" in last_status:
                    print(f"Status: {last_status['message']}")
                
                if last_status.get("available") and last_status.get("dates"):
                    print(f"Datas disponíveis: {', '.join(last_status['dates'][:5])}")
                
                print()
            
            return 0
    finally:
        bot.close()


def cmd_check(args):
    """Comando: Verificar disponibilidade"""
    load_dotenv()
    
    email = os.getenv("PRENOTAMI_EMAIL")
    password = os.getenv("PRENOTAMI_PASSWORD")
    
    if not email or not password:
        print("✗ Erro: Configure as variáveis no arquivo .env")
        return 1
    
    bot = PrenotaMIBot(email, password, headless=False)
    
    try:
        if bot.login():
            result = bot.check_availability(args.service)
            
            print("\n" + "="*60)
            print("RESULTADO DA VERIFICAÇÃO")
            print("="*60)
            print(f"Serviço: {result['service']}")
            print(f"Data: {datetime.fromisoformat(result['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Disponível: {'SIM' if result['available'] else 'NÃO'}")
            print(f"Mensagem: {result['message']}")
            
            if result['available'] and result['dates']:
                print(f"\nPrimeiras datas disponíveis:")
                for date in result['dates'][:10]:
                    print(f"  - {date}")
            
            print()
            return 0
    finally:
        bot.close()


def cmd_book(args):
    """Comando: Tentar agendar"""
    load_dotenv()
    
    email = os.getenv("PRENOTAMI_EMAIL")
    password = os.getenv("PRENOTAMI_PASSWORD")
    
    if not email or not password:
        print("✗ Erro: Configure as variáveis no arquivo .env")
        return 1
    
    bot = PrenotaMIBot(email, password, headless=False)
    
    try:
        if bot.login():
            result = bot.book_appointment(args.service, auto_select=not args.manual)
            
            print("\n" + "="*60)
            print("RESULTADO DO AGENDAMENTO")
            print("="*60)
            print(f"Sucesso: {'SIM' if result['success'] else 'NÃO'}")
            print(f"Mensagem: {result['message']}")
            
            if result.get('booking_code'):
                print(f"Código de Agendamento: {result['booking_code']}")
            
            print()
            return 0 if result['success'] else 1
    finally:
        bot.close()


def cmd_login(args):
    """Comando: Testar login"""
    load_dotenv()
    
    email = os.getenv("PRENOTAMI_EMAIL")
    password = os.getenv("PRENOTAMI_PASSWORD")
    
    if not email or not password:
        print("✗ Erro: Configure as variáveis no arquivo .env")
        return 1
    
    bot = PrenotaMIBot(email, password, headless=False)
    
    try:
        success = bot.login(force_manual=args.force)
        
        if success:
            print("\n✓ Login realizado com sucesso!")
            print("Os cookies foram salvos para uso futuro.")
            return 0
        else:
            print("\n✗ Falha no login")
            return 1
    finally:
        if not args.keep_open:
            bot.close()
        else:
            print("\nNavegador mantido aberto. Feche manualmente quando terminar.")


def main():
    """Função principal da CLI"""
    parser = argparse.ArgumentParser(
        description="Bot para agendamento no PrenotaMI - Consulado da Itália em Paris",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  
  # Verificar status dos agendamentos
  python3 cli.py status
  
  # Verificar disponibilidade para passaporte
  python3 cli.py check --service PASSAPORTO
  
  # Tentar agendar automaticamente
  python3 cli.py book --service PASSAPORTO
  
  # Agendar manualmente (apenas verifica disponibilidade)
  python3 cli.py book --service PASSAPORTO --manual
  
  # Testar login
  python3 cli.py login
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    # Comando: status
    parser_status = subparsers.add_parser(
        "status",
        help="Verificar status dos agendamentos existentes"
    )
    parser_status.set_defaults(func=cmd_status)
    
    # Comando: check
    parser_check = subparsers.add_parser(
        "check",
        help="Verificar disponibilidade de agendamentos"
    )
    parser_check.add_argument(
        "--service",
        default="PASSAPORTO",
        choices=["PASSAPORTO", "CARTA D'IDENTITA'", "VISTI"],
        help="Serviço a verificar (padrão: PASSAPORTO)"
    )
    parser_check.set_defaults(func=cmd_check)
    
    # Comando: book
    parser_book = subparsers.add_parser(
        "book",
        help="Tentar agendar um horário"
    )
    parser_book.add_argument(
        "--service",
        default="PASSAPORTO",
        choices=["PASSAPORTO", "CARTA D'IDENTITA'", "VISTI"],
        help="Serviço a agendar (padrão: PASSAPORTO)"
    )
    parser_book.add_argument(
        "--manual",
        action="store_true",
        help="Apenas verificar disponibilidade sem agendar automaticamente"
    )
    parser_book.set_defaults(func=cmd_book)
    
    # Comando: login
    parser_login = subparsers.add_parser(
        "login",
        help="Testar login e salvar cookies"
    )
    parser_login.add_argument(
        "--force",
        action="store_true",
        help="Forçar login manual mesmo se houver cookies salvos"
    )
    parser_login.add_argument(
        "--keep-open",
        action="store_true",
        help="Manter navegador aberto após login"
    )
    parser_login.set_defaults(func=cmd_login)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
