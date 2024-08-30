import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from plyer import notification

print("Sistema de alerta de chamados novos!")
print("Insira os dados de acesso ao Colaborador")

# Solicitando Credenciais
login = input("Login: ")
senha = input("Senha: ")

intervalo_busca_min = 5
intervalo_busca_sec = intervalo_busca_min * 60

print(f"O intervalo entre buscas esta definido para {intervalo_busca_min} minutos.")
print("Acessando Colaborador...")

# Lista de sistema para busca
sistema_para_busca = ["TRAMITE 5.00", "ALMOX 5.00", "SCF 5.00", "STP 5.00", "SRH 5.00"]

# Informa os sistemas que estamos procurando
print("Buscando pelos sistemas: ", end=' ')
for sistema in sistema_para_busca:  
    print(f"{sistema}", end=' - ')

print("")

# Iniciando o Chrome
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

def buscar_chamados():

    print("Realizando busca...")
    # Acessando url e logando
    navegador.get("https://central.equiplano.com.br/colaborador/buscarChamado")
    navegador.find_element('xpath','//*[@id="login"]').send_keys(login)
    navegador.find_element('xpath','//*[@id="senha"]').send_keys(senha)
    navegador.find_element('xpath','/html/body/div/div/div/form/div/div[2]/div[3]/button').click()

    # Filtrando chamados do Suporte
    Select(navegador.find_element('xpath','//*[@id="page-wrapper"]/div[2]/div[1]/form/div/div[2]/div[2]/select')).select_by_value('3053')
    navegador.find_element('xpath', '//*[@id="page-wrapper"]/div[2]/div[1]/form/div/div[1]/button').click()

    # Lista para armazenar os pares (número do chamado, sistema encontrado)
    conteudos_encontrados = []

    # Selecionando todos os tr dentro do tbody
    linhas = navegador.find_elements('xpath', '//*[@id="tableMeusChamados"]/tbody/tr')

    # Iterando sobre cada linha (tr)
    for linha in linhas:
        # Buscando o texto no XPath td[3]
        td_texto = linha.find_element('xpath', './td[3]').text
        
        # Verificando se o texto de td[3] contém algum dos sistemas para busca
        for sistema in sistema_para_busca:
            if sistema in td_texto:
                # Se encontrado, armazenar o número do chamado e o sistema encontrado
                numero_chamado = linha.find_element('xpath', './td[2]/a').text
                conteudos_encontrados.append((numero_chamado, sistema))

    # Verificação e exibição de mensagens
    if conteudos_encontrados:
        print("Novos chamados encontrados: ")
        mensagem_notificacao = ""
        for numero, sistema in conteudos_encontrados:
            print(f"Número do chamado: {numero} - Sistema: {sistema}")
            mensagem_notificacao += f"Número do chamado: {numero} - Sistema: {sistema}\n"

        # Exibindo uma única notificação
        notification.notify(
            title="Novos Chamados Encontrados!",
            message=mensagem_notificacao.strip(),  # Remove o último '\n' extra
            app_name="Sistema de Alerta de Chamados",
            timeout=10  # Exibe a notificação por 10 segundos
        )
    else:
        print("Nenhum chamado encontrado no momento.")

# Loop de atualização - erro
try:
    while True:
        buscar_chamados()
        print(f"Aguardando {intervalo_busca_min} minutos para a próxima busca...")
        time.sleep(intervalo_busca_sec)  # Intervalo de atualização
except KeyboardInterrupt:
    print("Parando o script.")
finally:
    navegador.quit()

