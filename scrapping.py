from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep

driver = webdriver.Firefox()

url = 'https://web.grew.fr/'

#Requisicao da página
driver.get(url)

#try:

# Esperando que os elementos fiquem disponiveis para scrapping
input_corpus = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'corpus_input'))
)

#Aguardando id da sessão ser alocado
sleep(3)

#Inserção do corpus
input_corpus.send_keys(os.getcwd()+"\Pre_Anotacao_Enhanced.conllu")

#Inserção das regras
input_regras = driver.find_element(By.ID, 'grs_file_input').send_keys(os.getcwd()+"\este2.grs")

#Observando quantas sentencas foram alteradas
changed_sentences = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="nav flex-column"]//li'))
)
num_items = len(changed_sentences)
#print(f"A lista contem {num_items} sentencas.")

strategie_name = 'ud_to_mix'
if num_items == 1:     
    #Aplicação das regras
    strategies_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'strat-'+strategie_name))
    )
    strategies_btn.click()

    sentence_element = driver.find_element(By.XPATH, '//div[@class="col-md-9 ml-sm-auto col-lg-10 px-md-4"]/h3')
    full_text = sentence_element.text
    id_name = full_text.split(':')[1].strip()
    print(f"O nome do ID eh '{id_name}'")
else:
    #for i in range(num_items):
    changed_sentences[0].click()
    
    #Aplicação das regras
    strategies_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'strat-'+strategie_name))
    )
    strategies_btn.click()

    see_rules_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME,'btn.btn-success.btn-lg'))
    )
    see_rules_btn.click()


    ## Nao ta funcionando isso ainda
    applied_rules = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="sidebar-sticky.pt-3"]/h3'))
    )
    applied_rules = applied_rules.text
    print(applied_rules)

    '''
    for i in range(len(applied_rules)-1):
        applied_rules_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='R_"+str(i)+"']"))
        )
        rule = applied_rules_btn.text
        print(rule)
    '''
    



#finally:
# Certifique-se de fechar o navegador após o uso.
#driver.quit()
