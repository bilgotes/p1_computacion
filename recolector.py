#! /usr/bin/python

import urllib2 as ul
from lxml import html
import csv
import numpy as np
from pymongo import MongoClient
import time
import datetime

website="https://www.meneame.net"
ts_api_key="51QQO7K0Q533P5FC"
baseURL = 'http://api.thingspeak.com/update?api_key=%s' % ts_api_key

print baseURL


# abre el socket al website
response = ul.urlopen(website)
# lee el contenido y genera un id de fichero
web = response.read()
# convierte el contenido en una estructura tipo HTML
tree=html.fromstring(web)
#titulos=tree.xpath('//div[@id="center-content"//h2//a/text()')

titulo=tree.xpath('//*[@class="news-summary"][1]/div//*[@class="center-content"]/h2/a/text()')
meneos=tree.xpath('//*[@class="news-summary"][1]/div/div/div[@class="votes"]/a/text()')
clics=tree.xpath('//*[@class="news-summary"][1]/div/div/div[@class="clics"]/text()')

titulo = titulo[0]
titulo_ascii = titulo.encode('ascii','ignore')
meneos = int(meneos[0])
clics = int(clics[0].replace('clics',''))
print titulo

pym = MongoClient("mongodb://localhost:27017/")
pymdb = pym["p1"]
pymco = pymdb["meneos"]
dic_men = {"ts" : datetime.datetime.utcnow(), "titulo": titulo, "meneos": meneos, "clics":clics }
x = pymco.insert_one(dic_men)

# inserta los datos en mi canal de ThingSpeak usando GET
get_request = baseURL + "&field1=%s&field2=%s&field3=%s" % (titulo_ascii,meneos,clics) 
response=ul.urlopen(baseURL + "&field1=%s,&field2=%s,&field3=%s" % (titulo_ascii,meneos,clics))
web = response.read()
'''
with open('data.csv','ab') as csvfile:
	escritor = csv.writer(csvfile, delimiter=';')
	with open('tickers.dat') as infile:
		lines=infile.readlines()
		rows=len(lines)
		print rows
		for i in range(1292,rows-1):
			ticker=lines[i].split(';')[0]
			variables=[]
			valores=[]
			tiempos=[]
			#website="http://www.finviz.com/quote.ashx?t="+tickers[i]+"&ty=c&ta=0&p=w"
			website="ettps://www.google.com/finance/historical?q=NASDAQ%3A"+ticker+"&ei=5i_cWPDCI4fIUcTBprAK&start=1&num=100"
			response = urllib2.urlopen(website)
			print website
			web = response.read()
			tree=html.fromstring(web)
			#variables=tree.xpath('//td[@class="snapshot-td2-cp"]/text()')
			variables_list=tree.xpath('//*[@id="prices"]/table/tr/th[position()>1 and position()<6]/text()')
			for j in range(len(variables_list)):
				variables.append(variables_list[j].strip('\n'))
			tiempos_list=tree.xpath('//*[@id="prices"]/table/tr/td[1]/text()')
			for j in range(len(tiempos_list)):
				for h in range(4):
					tiempos.append(tiempos_list[j].strip('\n'))
			for j in range(4,len(tiempos)):
				variables.append(variables[j-4])
			marcas=zip(variables,tiempos)
			#valores=tree.xpath('//td[@class="snapshot-td2"]/b/descendant::text()')
			valores_list=tree.xpath('//*[@id="prices"]/table/tr/td[position()>1 and position()<6]/text()')
			caracteristicas=len(valores_list)
			for j in range(caracteristicas):
				valores.append(valores_list[j].strip('\n'))
			if rows == 0:
				escritor.writerow(['Ticker']+marcas)
			escritor.writerow([ticker]+valores)
'''
