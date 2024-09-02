from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from plyer import notification
import getpass
import subprocess
import sys
from utils import clear_console

# Variável global para armazenar a instância do navegador
browser = None

def check_and_install_packages():
    # Packages que necessitam ser instalados para execução do programa
    packages = ["selenium", "webdriver_manager", "plyer", "getpass"]

    for package in packages:
        try:
            __import__(package)
            print(f"{package} já está instalado.")
        except ImportError:
            print(f"{package} não está instalado. Instalando...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    input("\nPacotes necessarios instalados! \nPressione ENTER para continuar...")

def print_art():
       print("""
       _                               _                    _           _     _ 
      | |                             | |                  | |         | |   | |
   ___| |__   __ _ _ __ ___   __ _  __| | ___  ___     __ _| | ___ _ __| |_  | |
  / __| '_ \ / _` | '_ ` _ \ / _` |/ _` |/ _ \/ __|   / _` | |/ _ \ '__| __| | |
 | (__| | | | (_| | | | | | | (_| | (_| | (_) \__ \  | (_| | |  __/ |  | |_  |_|
  \___|_| |_|\__,_|_| |_| |_|\__,_|\__,_|\___/|___/   \__,_|_|\___|_|   \__| (_)
                                                                                                                                                                                                                                        
    """)

def start_browser():
    global browser  # Utiliza a variável global 'browser'
    
    if browser is None:
        print("O navegador não estava aberto. Iniciando uma nova instância.")
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)
    else:
        try:
            # Tenta acessar a URL atual para verificar se o navegador está ativo
            browser.current_url  
            print("O navegador já está aberto e será utilizado.")
        except WebDriverException:
            # Se o navegador foi fechado ou não está mais ativo, cria uma nova instância
            print("O navegador não está mais aberto. Iniciando uma nova instância.")
            service = Service(ChromeDriverManager().install())
            browser = webdriver.Chrome(service=service)
    
    return browser

def get_credentials():
    print("Insira os dados de acesso ao Colaborador")

    username = input("Login: ")
    password = getpass.getpass("Senha (Nao será mostrada no terminal): ")
    return username, password

def access_colaborador(browser, username, password):
    while True:
        try:
            # Verifica se já estamos logados tentando acessar um elemento que só existe após o login
            browser.get("https://central.equiplano.com.br/colaborador/buscarChamado")
            browser.find_element('xpath', '//*[@id="tableMeusChamados_wrapper"]')
            print("Já estamos logados no sistema.")
            break
        except:
            # Se o elemento não for encontrado, realiza o login
            print("Não está logado, realizando o login...")
            browser.get("https://central.equiplano.com.br/colaborador/buscarChamado")
            browser.find_element('xpath','//*[@id="login"]').send_keys(username)
            browser.find_element('xpath','//*[@id="senha"]').send_keys(password)
            browser.find_element('xpath','/html/body/div/div/div/form/div/div[2]/div[3]/button').click()
            # Verifica se o Login foi feito com sucesso
            try:
                # Verifica se o elemento da página de chamados está presente
                browser.find_element('xpath', '//*[@id="tableMeusChamados_wrapper"]')
                print("Login realizado com sucesso!")
                break
            except NoSuchElementException:
                try:
                    # Verifica se o elemento de login ainda está presente, o que significa que o login falhou
                    browser.find_element('xpath','//*[@id="login"]')
                    print("Login falhou. Por favor, verifique suas credenciais e tente novamente.")
                    username, password = get_credentials()
                except NoSuchElementException:
                    # Se nenhum dos elementos foi encontrado, pode haver um problema na página ou no seletor.
                    print("Erro ao verificar o login. Por favor, verifique a página.")
                    username, password = get_credentials()

def get_search_interval():
    while True:
        user_input = input("Informe (em minutos) o intervalo entre buscas ou ENTER para padrão (5 minutos): ")
        
        if user_input == "":
            # Se o usuário pressionar ENTER, use o valor padrão
            search_interval_min = 5
            break
        
        try:
            # Tenta converter a entrada para um inteiro
            search_interval_min = int(user_input)
            if search_interval_min <= 0:
                print("Por favor, insira um número inteiro positivo.")
            else:
                break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro.")

    search_interval_sec = search_interval_min * 60
    return search_interval_min, search_interval_sec

def search_tickets(browser, systems_to_search):
    print("Realizando busca...")
    
    # Filtrando chamados do Suporte
    Select(browser.find_element('xpath', '//*[@id="page-wrapper"]/div[2]/div[1]/form/div/div[2]/div[2]/select')).select_by_value('3053')
    browser.find_element('xpath', '//*[@id="page-wrapper"]/div[2]/div[1]/form/div/div[1]/button').click()

    # Iniciando lista para valores encontrados
    found_contents = []

    # Contabilizando número de linhas na tabela
    rows = browser.find_elements('xpath', '//*[@id="tableMeusChamados"]/tbody/tr')

    for row in rows:
        td_text = row.find_element('xpath', './td[3]').text
        
        for system in systems_to_search:
            if system in td_text:
                ticket_number = row.find_element('xpath', './td[2]/a').text
                found_contents.append((ticket_number, system))

    return found_contents

def display_results(found_contents):
    if found_contents:
        print("Novos chamados encontrados: ")
        notification_message = ""
        for number, system in found_contents:
            print(f"Número do chamado: {number} - Sistema: {system}")
            notification_message += f"Número do chamado: {number} - Sistema: {system}\n"

        notification.notify(
            title="Novos Chamados Encontrados!",
            message=notification_message.strip(),
            app_name="Sistema de Alerta de Chamados",
            timeout=30
        )
    else:
        print("Nenhum chamado encontrado no momento.")