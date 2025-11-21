#!/usr/bin/env python3
"""
Script de monitoramento contínuo para verificar disponibilidade
e tentar agendar automaticamente quando houver vagas
"""

import os
import sys
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv

from prenotami_bot import PrenotaMIBot


def monitor_and_book(
    email: str,
    password: str,
    service: str = "PASSAPORTO",
    interval_minutes: int = 30,
    auto_book: bool = False,
    max_attempts: int = None
):
    """
    Monitora continuamente a disponibilidade e tenta agendar
    
    Args:
        email: Email de login
        password: Senha de login
        service: Serviço a monitorar
        interval_minutes: Intervalo entre verificações em minutos
        auto_book: Se True, agenda automaticamente quando encontrar vaga
        max_attempts: Número máximo de tentativas (None = infinito)
    """
    bot = PrenotaMIBot(email, password, headless=False)
    attempt = 0
    
    try:
        # Login inicial
        print("="*60)
        print("BOT DE MONITORAMENTO PRENOTAMI")
        print("="*60)
        print(f"Serviço: {service}")
        print(f"Intervalo de verificação: {interval_minutes} minutos")
        print(f"Agendamento automático: {'SIM' if auto_book else 'NÃO'}")
        print("="*60)
        print()
        
        if not bot.login():
            print("\n✗ Falha no login. Encerrando...")
            return
        
        print("\n✓ Bot iniciado com sucesso!")
        print(f"Pressione Ctrl+C para parar o monitoramento\n")
        
        while True:
            attempt += 1
            
            if max_attempts and attempt > max_attempts:
                print(f"\n⚠ Número máximo de tentativas ({max_attempts}) atingido. Encerrando...")
                break
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{timestamp}] Tentativa #{attempt}")
            print("-" * 60)
            
            # Verificar disponibilidade
            availability = bot.check_availability(service)
            
            if availability["available"]:
                print("\n" + "="*60)
                print("🎉 VAGA DISPONÍVEL ENCONTRADA!")
                print("="*60)
                
                if auto_book:
                    print("\nIniciando agendamento automático...")
                    result = bot.book_appointment(service, auto_select=True)
                    
                    if result["success"]:
                        print("\n" + "="*60)
                        print("✓ AGENDAMENTO REALIZADO COM SUCESSO!")
                        print("="*60)
                        print(f"Código: {result.get('booking_code', 'N/A')}")
                        print("\nVerifique seus agendamentos com: python3 cli.py status")
                        break
                    else:
                        print(f"\n⚠ Falha no agendamento automático: {result['message']}")
                        print("Continuando monitoramento...")
                else:
                    print("\nAgendamento automático desativado.")
                    print("Acesse o navegador para agendar manualmente.")
                    print("\nPara habilitar agendamento automático, use: --auto-book")
                    break
            else:
                print(f"Status: {availability['message']}")
            
            # Aguardar próxima verificação
            if max_attempts is None or attempt < max_attempts:
                wait_seconds = interval_minutes * 60
                print(f"\nPróxima verificação em {interval_minutes} minutos...")
                print(f"(às {datetime.fromtimestamp(time.time() + wait_seconds).strftime('%H:%M:%S')})")
                time.sleep(wait_seconds)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Monitoramento interrompido pelo usuário")
    except Exception as e:
        print(f"\n✗ Erro durante monitoramento: {e}")
    finally:
        bot.close()


def main():
    """Função principal"""
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description="Monitora disponibilidade de agendamentos no PrenotaMI"
    )
    parser.add_argument(
        "--service",
        default="PASSAPORTO",
        choices=["PASSAPORTO", "CARTA D'IDENTITA'", "VISTI"],
        help="Serviço a monitorar (padrão: PASSAPORTO)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Intervalo entre verificações em minutos (padrão: 30)"
    )
    parser.add_argument(
        "--auto-book",
        action="store_true",
        help="Agendar automaticamente quando encontrar vaga"
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=None,
        help="Número máximo de tentativas (padrão: infinito)"
    )
    
    args = parser.parse_args()
    
    email = os.getenv("PRENOTAMI_EMAIL")
    password = os.getenv("PRENOTAMI_PASSWORD")
    
    if not email or not password:
        print("✗ Erro: Configure as variáveis PRENOTAMI_EMAIL e PRENOTAMI_PASSWORD no arquivo .env")
        sys.exit(1)
    
    monitor_and_book(
        email=email,
        password=password,
        service=args.service,
        interval_minutes=args.interval,
        auto_book=args.auto_book,
        max_attempts=args.max_attempts
    )


if __name__ == "__main__":
    main()
