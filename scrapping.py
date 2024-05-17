from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
import csv

def cria_csv():
    #Criando arquivo csv para análise futura
    with open('aplicacoes.csv', 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['id_sentenca', 'tipo_pacote', 'pacote', 'regra'])

def get_key(dict, pack):
    for key, value in dict.items():
        if pack in value:
            return key
    return "Sem Classificacao"

#Insercao das regras no csv
def regras_no_csv(num_items, driver, id_name, classificacao_regras):
    with open('aplicacoes.csv', 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        for i in range(num_items):
            applied_rules_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@id='R_"+str(i)+"']"))
            )
            rule = applied_rules_btn.text
            rule = rule.split(' ')[2]
            rule = rule.split('.')
            rule.insert(0, id_name)
            classificacao = get_key(classificacao_regras, rule[1])
            rule.insert(1, classificacao)
            writer.writerow(rule)


def scrapp():
    driver = webdriver.Firefox()

    url = 'https://web.grew.fr/'

    #Requisicao da página
    driver.get(url)

    classificacao_regras = {
        'Acréscimo de preposições e conjunções': ['case_info', 'cc_info'],
        'Propagação de sujeitos de xcomp': ['deep_subj_ud'],
        'Propagação de head compartilhado por elementos coordenados': ['coord_gov'],
        'Propagação de dependentes de elementos coordenados': ['coord_dep_left_pck', 'coord_dep_right_pck'],
        'Anotação do referente dos pronomes relativos': ['rel_pron'],
        'Inclusão do predicado elíptico': ['null_nodes_head', 'null_nodes_dep', 'orphan_default_pck'],
        'Melhorias': ['elvis', 'elvis_orphan']
        }
    
    try:
        # Esperando que os elementos fiquem disponiveis para scrapping
        input_corpus = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'corpus_input'))
        )

        #Aguardando id da sessão ser alocado
        sleep(3)

        #Inserção do corpus
        input_corpus.send_keys(os.getcwd()+"\sentencas_teste.conllu")

        #Inserção das regras
        input_regras = driver.find_element(By.ID, 'grs_file_input').send_keys(os.getcwd()+"\conjunto_regras_oficial.grs")

        #Observando quantas sentencas foram alteradas
        changed_sentences = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="nav flex-column"]//li'))
        )
        num_sentences = len(changed_sentences)
        
        cria_csv()

        strategie_name = 'strat_principal'

        if num_sentences == 1:     
            #Aplicação das regras
            strategies_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'strat-'+strategie_name))
            )
            strategies_btn.click()

            sentence_element = driver.find_element(By.XPATH, '//div[@class="col-md-9 ml-sm-auto col-lg-10 px-md-4"]/h3')
            full_text = sentence_element.text
            id_name = full_text.split(':')[1].strip()

            see_rules_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME,'btn.btn-success.btn-lg'))
                )
            see_rules_btn.click()

            applied_rules = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[starts-with(@id, 'R_')]"))
            )

            num_items = len(applied_rules)

            regras_no_csv(num_items, driver, id_name, classificacao_regras)
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

                sentences_elements = driver.find_elements(By.XPATH, '//div[@class="col-md-9 ml-sm-auto col-lg-10 px-md-4"]/h3')

                sleep(0.5)

                
                full_text = sentences_elements[6].text

                id_name = full_text.split(': ')[1]

                applied_rules = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[starts-with(@id, 'R_')]"))
                )

                num_items = len(applied_rules)

                regras_no_csv(num_items, driver, id_name, classificacao_regras)
                
                sleep(1)

                #Ve a proxima sentenca
                corpus_btn = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-sm btn-secondary' and text()='Corpus']"))
                )
                driver.execute_script("arguments[0].style.display = 'block';", corpus_btn)
                driver.execute_script("arguments[0].click();", corpus_btn)
    finally:
        driver.close()
        print("Codigo finalizado")


if __name__ == '__main__':
    scrapp()