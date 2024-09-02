from functions import get_credentials, start_browser, access_colaborador, search_tickets, display_results
import time

def main():
    username, password = get_credentials()
    systems_to_search = ["TRAMITE 5.00", "ALMOX 5.00", "SCF 5.00", "STP 5.00", "SRH 5.00"]
    
    print("Buscando pelos sistemas: ", ' - '.join(systems_to_search))

    try:
        while True:
            browser = start_browser()
            access_colaborador(browser, username, password)

            search_interval_min = 5
            search_interval_sec = 10 #search_interval_min * 60
            found_contents = search_tickets(browser, systems_to_search)
            display_results(found_contents)
            print(f"Aguardando {search_interval_min} minutos para a próxima busca...")
            print(f"Pressione 'Ctrl + C' para finalizar o programa ")
            time.sleep(search_interval_sec)
    except KeyboardInterrupt:
        print("Parando o programa.")
    finally:
        browser.quit()


main()