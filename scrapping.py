from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
import csv

driver = webdriver.Firefox()

url = 'https://web.grew.fr/'

#Requisicao da página
driver.get(url)

try:
    # Esperando que os elementos fiquem disponiveis para scrapping
    input_corpus = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'corpus_input'))
    )

    #Aguardando id da sessão ser alocado
    sleep(3)

    #Inserção do corpus
    input_corpus.send_keys(os.getcwd()+"\este_print\corpus_teste.conllu")

    #Inserção das regras
    input_regras = driver.find_element(By.ID, 'grs_file_input').send_keys(os.getcwd()+"\este2.grs")

    #Observando quantas sentencas foram alteradas
    changed_sentences = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="nav flex-column"]//li'))
    )
    num_sentences = len(changed_sentences)
    #print(f"A lista contem {num_sentences} sentencas.")

    #Criando arquivo csv para análise futura
    with open('aplicacoes.csv', 'w', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['pacote', 'regra'])

    strategie_name = 'ud_to_mix'
    if num_sentences == 1:     
        #Aplicação das regras
        strategies_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'strat-'+strategie_name))
        )
        strategies_btn.click()

        #sentence_element = driver.find_element(By.XPATH, '//div[@class="col-md-9 ml-sm-auto col-lg-10 px-md-4"]/h3')
        #full_text = sentence_element.text
        #id_name = full_text.split(':')[1].strip()
        #print(f"O nome do ID eh '{id_name}'")

        see_rules_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'btn.btn-success.btn-lg'))
            )
        see_rules_btn.click()

        applied_rules = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[starts-with(@id, 'R_')]"))
        )

        num_items = len(applied_rules)
        print(num_items)

        with open('aplicacoes.csv', 'a', newline='') as arquivo:
            for i in range(num_items):
                writer = csv.writer(arquivo)
                applied_rules_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@id='R_"+str(i)+"']"))
                )
                rule = applied_rules_btn.text
                rule = rule.split(' ')[2]
                rule = rule.split('.')
                writer.writerow(rule)
        sleep(1)

    else:
        for i in range(num_sentences):
            changed_sentences[i].click()
            
            #Aplicação das regras
            strategies_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'strat-'+strategie_name))
            )
            strategies_btn.click()

            see_rules_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'btn.btn-success.btn-lg'))
            )
            see_rules_btn.click()

            applied_rules = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[starts-with(@id, 'R_')]"))
            )

            num_items = len(applied_rules)
            #print(num_items)

            with open('aplicacoes.csv', 'a', newline='') as arquivo:
                writer = csv.writer(arquivo)
                for i in range(len(applied_rules)):
                    applied_rules_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//a[@id='R_"+str(i)+"']"))
                    )
                    rule = applied_rules_btn.text
                    rule = rule.split(' ')[2]
                    rule = rule.split('.')
                    writer.writerow(rule)
            
            sleep(1)

            #Ve a proxima sentenca
            corpus_btn = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-sm btn-secondary' and text()='Corpus']"))
            )
            driver.execute_script("arguments[0].style.display = 'block';", corpus_btn)
            driver.execute_script("arguments[0].click();", corpus_btn)

finally:
    driver.close()
