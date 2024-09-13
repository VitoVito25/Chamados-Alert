from utils import clear_console, print_art
from functions import get_credentials, start_browser, access_colaborador, search_tickets, display_results, config_menu
from datetime import datetime
import time 


def main():

    clear_console()
    print_art()
    username, password = get_credentials()

    search_interval_min, search_interval_sec, systems_to_search = config_menu()
    
    clear_console()
    print_art()
    print("Buscando pelos sistemas: ", ' - '.join(systems_to_search))
    print(f"Pressione 'Ctrl + C' para finalizar o programa a qualquer momento")

    try:
        while True:
            browser = start_browser()
            access_colaborador(browser, username, password)
            found_contents = search_tickets(browser, systems_to_search)
            display_results(found_contents)

            # Obter a hora atual
            hora_atual = datetime.now().strftime("%H:%M:%S")
            print(f"[{hora_atual}] Aguardando {search_interval_min} minutos para a próxima busca...")
            time.sleep(search_interval_sec)

            # Limpa o vetor para sempre aparecer os mesmos dados
            found_contents.clear()
    except KeyboardInterrupt:
        print("Parando o programa.")
    finally:
        browser.quit()

main()