import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from plyer import notification

# Variável global para armazenar a instância do navegador
browser = None

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
    print("Sistema de alerta de chamados novos!")
    print("Insira os dados de acesso ao Colaborador")

    username = input("Login: ")
    password = input("Senha: ")
    return username, password

def access_colaborador(browser, username, password):
    try:
        # Verifica se já estamos logados tentando acessar um elemento que só existe após o login
        browser.get("https://central.equiplano.com.br/colaborador/buscarChamado")
        browser.find_element('xpath', '//*[@id="tableMeusChamados_wrapper"]')
        print("Já estamos logados no sistema.")
    except:
        # Se o elemento não for encontrado, realiza o login
        print("Não está logado, realizando o login...")
        browser.get("https://central.equiplano.com.br/colaborador/buscarChamado")
        browser.find_element('xpath','//*[@id="login"]').send_keys(username)
        browser.find_element('xpath','//*[@id="senha"]').send_keys(password)
        browser.find_element('xpath','/html/body/div/div/div/form/div/div[2]/div[3]/button').click()

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
            timeout=10
        )
    else:
        print("Nenhum chamado encontrado no momento.")