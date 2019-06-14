from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import getpass
import requests
import time
import pprint
import re
import csv


import pandas as pd
from pandas import Series, DataFrame, ExcelWriter
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import tools


def minera(user, senha):

    PAUSE_TIME = 5

    chrome_path = './chromedriver'

    driver = webdriver.Chrome(chrome_path)
    driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
    driver.find_element_by_xpath("""//*[@id="username"]""").send_keys(user)
    driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(senha)
    driver.find_element_by_xpath("""//*[@id="app__container"]/main/div/form/div[3]/button""").click()

    driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height

    page = driver.page_source
    links = re.findall(r'/in/+[\w\.-]+', page )

    oldLink = ""    
    cont = 1
    my_list = []

    with open('datasets/linkedinMinera.csv', 'w', newline="") as csvFile:
        writer = csv.writer(csvFile, delimiter=';')
        writer.writerow(["CONTADOR", "NOME", "CARGO", "EMPRESA", "INSTITUICAO DE ENSINO"])

        for link in links:

            if oldLink != link:

                driver.get("https://www.linkedin.com"+link)
                try:
                    nome = driver.find_element_by_xpath("""//*[@id="ember45"]/div[2]/div[2]/div[1]/ul[1]/li[1]""").text
                except:
                    nome = ""
                    
                try:
                    cargo = driver.find_element_by_xpath("""//*[@id="ember45"]/div[2]/div[2]/div[1]/h2""").text
                except:
                    cargo = ""

                try:
                    empresa = driver.find_element_by_xpath("""//*[@id="ember102"]""").text
                except:
                    empresa = ""

                try:
                    instEnsino = driver.find_element_by_xpath("""//*[@id="ember105"]""").text
                except:
                    instEnsino = ""   

                if nome != "":  
                    row = [str(cont)]
                    row.append(nome)
                    row.append(cargo)                  
                    row.append(empresa)
                    row.append(instEnsino)

                    #Grava no Arquivo CSV
                    try:
                        writer.writerow(row)
                        print(str(cont)+";"+nome+";"+cargo+";"+empresa+";"+instEnsino)
                        cont = cont+1
                    except:
                        print("Erro de encoding, perfil ignorado de: "+nome )              
                    
                # Wait to load page
                #time.sleep(PAUSE_TIME)
            oldLink = link

    csvFile.close() 

def grafico(sigaFile):
    minerFile = "datasets/linkedinMinera.csv"
    df = pd.DataFrame(pd.read_excel(sigaFile))
    df2 = pd.DataFrame(pd.read_csv(minerFile, delimiter=";", encoding = "ISO-8859-1"))

    data_xls = pd.read_excel(sigaFile, index_col=None)
    data_xls.to_csv('datasets/allStudents_contador.csv',index=False,header=None , encoding = "ISO-8859-1")

    data_xls = pd.read_excel('datasets/sakaueTreatedOnGoing.xlsx', index_col=None)
    data_xls.to_csv('datasets/trabalho_cursando_contador.csv',index=False,header=None , encoding = "ISO-8859-1")

    valuesOnGoing = {
        'situacao':[],
        'curso':[],
        'turno':[],
        'ra':[],
        'nome_aluno':[],
        'cargo':[],
        'empresa':[],
        'instituicao':[]
    }

    valuesFinished = {
        'situacao':[],
        'curso':[],
        'turno':[],
        'ra':[],
        'nome_aluno':[],
        'cargo':[],
        'empresa':[],
        'instituicao':[]
    }

    for nameMiner in df2['NOME']:
        for nameSiga in df['Nome Aluno']:
            if(nameSiga.upper() == nameMiner.upper()):
                
                auxValuesMiner = df2.loc[df2['NOME'] == nameMiner].iloc[0]
                    
                if(len(df.loc[(df['Nome Aluno'] == nameSiga)&(df['Situacao'] == 'Graduado')]) > 0 or len(df.loc[(df['Nome Aluno'] == nameSiga) & (df['Situacao'] == 'Concluído')]) > 0):
                    auxValuesSiga = df.loc[(df['Nome Aluno'] == nameSiga)&(df['Situacao'] == 'Graduado')].iloc[0] if len(df.loc[(df['Nome Aluno'] == nameSiga)&(df['Situacao'] == 'Graduado')]) > 0 else df.loc[(df['Nome Aluno'] == nameSiga)&(df['Situacao'] == 'Concluído')].iloc[0]
                    valuesFinished['situacao'].append(str(auxValuesSiga['Situacao']))
                    valuesFinished['curso'].append(auxValuesSiga['Curso'])
                    valuesFinished['turno'].append(auxValuesSiga['Turno'])
                    valuesFinished['ra'].append(auxValuesSiga['RA'])
                    valuesFinished['nome_aluno'].append(auxValuesSiga['Nome Aluno'])
                    valuesFinished['cargo'].append(auxValuesMiner['CARGO'])
                    valuesFinished['empresa'].append(auxValuesMiner['EMPRESA'])
                    valuesFinished['instituicao'].append(auxValuesMiner['INSTITUICAO DE ENSINO'])
                        
                elif(len(df.loc[(df['Nome Aluno'] == nameSiga)&(df['Situacao'] == 'Cursando')]) > 0):
                    auxValuesSiga = df.loc[(df['Nome Aluno'] == nameSiga)&(df['Situacao'] == 'Cursando')].iloc[0] 
                    valuesOnGoing['situacao'].append(str(auxValuesSiga['Situacao']))
                    valuesOnGoing['curso'].append(auxValuesSiga['Curso'])
                    valuesOnGoing['turno'].append(auxValuesSiga['Turno'])
                    valuesOnGoing['ra'].append(auxValuesSiga['RA'])
                    valuesOnGoing['nome_aluno'].append(auxValuesSiga['Nome Aluno'])
                    valuesOnGoing['cargo'].append(auxValuesMiner['CARGO'])
                    valuesOnGoing['empresa'].append(auxValuesMiner['EMPRESA'])
                    valuesOnGoing['instituicao'].append(auxValuesMiner['INSTITUICAO DE ENSINO'])

    newDataOnGoing = pd.DataFrame({
        'SITUAÇÃO': valuesOnGoing['situacao'],
        'CURSO': valuesOnGoing['curso'],
        'TURNO': valuesOnGoing['turno'],
        'RA': valuesOnGoing['ra'],
        'NOME ALUNO': valuesOnGoing['nome_aluno'],
        'CARGO': valuesOnGoing['cargo'],
        'EMPRESA': valuesOnGoing['empresa'],
        'INSTITUICAO DE ENSINO': valuesOnGoing['instituicao'],
    }, columns=['SITUAÇÃO','CURSO','TURNO','RA','NOME ALUNO','CARGO','EMPRESA','INSTITUICAO DE ENSINO'])
    

    newDataFinished = pd.DataFrame({
        'SITUAÇÃO': valuesFinished['situacao'],
        'CURSO': valuesFinished['curso'],
        'TURNO': valuesFinished['turno'],
        'RA': valuesFinished['ra'],
        'NOME ALUNO': valuesFinished['nome_aluno'],
        'CARGO': valuesFinished['cargo'],
        'EMPRESA': valuesFinished['empresa'],
        'INSTITUICAO DE ENSINO': valuesFinished['instituicao'],
    }, columns=['SITUAÇÃO','CURSO','TURNO','RA','NOME ALUNO','CARGO','EMPRESA','INSTITUICAO DE ENSINO'])

    writer = pd.ExcelWriter('datasets/sakaueTreatedOnGoing.xlsx', engine='xlsxwriter')
    newDataOnGoing.to_excel(writer, sheet_name='Sheet1')
    writer.save()

    writer = pd.ExcelWriter('datasets/sakaueTreatedFinished.xlsx', engine='xlsxwriter')
    newDataFinished.to_excel(writer, sheet_name='Sheet1')
    writer.save()

    #estudantes trabalhando em curso
    estudantesTrabalhando = (len(newDataOnGoing))

    #formados estralhando
    formadosTrabalhando = (len(newDataFinished))

    #criando array de dados
    arraydados = [estudantesTrabalhando, formadosTrabalhando]

    #criando array de labels
    arraysituacao = ['Estudantes Trabalhando', 'Formados Trabalhando']

    #total de aluno por curso na fatec
    ana = (calcular_tipo('Cursando,AN'))
    manuf = (calcular_tipo('Cursando,MANUF'))
    manut = (calcular_tipo('Cursando,MANUT'))
    aut = (calcular_tipo('Cursando,AUT'))
    gest_p = (calcular_tipo('Cursando,GEST.P'))
    gestao = (calcular_tipo('Cursando,GESTÃO'))
    banco = (calcular_tipo('Cursando,B'))
    logis = (calcular_tipo('Cursando,LOG'))
    proj = (calcular_tipo('Cursando,PRO'))

    arraydadoscrusando = [ana,manuf,manut,aut,gest_p,gestao,banco,logis,proj]
    arraycursolabel = ['ANÁLISE E DESENV. DE SISTEMAS','MANUFATURA AVANÇADA','MANUTENÇÃO AERONAVES','AUTOMAÇÃO MANUFATURA DIGITAL','GEST.PROD.INDUSTRIAL','GESTÃO EMPRESARIAL',
    'BANCO DE DADOS','LOGÍSTICA','PROJ. ESTRUT. AERONAUTICAS']

    totalcursando = str(ana+manuf+manut+aut+gest_p+gestao+banco+logis+proj)

    alunostrabalhando = str(estudantesTrabalhando+formadosTrabalhando)

    #total de aluno por trabalhando na fatec por curso
    ana_c = (contador_trabalhando('Cursando,AN'))
    manuf_c = (contador_trabalhando('Cursando,MANUF'))
    manut_c = (contador_trabalhando('Cursando,MANUT'))
    aut_c = (contador_trabalhando('Cursando,AUT'))
    gest_p_c = (contador_trabalhando('Cursando,GEST.P'))
    gestao_c = (contador_trabalhando('Cursando,GESTÃO'))
    banco_c = (contador_trabalhando('Cursando,B'))
    logis_c = (contador_trabalhando('Cursando,LOG'))
    proj_c = (contador_trabalhando('Cursando,PRO'))

    arraydadoscrusando_t = [ana_c,manuf_c,manut_c,aut_c,gest_p_c,gestao_c,banco_c,logis_c,proj_c]


    comparacaotrabalhando = [(int(totalcursando)-estudantesTrabalhando),estudantesTrabalhando, formadosTrabalhando ]
    comparacaotrabalhandosituacao = ['Sem informação', 'Alunos', 'Formado']


    sources_pie = go.Pie(labels=arraysituacao, rotation = 47, values=arraydados, domain={'row':0, 'column' : 0}, showlegend=False, name='', textinfo='label+percent',hoverinfo='label+percent+value')

    flavor_pie = go.Pie(labels=arraycursolabel, values=arraydadoscrusando, domain={'row':0, 'column' : 1}, showlegend=False, name='', textinfo='label+percent',hoverinfo='label+percent+value')

    sources_pie1 = go.Pie(labels=comparacaotrabalhandosituacao, rotation = 45, values=comparacaotrabalhando, domain={'row':1, 'column' : 0}, showlegend=False, name='', textinfo='label+percent',hoverinfo='label+percent+value')

    flavor_pie1 = go.Pie(labels=arraycursolabel, values=arraydadoscrusando_t, rotation = 345, domain={'row':1, 'column' : 1}, showlegend=False, name='', textinfo='label+percent',hoverinfo='label+percent+value')




    layout = go.Layout(autosize = True,
                    title = {'text':'ANÁLISE DE TRABALHO DE ALUNOS DA FATEC SJC', "font": { "size": 25}},
                    grid = {'rows': 2, 'columns': 2},
                    annotations =  [
                        { "font": { "size": 17},
                        "showarrow": False,
                        "text": "Alunos trabalhando("+alunostrabalhando+')',
                            "x": 0.16,
                            "y": 1.07
                        },
                        { "font": { "size": 17},
                        "showarrow": False,
                        "text": "Alunos por Curso - ("+totalcursando+')',
                            "x": 0.87,
                            "y": 1.07
                        },
                        { "font": { "size": 17},
                        "showarrow": False,
                        "text": "Alunos e Graduado trabalhando",
                            "x": 0.13,
                            "y": -0.06
                        },
                        { "font": { "size": 17},
                        "showarrow": False,
                        "text": "Alunos trabalhando<br> por curso",
                            "x": 0.99,
                            "y": 0.20
                        }
                        
                        ])

    fig = go.Figure(data = [sources_pie,flavor_pie, sources_pie1, flavor_pie1], layout = layout)

    plot(fig, filename='datasets/Gráfico da Análise.html')

def calcular_tipo(tipo):
    contador = 0
    with open('datasets/allStudents_contador.csv') as arquivo:
        for linha in arquivo:
            if tipo in linha:
                contador += 1
    return(contador)
	
	
def contador_trabalhando(tipo):
    contador = 0
    with open('datasets/trabalho_cursando_contador.csv') as arquivo:
        for linha in arquivo:
            if tipo in linha:
                contador += 1
    return(contador)
	


