#!/usr/bin/env python3
"""
Script para gerar URL de convite do bot Discord
"""

import sys

def generate_invite_url(client_id: str, permissions: int = 274877975552):
    """
    Gera URL de convite para o bot Discord
    
    Args:
        client_id: Application ID do bot
        permissions: Permissões em formato numérico
    
    Returns:
        URL de convite
    """
    # URL base
    base_url = "https://discord.com/api/oauth2/authorize"
    
    # Parâmetros
    params = {
        "client_id": client_id,
        "permissions": permissions,
        "scope": "bot"
    }
    
    # Construir URL
    url = f"{base_url}?client_id={params['client_id']}&permissions={params['permissions']}&scope={params['scope']}"
    
    return url


def main():
    """Função principal"""
    print("="*60)
    print("GERADOR DE URL DE CONVITE - BOT DISCORD")
    print("="*60)
    print()
    
    # Application ID padrão (do usuário)
    default_client_id = "1441508569110417590"
    
    # Solicitar Application ID
    print(f"Application ID padrão: {default_client_id}")
    client_id = input("Digite o Application ID (ou Enter para usar o padrão): ").strip()
    
    if not client_id:
        client_id = default_client_id
    
    print()
    print("Permissões disponíveis:")
    print("1. Mínimas (Send Messages + Embed Links) - 274877975552")
    print("2. Completas (Todas as permissões de texto) - 534723950656")
    print("3. Administrador (não recomendado) - 8")
    print()
    
    perm_choice = input("Escolha as permissões (1-3) [padrão: 1]: ").strip()
    
    permissions_map = {
        "1": 274877975552,
        "2": 534723950656,
        "3": 8,
        "": 274877975552
    }
    
    permissions = permissions_map.get(perm_choice, 274877975552)
    
    # Gerar URLs
    print()
    print("="*60)
    print("URLS GERADAS")
    print("="*60)
    print()
    
    # URL para servidor
    server_url = generate_invite_url(client_id, permissions)
    print("📌 URL para adicionar a SERVIDOR:")
    print(server_url)
    print()
    
    # URL para DM (com scope adicional)
    dm_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands&integration_type=1"
    print("💬 URL para adicionar a DM (User Install):")
    print(dm_url)
    print()
    
    print("="*60)
    print("COMO USAR")
    print("="*60)
    print()
    print("1. Copie uma das URLs acima")
    print("2. Cole no navegador")
    print("3. Escolha onde adicionar o bot:")
    print("   - Servidor: Selecione um servidor seu")
    print("   - DM: Selecione 'Adicionar ao DM' ou 'Usar como aplicativo'")
    print()
    print("⚠️ IMPORTANTE: Certifique-se de ativar 'User Install' no")
    print("   Developer Portal para usar em DM!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(0)
