from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

#Passando credenciais
login = "victor.renaud"
senha = ""

#Iniciando o Chrome
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

#Acessando url e logando
navegador.get("https://central.equiplano.com.br/colaborador/buscarChamado")
navegador.find_element('xpath','//*[@id="login"]').send_keys(login)
navegador.find_element('xpath','//*[@id="senha"]').send_keys(senha)
navegador.find_element('xpath','/html/body/div/div/div/form/div/div[2]/div[3]/button').click()

#Filtrando chamados do Suporte
Select(navegador.find_element('xpath','//*[@id="page-wrapper"]/div[2]/div[1]/form/div/div[2]/div[2]/select')).select_by_value('3053')
navegador.find_element('xpath', '//*[@id="page-wrapper"]/div[2]/div[1]/form/div/div[1]/button').click()

#####

# Lista de termos para busca
termos_para_busca = ["TRAMITE 5.0", "ALMOX 5.0", "SCF 5.0", "SPT 5.0", "SRH 5.0"]

# Lista para armazenar os conteúdos de td[2]
conteudos_encontrados = []

# Iterar por todas as linhas da tabela
linhas = navegador.find_elements('xpath', '//*[@id="tableMeusChamados"]/tbody/tr')
totalLinhas = enumerate(linhas, start=1)

i = 1
for i, linha in totalLinhas:
    # Obter o conteúdo da terceira célula (td[3])
    td3_text = linha.find_element('xpath', f'//*[@id="tableMeusChamados"]/tbody/tr[{i}]/td[3]').text
    
    # Verificar se o texto de td[3] corresponde a algum dos termos buscados
    if td3_text in termos_para_busca:
        linha.find_element('xpath', f'//*[@id="tableMeusChamados"]/tbody/tr[{i}]/td[3]').click
        input("Pause...")


#####

#Deixando o navegador aberto até "Enter"
input("Pressione Enter para fechar o navegador...")
navegador.quit()
