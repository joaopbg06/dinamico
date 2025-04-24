# pip install selenium

# módulo para controlar o navegador web
from selenium import webdriver

# localizador de elementos
from selenium.webdriver.common.by import By

# serviço para configurar o caminho do executável chromedriver
from selenium.webdriver.chrome.service import Service

# classe que permite executar ações de avançar(o mover do mouse, clique/arrasta)
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera de forma explícita até uma condição seja satisfeita(ex: que um elemento apareça)
from selenium.webdriver.support.ui import WebDriverWait

#Condições esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# trabalhar com dataframe
import pandas as pd

#uso de funções relacionada ao tempo
import time 

#uso para tratamento de exceção
from selenium.common.exceptions import TimeoutException


chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path) #navegador controlado pelo Selenium
options = webdriver.ChromeOptions() #configurar as opções do navegador
options.add_argument('--disable-gpu') #evita possíveis erros gráficos
options.add_argument('--window-size=1920,1080') #defini uma resolução fixa
options.add_argument('--headless') # ativa o modo headless (sem abrir o navegador)


driver = webdriver.Chrome(service=service, options=options)


url_base = 'https://www.kabum.com.br/perifericos/-mouse-gamer'
driver.get(url_base)
time.sleep(5) #


dic_produtos = {"nome":[], 'preco':[], 'parcelas':[]}

pagina = 1

while True:
    print(f"\n Coletando dados da página {pagina}...")

    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "productCard"))
        )

        print('Elementos encontrados com sucesso')
    except TimeoutException:
        print('Tempo de expera foi muito e tankei foi nothing')
    
    produtos = driver.find_elements(By.CLASS_NAME, "productCard")
    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()
            parcelas = produto.find_element(By.CLASS_NAME, "priceTextCard ").text.strip()
            print(f"{nome} - {preco} - {parcelas}")

            dic_produtos['nome'].append(nome)
            dic_produtos['preco'].append(preco)
            dic_produtos['parcelas'].append(parcelas)

        except Exception:
            print('Erro ao coletar dados: ', Exception)


    try:
        botao_proximo = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )

        if botao_proximo:
            driver.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(1)


            driver.execute_script("arguments[0].click();", botao_proximo)
            pagina += 1
            print(f"Indo para a página {pagina}")
            time.sleep(5)

        else:
            print('Você chegou na ultima página')
            break

    except Exception as e:
        print('Erro ao tentear avançar para a proxima página', e)
        break

driver.quit()

df = pd.DataFrame(dic_produtos)
df.to_excel('mouses.xlsx', index=False)

print(f"{len(df)} produtos encontrados")

