from utils import clear_console, print_art
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from plyer import notification
from datetime import datetime
import base64
import getpass
import json
import os

def add_systems_to_search_and_save():
    systems_list = []

    print("Digite o nome dos sistemas (aperte ENTER sem digitar nada para finalizar):")
    
    while True:
        system_name = input("Informe o nome do sistema: ").strip()
        
        if system_name == "":
            # Se o usuário não digitar nada, definir sistemas padrão e sair do loop
            if not systems_list:
                systems_list = ["TRAMITE 5.00", "ALMOX 5.00", "SCF 5.00", "STP 5.00", "SBI 5.00"]
                print("Nenhum sistema informado. Usando a configuração padrão.")
                input("Pressione ENTER para continuar...")
            break

        # Formatar o nome do sistema (maiúsculo + " 5.00")
        formatted_system = system_name.upper() + " 5.00"
        systems_list.append(formatted_system)

    # Chamar a função para salvar os sistemas no arquivo JSON
    save_systems_to_search(systems_list)
    return systems_list

def save_systems_to_search(systems_list):

    filename="arquivos/systems_to_search.json"

    try:
        # Garantir que a pasta 'arquivos' exista
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Tentativa de salvar o arquivo JSON
        with open(filename, 'w') as file:
            json.dump(systems_list, file, indent=4)
        print(f"Sistemas salvos em {filename}")

    except FileNotFoundError:
        print(f"Erro: O caminho '{filename}' não foi encontrado.")
        input("Pressione ENTER para continuar...")
    
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"Ocorreu um erro ao tentar salvar os sistemas: {e}")
        input("Pressione ENTER para continuar...")

def load_systems_to_search():

    filename="arquivos/systems_to_search.json"
    try:
        with open(filename, 'r') as file:
            systems_list = json.load(file)
        print(f"Sistemas carregados de {filename}")
        return systems_list
    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado. Usando lista padrão.")
        input("Pressione ENTER para continuar...")
        return ["TRAMITE", "ALMOX", "SCF", "STP", "SBI"]
    
def show_log_option():

    while True:
        user_input = input("Digite 1 para ver todo o log do sistema ou ENTER para nao visualizar.")
        
        if user_input == "":
            # Se o usuário pressionar ENTER, nao vai printar os logs do Sistema
            print_log = False
            break
        elif user_input == "1":
            # Se o usuário pressionar ENTER, vai printar os logs do Sistema
            print_log = True
            break
        else:
            print("Opção invalida, por favor insira 1 ou apenas Clique Enter")
    
    return print_log

def print_log_message(print_log, message):

    if(print_log == True):
        print(message)

def config_menu():
    """
        Função para acessar menu de configurações

        :return search_interval_min:
        :return search_interval_sec:
        :return systems_to_search:
    """

    while True:
        try:
            # Menu de escolha do usuário
            choice = input("Digite 1 para entrar nas configurações ou pressione ENTER para continuar com config padrão: ")

            # Se o usuário pressionar ENTER, valores padrão serão usados
            if choice == '':
                #Padrão de intervalo entre buscas 5 minutos
                search_interval_min = 5
                search_interval_sec = 300
                # Lista de sistemas carregada de um arquivo JSON
                systems_to_search = load_systems_to_search()
                # Configuração para nao mostrar o LOG
                print_log = False
                break  # Sai do loop se a configuração padrão for escolhida

            # Caso contrário, validamos se o valor digitado é '1'
            elif choice == '1':
                clear_console()
                print_art()
                search_interval_min, search_interval_sec = get_search_interval()
                systems_to_search = add_systems_to_search_and_save()
                print_log = show_log_option()
                break  # Sai do loop após configurar
            else:
                print("Entrada inválida. Digite '1' para entrar nas configurações ou pressione ENTER para configuração padrão.")
        
        except ValueError:
            print("Erro: Valor inválido, por favor tente novamente.")

    return search_interval_min, search_interval_sec, systems_to_search, print_log
 
# Variável global para armazenar a instância do navegador
browser = None    

def start_browser(print_log):
    """"
        Função para abrir o navegador ou utilizar o ja existente

        :param: Passar configuração do print_log
        :return: Retorna o browser

    """
    global browser  # Utiliza a variável global 'browser'
    
    if browser is None:

        print_log_message(print_log, "[LOG] O navegador não estava aberto. Iniciando uma nova instância.")
        
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)
    else:
        try:
            # Tenta acessar a URL atual para verificar se o navegador está ativo
            browser.current_url  
            print_log_message(print_log, "[LOG] O navegador já está aberto e será utilizado.")
        except WebDriverException:
            print_log_message(print_log, "[LOG] O navegador não está mais aberto. Iniciando uma nova instância.")
            service = Service(ChromeDriverManager().install())
            browser = webdriver.Chrome(service=service)
    
    return browser

def get_credentials():
    print("Insira os dados de acesso ao Colaborador")

    username = input("Login: ")
    password = getpass.getpass("Senha (Nao será mostrada no terminal): ")
    save_login = input("Deseja salvar o login? (S/N): ")
    encoded_password = base64.b64encode(password.encode("utf-8")).decode("utf-8")
    if save_login.upper() == "S":
        with open("arquivos/credentials.json", "w") as file:
            json.dump({"username": username, "password": encoded_password}, file)
            print("Credenciais salvas com sucesso.")
    else:
        print("Credenciais não salvas.")


    return username, password

def access_colaborador(browser, username, password, print_log):
    while True:
        try:
            # Verifica se já estamos logados tentando acessar um elemento que só existe após o login
            browser.get("https://central.equiplano.com.br/colaborador/buscarChamado")
            browser.find_element('xpath', '//*[@id="tableMeusChamados_wrapper"]')
            print_log_message(print_log, "[LOG] Já estamos logados no sistema.")
            break
        except:
            print_log_message(print_log, "[LOG] Não está logado, realizando o login...")

            browser.get("https://central.equiplano.com.br/colaborador/buscarChamado")
            browser.find_element('xpath','//*[@id="login"]').send_keys(username)
            browser.find_element('xpath','//*[@id="senha"]').send_keys(password)
            browser.find_element('xpath','/html/body/div/div/div/form/div/div[2]/div[3]/button').click()
            # Verifica se o Login foi feito com sucesso
            try:
                # Verifica se o elemento da página de chamados está presente
                browser.find_element('xpath', '//*[@id="tableMeusChamados_wrapper"]')
                print_log_message(print_log, "[LOG] Login realizado com sucesso!")
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

def search_tickets(browser, systems_to_search, print_log):
    
    print_log_message(print_log, "[LOG] Realizando busca...")

    try:
        # Filtrando chamados do Suporte
        Select(browser.find_element('xpath', '//*[@id="page-wrapper"]/div[2]/div[1]/form/div/div[2]/div[2]/select')).select_by_value('3053')
        browser.find_element('xpath', '//*[@id="page-wrapper"]/div[2]/div[1]/form/div/div[1]/button').click()

        # Aguardando a tabela carregar após o clique (espera explícita)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tableMeusChamados"]/tbody/tr')))

        # Iniciando lista para valores encontrados
        found_contents = []

        # Contabilizando número de linhas na tabela
        rows = browser.find_elements('xpath', '//*[@id="tableMeusChamados"]/tbody/tr')

        for row in rows:
            try:
                td_text = row.find_element('xpath', './td[3]').text.lower() 
                for system in systems_to_search:
                    if system.lower() in td_text:
                        ticket_number = row.find_element('xpath', './td[2]/a').text
                        found_contents.append((ticket_number, system))
            except Exception as e:
                print(f"Erro ao processar linha: {e}")

        return found_contents

    except Exception as e:
        print(f"Erro durante a busca: {e}")
        return []

def display_results(found_contents):
    hora_atual = datetime.now().strftime("%H:%M:%S")
    if found_contents:       
        print(f"[{hora_atual}] Novos chamados encontrados: ")
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
        print(f"[{hora_atual}] Nenhum chamado encontrado no momento.")