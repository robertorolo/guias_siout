import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import warnings
import os.path

if not sys.warnoptions:
    warnings.simplefilter("ignore") 
        
#definindo planilhas de guis pagas e emitidas
print('Lendo planilhas de guias emitidas e pagas')
if os.path.isfile('leitura_parcial.csv'):
    guias_rela_path = 'leitura_parcial.csv'
    guias_rela = pd.read_csv(guias_rela_path, sep=';',  encoding = 'utf-8', error_bad_lines=False)
else:
    guias_rela_path = 'relatorio.csv'
    guias_rela = pd.read_csv(guias_rela_path, sep=';',  encoding = 'utf-8', error_bad_lines=False)
    guias_rela['Número da guia'] = 'N/D'
    guias_rela['Valor da guia'] = 'N/D'
    guias_rela['Data da emissão'] = 'N/D'
    guias_rela['Status'] = 'N/D'
    guias_rela['CPF/CNPJ'] = 'N/D'

#acessando o siout
print('Acessando o SIOUT pelo Firefox')
driver = webdriver.Firefox(executable_path=r'geckodriver.exe')

driver.get('http://www.siout.rs.gov.br/#/')

username = driver.find_element_by_xpath('//*[@id="login"]')
password = driver.find_element_by_xpath('//*[@id="password"]')

username.send_keys("079.949.786-06")
password.send_keys("Sparta1941")

entrar = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div[2]/div[1]/div/form/div[3]/button')
entrar.click()
time.sleep(5)

#entrando como administrador
adm = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/div[2]/table/tbody/tr[1]/td/a')
adm.click()
time.sleep(5)

#entrando guias emitidas
driver.get('http://www.siout.rs.gov.br/#/arrecadacao/relatorio/guias-emitidas')
time.sleep(20)

#definindo botoes e campos de busca
busca_proc = driver.find_element_by_xpath('//*[@id="numeroCadastro"]')
busca_clasi = driver.find_element_by_xpath('//*[@id="classificacao"]')
pesquisabtn = driver.find_element_by_xpath('//*[@id="wrap"]/section/lm-filtros-pesquisa-guias-emitidas/div[1]/div/div/div[2]/div/div/form/div[10]/div/button[2]')
limparbtn = driver.find_element_by_xpath('/html/body/div/section/lm-filtros-pesquisa-guias-emitidas/div[1]/div/div/div[2]/div/div/form/div[10]/div/button[1]')

#iterando nas listas de guias
for idx, p in enumerate(guias_rela['Nº de cadastro']):
    
    print('---')
    print('Indice: {}'.format(idx))
    classi = guias_rela['Classificação'].iloc[idx]
    tipo = guias_rela['Tipo de Intervenção'].iloc[idx]
    fonte = guias_rela['Fonte captação'].iloc[idx]
    print('Numero do processo: {}'.format(p))
    print('Intervencao: {}'.format(tipo))
    print('Classificacao: {}'.format(classi))
    
    busca_proc.send_keys(p)
    
    if classi == 'Autorização Prévia':
        busca_clasi.send_keys(Keys.DOWN)
    elif classi == 'Outorga':
        busca_clasi.send_keys(Keys.DOWN+Keys.DOWN)
    elif classi == 'Reserva de Disponibilidade Hídrica':
        busca_clasi.send_keys(Keys.DOWN+Keys.DOWN+Keys.DOWN)
    else:
        busca_clasi.send_keys(Keys.DOWN+Keys.DOWN+Keys.DOWN+Keys.DOWN)
    
    time.sleep(2)
    driver.execute_script("arguments[0].click();", pesquisabtn)
    
    time.sleep(10)
    tabela_procs = driver.find_element_by_xpath('/html/body/div/section/lm-filtros-pesquisa-guias-emitidas/div[2]/div/div/div[2]').text.splitlines()[10:-2]
    #print(tabela_procs)
    
    if len(tabela_procs) == 2:
        acoes = driver.find_element_by_xpath('/html/body/div/section/lm-filtros-pesquisa-guias-emitidas/div[2]/div/div/div[2]/div[2]/table/tbody/tr/td[8]/div/button')
        vis_resumo = driver.find_element_by_xpath('/html/body/div/section/lm-filtros-pesquisa-guias-emitidas/div[2]/div/div/div[2]/div[2]/table/tbody/tr/td[8]/div/ul/li[1]/a') 

    else:
        acoes = driver.find_element_by_xpath('/html/body/div/section/lm-filtros-pesquisa-guias-emitidas/div[2]/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[8]/div/button'.format(len(tabela_procs)/2))
        vis_resumo = driver.find_element_by_xpath('/html/body/div/section/lm-filtros-pesquisa-guias-emitidas/div[2]/div/div/div[2]/div[2]/table/tbody/tr[{}]/td[8]/div/ul/li[1]/a'.format(len(tabela_procs)/2)) 

    acoes.click()
    time.sleep(10)

    vis_resumo.click()
    time.sleep(10)
    
    #mudando de aba
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(20)
    
    #buscando infos
    cpf = driver.find_element_by_xpath('//*[@id="wrap"]/section/div[3]/div/div/div/div[2]/div[2]/div/div[2]').text
    guias_rela.loc[idx, 'CPF/CNPJ'] = cpf
    nguia = driver.find_element_by_xpath('//*[@id="wrap"]/section/div[1]/div/div/div[2]/div[1]/div/div[2]').text
    guias_rela.loc[idx, 'Número da guia'] = nguia
    valor = driver.find_element_by_xpath('//*[@id="wrap"]/section/div[1]/div/div/div[2]/div[2]/div/div[2]').text
    valor = float(valor.replace('.','').replace(',','.'))
    guias_rela.loc[idx, 'Valor da guia'] = valor
    data = driver.find_element_by_xpath('//*[@id="wrap"]/section/div[1]/div/div/div[2]/div[3]/div/div[2]').text
    guias_rela.loc[idx, 'Data da emissão'] = data
    status = driver.find_element_by_xpath('//*[@id="wrap"]/section/div[1]/div/div/div[2]/div[4]/div/div[2]').text
    guias_rela.loc[idx, 'Status'] = status
    
    #fechando a nova aba
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    limparbtn.click()
    print('---\n')
    
    #salvando uma parcial
    if idx%5==0 and idx!=0:
        print('Salvando parcial\n')
        guias_rela.iloc[idx:].to_csv('leitura_parcial.csv', sep=';', index=False)
        
        if os.path.isfile('escrita_parcial.csv'):
            p = pd.read_csv('escrita_parcial.csv', sep=';',  encoding = 'utf-8', error_bad_lines=False)

            guias_rela_p = p.append(guias_rela[idx-5:idx])
            guias_rela_p.to_csv('escrita_parcial.csv', sep=';', index=False)
        
        else:
            guias_rela.iloc[:idx].to_csv('escrita_parcial.csv', sep=';', index=False)

#salvando resultado final
if os.path.isfile('escrita_parcial.csv'):
    p = pd.read_csv('escrita_parcial.csv', sep=';',  encoding = 'utf-8', error_bad_lines=False)

    guias_rela = guias_rela.append(p)

colunas = ['Nº de cadastro','Usuário de Água','CPF/CNPJ','Município','Fonte captação','Tipo de Intervenção','Classificação','Status','Número da guia','Data da emissão','Valor da guia']
guias_rela[colunas].to_csv('relatorio_completo.csv', sep=';', index=False)

print('Finalizado!')