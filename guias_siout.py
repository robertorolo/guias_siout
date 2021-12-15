import pandas as pd
from selenium import webdriver
import time
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    
#definindo o valor da UPF
upf = 21.1581
    
#definindo os dicionarios de valores de guias
subterranea = {
'Poço tubular':{
    'Autorização Prévia':5.83*upf,
    'Outorga':14.58*upf,
    'Atestado de cadastro de empresa Perfuradora':0,
    'Atestado de renovação de cadastro de empresa Perfuradora':0,
    'Dispensa de Outorga':0,
    'Ofício de Aprovação do Projeto de Tamponamento':0,
    'Ofício de Aprovação de Tamponamento Realizado em Desacordo':0,
    'Ofício de Tamponamento Realizado sem Autorização':0,
},
'Poço ponteira':{
    'Autorização Prévia':0,
    'Outorga':14.58*upf,
    'Atestado de cadastro de empresa Perfuradora':0,
    'Atestado de renovação de cadastro de empresa Perfuradora':0,
    'Dispensa de Outorga':0,
    'Ofício de Aprovação do Projeto de Tamponamento':0,
    'Ofício de Aprovação de Tamponamento Realizado em Desacordo':0,
    'Ofício de Tamponamento Realizado sem Autorização':0,
},
'Poço escavado':{
    'Autorização Prévia':0,
    'Outorga':0,
    'Atestado de cadastro de empresa Perfuradora':0,
    'Atestado de renovação de cadastro de empresa Perfuradora':0,
    'Dispensa de Outorga':0,
    'Ofício de Aprovação do Projeto de Tamponamento':0,
    'Ofício de Aprovação de Tamponamento Realizado em Desacordo':0,
    'Ofício de Tamponamento Realizado sem Autorização':0,
},
'Poço de pequeno diâmetro':{
    'Autorização Prévia':0,
    'Outorga':14.58*upf,
    'Atestado de cadastro de empresa Perfuradora':0,
    'Atestado de renovação de cadastro de empresa Perfuradora':0,
    'Dispensa de Outorga':0,
    'Ofício de Aprovação do Projeto de Tamponamento':0,
    'Ofício de Aprovação de Tamponamento Realizado em Desacordo':0,
    'Ofício de Tamponamento Realizado sem Autorização':0,
},
'Poço de monitoramento':{
    'Autorização Prévia':0,
    'Outorga':0,
    'Atestado de cadastro de empresa Perfuradora':0,
    'Atestado de renovação de cadastro de empresa Perfuradora':0,
    'Dispensa de Outorga':0,
    'Ofício de Aprovação do Projeto de Tamponamento':0,
    'Ofício de Aprovação de Tamponamento Realizado em Desacordo':0,
    'Ofício de Tamponamento Realizado sem Autorização':0,
},
'Rebaixamento de nível de água subterrânea':{
    'Autorização Prévia':0,
    'Outorga':14.58*upf,
    'Atestado de cadastro de empresa Perfuradora':0,
    'Atestado de renovação de cadastro de empresa Perfuradora':0,
    'Dispensa de Outorga':0,
    'Ofício de Aprovação do Projeto de Tamponamento':0,
    'Ofício de Aprovação de Tamponamento Realizado em Desacordo':0,
    'Ofício de Tamponamento Realizado sem Autorização':0,
},
'Empresa perfuradora':{
    'Autorização Prévia':0,
    'Outorga':0,
    'Atestado de cadastro de empresa Perfuradora':5.83*upf,
    'Atestado de renovação de cadastro de empresa Perfuradora':5.83*upf,
    'Dispensa de Outorga':0,
    'Ofício de Aprovação do Projeto de Tamponamento':0,
    'Ofício de Aprovação de Tamponamento Realizado em Desacordo':0,
    'Ofício de Tamponamento Realizado sem Autorização':0,
}
}

superficial_rdh = {
'Açude':{
'Adução para aproveitamento hidrelétrico':5.83*upf,
'Bombeamento':5.83*upf,
'Canal de derivação por gravidade':5.83*upf,
'Derivação por gravidade':5.83*upf,
'Tubulação por gravidade':5.83*upf,
'Cadastro apenas do açude':5.83*upf,
},
'Barragem de acumulação':{
'Adução para aproveitamento hidrelétrico':5.83*upf,
'Bombeamento':5.83*upf,
'Canal de derivação por gravidade':5.83*upf,
'Derivação por gravidade':5.83*upf,
'Tubulação por gravidade':5.83*upf,
'Cadastro apenas da barragem':5.83*upf,
},
'Barragem de nível':{
'Adução para aproveitamento hidrelétrico':5.83*upf,
'Bombeamento':5.83*upf,
'Canal de derivação por gravidade':5.83*upf,
'Derivação por gravidade':5.83*upf,
'Tubulação por gravidade':5.83*upf,
'Cadastro apenas da barragem':5.83*upf,
},
'Canal':{
'Bombeamento':5.83*upf,
'Canal de derivação por gravidade':5.83*upf,
'Derivação por gravidade':5.83*upf,
'Tubulação por gravidade':5.83*upf,
'Cadastro apenas do canal':5.83*upf,
},
'Sem Captação':{
'Canal de drenagem':5.83*upf,
"Retificação de curso d'água":5.83*upf,
"Canalização do curso d'água":5.83*upf,
'Dique':5.83*upf,
'Eclusa':5.83*upf,
'Obra de proteção do leito de curso dágua':5.83*upf,
"Remoção de material do leito de curso dágua":5.83*upf,
'Travessia/ponte/ancoradouro/porto':5.83*upf,
'Alteração da várzea de inundação':5.83*upf,
"Dessedentação animal direta em curso d'água":5.83*upf,
'Hidrovia':5.83*upf,
},
'Estuário':{
'Bombeamento':5.83*upf,
'Canal de derivação por gravidade':5.83*upf,
'Tubulação por gravidade':5.83*upf,
},
'Lago natural ou lagoa':{
'Canal de derivação por gravidade':5.83*upf,
'Bombeamento':5.83*upf,
'Tubulação por gravidade':5.83*upf,
'Vertedor/Extravasor':5.83*upf,
},
'Nascente':{
'Bombeamento':5.83*upf,
'Canal de derivação por gravidade':5.83*upf,
'Tubulação por gravidade':5.83*upf,
},
"Rio ou curso d'água perene":{
'Canal de derivação por gravidade':5.83*upf,
'Bombeamento':5.83*upf,
'Tubulação por gravidade':5.83*upf,
'Vertedor/Extravasor':5.83*upf,
},
"Rio ou curso d'água intermitente":{
'Canal de derivação por gravidade':5.83*upf,
'Bombeamento':5.83*upf,
'Tubulação por gravidade':5.83*upf,
'Vertedor/Extravasor':5.83*upf,
},
}

superficial_class = {
'Açude':{
'Cadastro apenas do açude':0,
},
'Barragem de acumulação':{
'Cadastro apenas da barragem':61.78,
},
'Barragem de nível':{
'Cadastro apenas da barragem':61.78,
},
}

#definindo lista de usos consuntivos
consuntivos = []

# definindo função para encontrar processos filhos
def achar_filho(lista_de_filhos):
    possiveis = ['Adução para aproveitamento hidrelétrico','Bombeamento','Canal de derivação por gravidade','Derivação por gravidade','Tubulação por gravidade','Cadastro apenas do açude']
    encontrados = []
    for p in possiveis:
        if p in lista_de_filhos:
            encontrados.append(p)
    return encontrados

#definindo planilhas de guis pagas e emitidas
print('Lendo planilhas de guias emitidas e pagas')
guias_emitidas_path = 'guias_emitidas.csv'
guias_pagas_path = 'guias_pagas.csv'

#lendo os arquivos
guias_emitidas = pd.read_csv(guias_emitidas_path, sep=';',  encoding = 'utf-8', error_bad_lines=False)
guias_pagas = pd.read_csv(guias_pagas_path, sep=';',  encoding = 'utf-8', error_bad_lines=False)

#acessando o siout
print('Acessando o SIOUT pelo Firefox')
driver = webdriver.Firefox(executable_path=r'geckodriver.exe')

driver.get('http://www.siout.rs.gov.br/#/')

username = driver.find_element_by_xpath('//*[@id="login"]')
password = driver.find_element_by_xpath('//*[@id="password"]')

username.send_keys("***")
password.send_keys("***")

entrar = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div[2]/div[1]/div/form/div[3]/button')
entrar.click()

time.sleep(5)

#entrando como analista 1
analista1 = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/div[2]/table/tbody/tr[2]/td/a')
analista1.click()

time.sleep(5)

#entrando em cadastros
cadastros = driver.find_element_by_xpath('//*[@id="CadastrodeUsosdagua"]/div[2]/h4')
cadastros.click()

print('Aguardando 100 segundos para que o cadastros de uso de agua carregue')
time.sleep(100)

inconformidade = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/button')
inconformidade.click()

busca_proc = driver.find_element_by_xpath('//*[@id="wrap"]/section/div[1]/div/div/div[2]/div[1]/div/div/input')
pesquisabtn = driver.find_element_by_xpath('//*[@id="wrap"]/section/div[1]/div/div/div[2]/div[1]/div/div/div/span')

#iterando nas listas de guias
lista_guias = [guias_emitidas, guias_pagas]
tipo_lista = ['Emitida', 'Paga']
for idxl, rela in enumerate(lista_guias):
    print('Iterando a lista de guias {}\n'.format(tipo_lista[idxl]))

    guias = []
    sit_guia = []
    cpfcnpj = []
    valor = []

    for idx, p in enumerate(rela[rela.columns[0]]):
        
        sit_guia.append(tipo_lista[idxl])
        classi = rela[rela.columns[-1]].iloc[idx]
        tipo = rela[rela.columns[-2]].iloc[idx]
        fonte = rela[rela.columns[-3]].iloc[idx]
        print('Processo {}'.format(p))
        print('Tipo {}'.format(tipo))
        print('Classificacao {}'.format(classi))
        
        busca_proc.send_keys(p)
        driver.execute_script("arguments[0].click();", pesquisabtn)
        busca_proc.clear()
        time.sleep(10)
        
        acoes = driver.find_element_by_xpath('/html/body/div/section/div[2]/div/div/div[2]/table/tbody/tr/td[9]/div/button')
        acoes.click()
        time.sleep(10)
        acoes_janela = driver.find_element_by_xpath('/html/body/div/section/div[2]/div/div/div[2]/table/tbody/tr/td[9]/div/ul').text.splitlines()
        for idxp, ip in enumerate(acoes_janela):
            if ip == 'Visualizar processo':
                indice = idxp

        vis_proc = driver.find_element_by_xpath('//*[@id="wrap"]/section/div[2]/div/div/div[2]/table/tbody/tr/td[9]/div/ul/li[2]/a[{}]'.format(indice))
        vis_proc.click()
        
        time.sleep(15)
        driver.switch_to.window(driver.window_handles[1])
        
        #lendo cpf ou cpnj
        c = driver.find_element_by_xpath('/html/body/div/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div[2]').text
        print('CPF ou CNPJ: {}'.format(c))
        cpfcnpj.append(c)
        
        ###subterranea
        if fonte == 'Água subterrânea':
            valor_da_guia = 0
        
            if tipo in ['Poço tubular', 'Poço ponteira', 'Poço escavado', 'Poço de pequeno diâmetro']:
            
                quadro_vaz = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[6]/div/div/div/div[2]').text.splitlines()
                
                vmaxd = quadro_vaz[-1]
               
                if vmaxd == 'Não':
                    
                    quadro_vaz = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[7]/div/div/div/div[2]').text.splitlines()
                    
                    
                    tabela_finalidades = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[8]/div/div/div/div[2]').text.splitlines()
                    #print(tabela_finalidades)
                    
                else:
                
                    tabela_finalidades = driver.find_element_by_xpath('/html/body/div/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[7]/div/div/div/div[2]').text.splitlines()
                    #print(tabela_finalidades)
                
                vmaxd = float(quadro_vaz[-1].split()[-2].replace('.','').replace(',','.'))
                print('Vmax: {}'.format(vmaxd))
                
                if vmaxd > 2.:
                    valor_da_guia = subterranea[tipo][classi]
                
            else:
                
                valor_da_guia = subterranea[tipo][classi]
        
        ###superficial
        else:
            valor_da_guia = 0
            
            ##barragens e acudes
            if fonte in ['Açude', 'Barragem de acumulação', 'Barragem de nível']:
               
               dados_da_int = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[4]/div/div/div/div[2]').text.splitlines()

               h = float(dados_da_int[15].split()[-2].replace('.','').replace(',','.'))
               v = float(dados_da_int[9].split()[-2].replace('.','').replace(',','.'))
               print('H: {} - V: {}'.format(h, v))
               
               tabela_finalidades = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[6]/div/div/div/div[2]').text.splitlines()	
               print(tabela_finalidades)
               
               tabela_filhos = []
               if 'Usos de água envolvidos com esta intervenção' in dados_da_int:
                   print('Existe processo filho')
                   tabela_filhos = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[4]/div/div/div/div[2]/div[10]/div[2]').text.splitlines()[7:]
                   #print(tabela_filhos)
                   print(achar_filho(tabela_filhos[0]))
                   
               if (h < 1.5 or v < 15000) and len(tabela_filhos) > 0:
                   pass
                
               else:
                    if classi == 'Reserva de Disponibilidade Hídrica':
                      valor_da_guia = valor_da_guia + superficial_rdh[fonte][tipo]
                      
                      if len(tabela_filhos) > 0:
                        filhos = achar_filho(tabela_filhos[0])
                        for f in filho:
                            valor_da_guia = valor_da_guia + superficial_rdh[fonte][tipo]
                            
                    elif classi == 'Outorga':
                        if tipo in ['Cadastro apenas do açude', 'Cadastro apenas da barragem']:
                            valor_da_guia = valor_da_guia + superficial_class[fonte][tipo]
                            
                    else:
                        pass
            
            ##canais
            elif fonte == 'Canal':
                dados_da_int = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[4]/div/div/div/div[2]').text.splitlines()
                #print(dados_da_int)
                
                tabela_finalidades = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[6]/div/div/div/div[2]').text.splitlines()	
                print(tabela_finalidades)
               
                if 'Usos de água envolvidos com esta intervenção' in dados_da_int:
                   print('Existe processo filho')
                   tabela_filhos = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[4]/div/div/div/div[2]/div[10]/div[2]').text.splitlines()[7:]
                   #print(tabela_filhos)
                   print(achar_filho(tabela_filhos[0]))
                   
                if classi == 'Reserva de Disponibilidade Hídrica':
                    valor_da_guia = valor_da_guia + superficial_rdh[fonte][tipo]
                    
                    if len(tabela_filhos) > 0:
                        filhos = achar_filho(tabela_filhos[0])
                        for f in filho:
                            valor_da_guia = valor_da_guia + superficial_rdh[fonte][tipo]
                      
                    if len(tabela_filhos) > 0:
                        filhos = achar_filho(tabela_filhos[0])
                        for f in filho:
                            valor_da_guia = valor_da_guia + superficial_rdh[fonte][tipo]
                            
                elif classi == 'Outorga':
                    pass
                    
                else:
                    print(classi)
                            
            ##outros
            else:
                print(fonte)
                qvaz = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[6]/div/div/div/div[2]').text.splitlines()
                qmax = max([float(i.replace('.','').replace(',','.')) for i in qvaz[28:40]])
                print('Vazao maxima: {}'.format(qmax))                
                
                tabela_finalidades = driver.find_element_by_xpath('//*[@id="wrap"]/section/div/div/div[1]/fieldset/div/div[11]/div/div/div/div[7]/div/div/div/div[2]').text.splitlines()	
                print(tabela_finalidades)
                
                if qmax < 0.003:
                    pass

                else:
                    if classi == 'Reserva de Disponibilidade Hídrica':
                        valor_da_guia = valor_da_guia + superficial_rdh[fonte][tipo]
                    
                    else:
                        pass

        print('Valor da guia: {}'.format(valor_da_guia))
        valor.append(valor_da_guia)
        
        print('----\n')
            
        #fechando a nova aba
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        time.sleep(10)

    rela['CPF opu CNPJ'] = cpfcnpj
    rela['Situação da guia'] = sit_guia
    rela['Valor'] = valor   
    
print('Finalizado!')
