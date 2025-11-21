#!/usr/bin/env python3
"""
Bot para agendamento automático de renovação de passaporte no sistema PrenotaMI
Consulado Geral da Itália em Paris
"""

import os
import json
import time
import pickle
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv


class PrenotaMIBot:
    """Bot para automatizar agendamentos no sistema PrenotaMI"""
    
    BASE_URL = "https://prenotami.esteri.it"
    COOKIES_FILE = "session_cookies.pkl"
    STATUS_FILE = "booking_status.json"
    
    def __init__(self, email: str, password: str, headless: bool = False):
        """
        Inicializa o bot com credenciais
        
        Args:
            email: Email de login no PrenotaMI
            password: Senha de login
            headless: Se True, executa o navegador em modo headless
        """
        self.email = email
        self.password = password
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def _setup_driver(self):
        """Configura o driver do Chrome com as opções necessárias"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Usar o ChromeDriver já instalado no sistema
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        
    def _save_cookies(self):
        """Salva os cookies da sessão para reutilização"""
        with open(self.COOKIES_FILE, 'wb') as f:
            pickle.dump(self.driver.get_cookies(), f)
        print(f"✓ Cookies salvos em {self.COOKIES_FILE}")
        
    def _load_cookies(self) -> bool:
        """
        Carrega cookies salvos anteriormente
        
        Returns:
            True se os cookies foram carregados com sucesso, False caso contrário
        """
        if not Path(self.COOKIES_FILE).exists():
            return False
            
        try:
            self.driver.get(self.BASE_URL)
            with open(self.COOKIES_FILE, 'rb') as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            print("✓ Cookies carregados com sucesso")
            return True
        except Exception as e:
            print(f"✗ Erro ao carregar cookies: {e}")
            return False
            
    def _save_status(self, status_data: Dict):
        """Salva o status atual dos agendamentos"""
        with open(self.STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)
            
    def _load_status(self) -> Dict:
        """Carrega o status salvo dos agendamentos"""
        if not Path(self.STATUS_FILE).exists():
            return {}
        
        with open(self.STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def login(self, force_manual: bool = False) -> bool:
        """
        Realiza login no sistema PrenotaMI
        
        Args:
            force_manual: Se True, força login manual mesmo se houver cookies salvos
            
        Returns:
            True se o login foi bem-sucedido, False caso contrário
        """
        if self.driver is None:
            self._setup_driver()
        
        # Tentar usar cookies salvos primeiro
        if not force_manual and self._load_cookies():
            self.driver.refresh()
            time.sleep(2)
            
            # Verificar se está logado
            if self._is_logged_in():
                print("✓ Login automático bem-sucedido usando cookies salvos")
                return True
            else:
                print("⚠ Cookies expirados, realizando login manual...")
        
        # Login manual
        print("Acessando página de login...")
        self.driver.get(self.BASE_URL)
        
        try:
            # Preencher email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "login-email"))
            )
            email_input.clear()
            email_input.send_keys(self.email)
            
            # Preencher senha
            password_input = self.driver.find_element(By.ID, "login-password")
            password_input.clear()
            password_input.send_keys(self.password)
            
            print("\n" + "="*60)
            print("⚠ ATENÇÃO: reCAPTCHA detectado!")
            print("="*60)
            print("\nPor favor, resolva o reCAPTCHA manualmente no navegador.")
            print("Após resolver, clique no botão 'AVANTI' para fazer login.")
            print("\nAguardando login manual...")
            print("(O bot continuará automaticamente após o login)\n")
            
            # Aguardar até que o login seja completado (URL muda ou elemento da área logada aparece)
            self.wait.until(
                lambda driver: driver.current_url != self.BASE_URL + "/" or 
                self._is_logged_in()
            )
            
            time.sleep(2)
            
            if self._is_logged_in():
                print("\n✓ Login realizado com sucesso!")
                self._save_cookies()
                return True
            else:
                print("\n✗ Falha no login. Verifique suas credenciais.")
                return False
                
        except TimeoutException:
            print("✗ Timeout ao tentar fazer login")
            return False
        except Exception as e:
            print(f"✗ Erro durante o login: {e}")
            return False
    
    def _is_logged_in(self) -> bool:
        """
        Verifica se o usuário está logado
        
        Returns:
            True se está logado, False caso contrário
        """
        try:
            # Verificar se há elementos da área logada
            self.driver.find_element(By.XPATH, "//a[contains(text(), 'Prenota') or contains(text(), 'I miei appuntamenti')]")
            return True
        except NoSuchElementException:
            return False
    
    def check_availability(self, service: str = "PASSAPORTO") -> Dict:
        """
        Verifica disponibilidade de slots para um serviço
        
        Args:
            service: Nome do serviço (PASSAPORTO, CARTA D'IDENTITA', VISTI)
            
        Returns:
            Dicionário com informações sobre disponibilidade
        """
        if not self._is_logged_in():
            print("✗ Não está logado. Execute login() primeiro.")
            return {"available": False, "error": "Not logged in"}
        
        result = {
            "service": service,
            "timestamp": datetime.now().isoformat(),
            "available": False,
            "dates": [],
            "message": ""
        }
        
        try:
            print(f"\nVerificando disponibilidade para {service}...")
            
            # Navegar para a página de agendamento
            self.driver.get(f"{self.BASE_URL}/Services")
            time.sleep(2)
            
            # Procurar o serviço e clicar em "Prenota"
            try:
                service_link = self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//td[contains(text(), '{service}')]/following-sibling::td//a[contains(text(), 'Prenota')]")
                    )
                )
                service_link.click()
                time.sleep(2)
                
                # Verificar se já existe uma prenotação
                if "già effettuata" in self.driver.page_source:
                    result["message"] = "Já existe uma prenotação para este serviço"
                    print(f"⚠ {result['message']}")
                    return result
                
                # Selecionar prenotação singola (se disponível)
                try:
                    single_booking = self.driver.find_element(
                        By.XPATH, "//input[@value='false' and @name='IsMultiple']"
                    )
                    single_booking.click()
                    time.sleep(1)
                except:
                    pass
                
                # Clicar em avançar para ver o calendário
                try:
                    next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'AVANTI')]")
                    next_button.click()
                    time.sleep(3)
                except:
                    pass
                
                # Verificar disponibilidade no calendário
                available_dates = self.driver.find_elements(
                    By.XPATH, "//td[contains(@class, 'available') or contains(@class, 'verde')]"
                )
                
                if available_dates:
                    result["available"] = True
                    result["dates"] = [date.text for date in available_dates[:10]]  # Primeiras 10 datas
                    result["message"] = f"Encontradas {len(available_dates)} datas disponíveis"
                    print(f"✓ {result['message']}")
                    print(f"  Primeiras datas: {', '.join(result['dates'][:5])}")
                else:
                    # Verificar mensagem de indisponibilidade
                    if "non ci sono date disponibili" in self.driver.page_source.lower():
                        result["message"] = "Nenhuma data disponível no momento"
                        print(f"⚠ {result['message']}")
                    else:
                        result["message"] = "Não foi possível verificar disponibilidade"
                        print(f"⚠ {result['message']}")
                
            except TimeoutException:
                result["message"] = f"Serviço {service} não encontrado"
                print(f"✗ {result['message']}")
            
        except Exception as e:
            result["error"] = str(e)
            result["message"] = f"Erro ao verificar disponibilidade: {e}"
            print(f"✗ {result['message']}")
        
        # Salvar status
        self._save_status(result)
        
        return result
    
    def book_appointment(self, service: str = "PASSAPORTO", auto_select: bool = True) -> Dict:
        """
        Tenta agendar um horário automaticamente
        
        Args:
            service: Nome do serviço
            auto_select: Se True, seleciona automaticamente a primeira data disponível
            
        Returns:
            Dicionário com resultado do agendamento
        """
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "message": ""
        }
        
        # Primeiro verificar disponibilidade
        availability = self.check_availability(service)
        
        if not availability["available"]:
            result["message"] = "Nenhuma data disponível para agendamento"
            print(f"⚠ {result['message']}")
            return result
        
        if not auto_select:
            result["message"] = "Datas disponíveis encontradas. Agendamento manual necessário."
            print(f"⚠ {result['message']}")
            print("  Use o navegador para selecionar manualmente a data desejada.")
            return result
        
        try:
            print("\nTentando agendar automaticamente...")
            
            # Selecionar primeira data disponível
            first_available = self.driver.find_element(
                By.XPATH, "//td[contains(@class, 'available') or contains(@class, 'verde')]"
            )
            first_available.click()
            time.sleep(2)
            
            # Selecionar primeira faixa horária disponível
            time_slots = self.driver.find_elements(
                By.XPATH, "//div[contains(@class, 'time-slot')]//button[not(@disabled)]"
            )
            
            if time_slots:
                time_slots[0].click()
                time.sleep(1)
                
                # Confirmar agendamento
                confirm_button = self.driver.find_element(
                    By.XPATH, "//button[contains(text(), 'PRENOTA')]"
                )
                confirm_button.click()
                time.sleep(3)
                
                # Verificar se o agendamento foi bem-sucedido
                if "codice prenotazione" in self.driver.page_source.lower():
                    # Extrair código de prenotação
                    try:
                        booking_code = self.driver.find_element(
                            By.XPATH, "//span[contains(@class, 'booking-code')]"
                        ).text
                        result["booking_code"] = booking_code
                    except:
                        result["booking_code"] = "Não foi possível extrair o código"
                    
                    result["success"] = True
                    result["message"] = f"Agendamento realizado com sucesso! Código: {result.get('booking_code', 'N/A')}"
                    print(f"\n✓ {result['message']}")
                else:
                    result["message"] = "Falha ao confirmar agendamento"
                    print(f"✗ {result['message']}")
            else:
                result["message"] = "Nenhuma faixa horária disponível"
                print(f"⚠ {result['message']}")
                
        except Exception as e:
            result["error"] = str(e)
            result["message"] = f"Erro durante agendamento: {e}"
            print(f"✗ {result['message']}")
        
        self._save_status(result)
        return result
    
    def get_my_appointments(self) -> List[Dict]:
        """
        Obtém lista de agendamentos existentes
        
        Returns:
            Lista de dicionários com informações dos agendamentos
        """
        if not self._is_logged_in():
            print("✗ Não está logado. Execute login() primeiro.")
            return []
        
        appointments = []
        
        try:
            print("\nBuscando agendamentos existentes...")
            
            # Navegar para "I miei appuntamenti"
            self.driver.get(f"{self.BASE_URL}/Home/Bookings")
            time.sleep(2)
            
            # Verificar se há mensagem de "nenhum agendamento"
            if "non hai prenotazioni" in self.driver.page_source.lower():
                print("⚠ Nenhum agendamento encontrado")
                return appointments
            
            # Extrair informações dos agendamentos
            booking_rows = self.driver.find_elements(By.XPATH, "//table//tr[td]")
            
            for row in booking_rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 4:
                        appointment = {
                            "service": cells[0].text,
                            "booking_code": cells[1].text,
                            "date": cells[2].text,
                            "status": cells[3].text
                        }
                        appointments.append(appointment)
                except:
                    continue
            
            if appointments:
                print(f"✓ Encontrados {len(appointments)} agendamento(s)")
                for apt in appointments:
                    print(f"  - {apt['service']}: {apt['date']} (Código: {apt['booking_code']})")
            
        except Exception as e:
            print(f"✗ Erro ao buscar agendamentos: {e}")
        
        return appointments
    
    def close(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            print("\n✓ Navegador fechado")


def main():
    """Função principal para testes"""
    load_dotenv()
    
    email = os.getenv("PRENOTAMI_EMAIL")
    password = os.getenv("PRENOTAMI_PASSWORD")
    
    if not email or not password:
        print("✗ Erro: Configure as variáveis PRENOTAMI_EMAIL e PRENOTAMI_PASSWORD no arquivo .env")
        return
    
    bot = PrenotaMIBot(email, password, headless=False)
    
    try:
        # Login
        if bot.login():
            # Verificar disponibilidade
            bot.check_availability("PASSAPORTO")
            
            # Buscar agendamentos existentes
            bot.get_my_appointments()
    finally:
        bot.close()


if __name__ == "__main__":
    main()
