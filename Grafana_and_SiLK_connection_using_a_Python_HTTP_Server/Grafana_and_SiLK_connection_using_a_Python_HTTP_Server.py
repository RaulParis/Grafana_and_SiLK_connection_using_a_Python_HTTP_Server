# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import print_function
from http.server import BaseHTTPRequestHandler, HTTPServer
from silk import * 
import time
import json
import sys
import os
import datetime
import geoip2.database
from collections import defaultdict

#Define global variables / Definimos las variables globales que serán utilizadas a lo largo del cógigo
hostName = "localhost"
hostPort = 9000
#geoip2 database, download from their official website / Esta es la base de datos del módulo geoip2, descargada de su página oficial
reader = geoip2.database.Reader('/data/prueba2/GeoLite2-City_20190319/GeoLite2-City.mmdb')
auxi1=1
auxi2=1
auxi3=1
auxi4=1
global time_minmej
global time_maxmej
time_minmej=1
time_maxmej=1

#Define server class / Definimos el servidor
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self): #if it is a GET query / Si es una petición GET
        self.send_response(200) #Answer 200 / Repondemos 200
        self.send_header("Content-type", "text/html") #HTML type / Tipo HTML
        self.end_headers()
    def do_POST(self): #if it is a POST query / Si es una petición POST
        content_type = (self.headers.get('content-type',0)) #Verificar json
        global values #Define values as global / Definimos values como global
        if (content_type=="application/json"): #if it is a JSON object / Si se trata de un objeto JSON
        	if (self.path != "/search"): #And it is a query from /search / Y viene dirigido a /search
	             content_len = int(self.headers.get('content-length',0)) #Verificar json

	             post_body = self.rfile.read(content_len)

	             body_aux = json.loads(post_body)

	             time_min = (body_aux['range'])['from'] #Extract the min time of the query / Extraemos el tiempo minimo de la petición
	             time_min = datetime.datetime.strptime(time_min, "%Y-%m-%dT%H:%M:%S.%fZ") # Lo convertimos a datetime
	             time_min = time_min + datetime.timedelta(hours=0)
	             time_min_aux = datetime.datetime(time_min.year,time_min.month,time_min.day,time_min.hour,time_min.minute,time_min.second).timestamp()
	             time_min_aux = datetime.datetime(time_min.year,time_min.month,time_min.day,time_min.hour,time_min.minute,time_min.second).replace(tzinfo=datetime.timezone.utc).timestamp() #Hacemos cambio al tiempo con nuestra hora local

	             time_max = (body_aux['range'])['to'] #Extract the max time of the query / Extraemos el tiempo maximo de la petición
	             time_max = datetime.datetime.strptime(time_max, "%Y-%m-%dT%H:%M:%S.%fZ") #convert it to datetime / Lo convertimos a datetime
	             time_max = time_max + datetime.timedelta(hours=0)
	             time_max_aux = datetime.datetime(time_max.year,time_max.month,time_max.day,time_max.hour,time_max.minute,time_max.second).timestamp()
	             time_max_aux = datetime.datetime(time_max.year,time_max.month,time_max.day,time_max.hour,time_max.minute,time_max.second).replace(tzinfo=datetime.timezone.utc).timestamp() #Hacemos cambio al tiempo con nuestra hora local

	             interval = body_aux['intervalMs']/1000


	             variables = "" #Create the variable which will store Grafana variables / Creamos la variable donde se almacenarán las variables de Grafana

	             if 'IPs' in (body_aux['scopedVars']): #if Ips in scopedVars exists / Si existe el campo en scopedVars
	                 if (((body_aux['scopedVars'])['IPs'])['text']) != "": #if it contains something / Si contiene algo
	             	     variables = variables + " --scidr=" + str(((body_aux['scopedVars'])['IPs'])['text'])

	             if 'IPd' in (body_aux['scopedVars']): #if Ipd in scopedVars exists / Si existe el campo en scopedVars
	                 if (((body_aux['scopedVars'])['IPd'])['text']) != "": #if it contains something / Si contiene algo
	             	     variables = variables + " --dcidr=" + str(((body_aux['scopedVars'])['IPd'])['text'])

	             if 'PortS' in (body_aux['scopedVars']): #if PortS in scopedVars exists / Si existe el campo en scopedVars
	                 if (((body_aux['scopedVars'])['PortS'])['text']) != "": #if it contains something / Si contiene algo
	                     variables = variables + " --sport=" + str(((body_aux['scopedVars'])['PortS'])['text'])

	             if 'PortD' in (body_aux['scopedVars']): #if PortD in scopedVars exists / Si existe el campo en scopedVars
	                 if (((body_aux['scopedVars'])['PortD'])['text']) != "": #if it contains something / Si contiene algo
	                     variables = variables + " --dport=" + str(((body_aux['scopedVars'])['PortD'])['text'])

	             if 'Bytes_Range' in (body_aux['scopedVars']): #if Bytes_Range in scopedVars exists / Si existe el campo en scopedVars
	                 if (((body_aux['scopedVars'])['Bytes_Range'])['text']) != "": #if it contains something / Si contiene algo
	                     variables = variables + " --bytes=" + str(((body_aux['scopedVars'])['Bytes_Range'])['text'])

	             if 'Filtro_silk' in (body_aux['scopedVars']): #if Filtro silk in scopedVars exists / Si existe el campo en scopedVars
	                 if (((body_aux['scopedVars'])['Filtro_silk'])['text']) != "": #if it contains something / Si contiene algo
	             	     variables = variables + " " + str(((body_aux['scopedVars'])['Filtro_silk'])['text'])

	             if (body_aux['maxDataPoints']) == 1: #If maxDataPoints is 1 / En el caso de que maxdatapoints sea 1
	                 global time_minmej #we load global variables / Cargamos variables globales dentro del if
	                 global time_maxmej
	                 if (time_min != time_minmej) or (time_max != time_maxmej): #If the query has the same time range than the one before / Si la petición no tiene el mismo rango de tiempo que la anterior
	                     try:
	                         os.system('rm filtro.rw') #It is removed / Se borra el anterior
	                         #And it is done a new filter / Y se realiza el nuevo filtro
	                         comando = 'sudo rwfilter --start-date='+str(time_min.year)+'/'+str(time_min.month)+'/'+str(time_min.day)+':'+str(time_min.hour)+' --end-date='+str(time_max.year)+'/'+str(time_max.month)+'/'+str(time_max.day)+':'+str(time_max.hour)+' --type=all ' + str(variables) + ' --proto=6 --pass-destination=filtro.rw'
	                         os.system(comando)
	                         
	                     except:
	                         hostPort = 9000
	                 time_maxmej = time_max #We save time range / Guardamos los rangos de tiempo de las peticiones
	                 time_minmej = time_min

	                 infile = silkfile_open("filtro.rw", READ) #Reed the results of the filter / Leemos el resultado del filtro

	                 values = '[' #Create response variable / Creamos la variable de la respuesta
	                 my_dict = defaultdict(int) #Inizializate dic of ints / Inicializamos un diccionario de ints

	                 for rec in infile: #For each register in the file / Para cada registro del archivo de registros
	                     try:
	                         response = reader.city(str(rec.sip)) #Localizate IP / Localizamos la IP
	                         my_dict[response.country.iso_code] += 1 #Index city to dict / La indexamos en el diccionario
	                     except:
	                     	 hostPort = 9000
	                 for key in my_dict: #For each key / Para cada clave del diccionario
	                 	 values = values + '{"target": ' + '"' + str(key) + '", "datapoints": [[' + str(my_dict[key]) + ',' + str(rec.etime_epoch_secs) + ']]},' #Build the response / Construimos la respuesta
	                 values = values[:-1] + "]" #CLose the JSON object / Cerramos el JSON

	             elif (body_aux['maxDataPoints']) == 3: #If maxdatapoints is 3 / En el caso de que maxdatapoints sea 3
	                 
	                 if (time_min != time_minmej) or (time_max != time_maxmej): #If the query doesn't have the same timerange / Si la petición no tiene el mismo rango de tiempo que la anterior
	                     try:
	                         os.system('rm filtro.rw') #It is removed / Se borra el anterior
	                         #And it is done a new filter / Y se realiza el nuevo filtro
	                         comando = 'sudo rwfilter --start-date='+str(time_min.year)+'/'+str(time_min.month)+'/'+str(time_min.day)+':'+str(time_min.hour)+' --end-date='+str(time_max.year)+'/'+str(time_max.month)+'/'+str(time_max.day)+':'+str(time_max.hour)+' --type=all ' + str(variables) + ' --proto=6 --pass-destination=filtro.rw'
	                         os.system(comando)

	                     except:
	                         hostPort = 9000
	                 time_maxmej = time_max #We save time range / Guardamos los rangos de tiempo de las peticiones
	                 time_minmej = time_min

	                 infile = silkfile_open("filtro.rw", READ) #Reed the results of the filter / Leemos el resultado del filtro

	                 global auxi4

	                 seleccion_aux_pie = (auxi4%4)+1 #Calculate the representation / Calculamos la respresenación
                     
	                 if (seleccion_aux_pie) == 1: #If it is 1 / Si es 1
	                 	seleccion_aux_pie = 'CountryS' #Countrys will be plotted / Se representarán paises

	                 elif (seleccion_aux_pie) == 2: #If it is 2 / Si es 2
	                    seleccion_aux_pie = 'IPS' #IPs will be plotted / Se representarán IPs

	                 elif (seleccion_aux_pie) == 3: #If it is 3 / Si es 3
	                 	seleccion_aux_pie = 'PortS' #PortS will be plotted / Se representarán puertos
                         
	                 else: #if not / Sino
	                 	seleccion_aux_pie = 'application' #Application would be represented / Se representará la aplicación
	                     
	                 auxi4 +=1	#Add 1 to variable / Sumamos 1 a la variable
	                 values = '[' #Create response variable / Creamos la variable de la respuesta
	                 my_dict = defaultdict(int) #Inizializate dict of ints / Inicializamos un diccionario de ints

	                 if (seleccion_aux_pie) == 'CountryS': #If countryS will be plotted / Si se representarán paises

	                     for rec in infile: #For each register in the file / Para cada registro del archivo de registros
	                         try:
	                             response = reader.city(str(rec.sip)) #Locate the IP / Localizamos la IP
	                             my_dict[response.country.iso_code] += 1 #Index it to the dict / La indexamos en el diccionario
	                         except:
	                             hostPort = 9000
	                     for key, value in sorted(my_dict.items(), key=lambda x: x[1], reverse=True): #For each key of the dict in reverse order / Para cada clave del diccionario ordenado de menor a mayor
	                         values = values + '{"target": ' + '"' + str(key) + '", "datapoints": [[' + str(value) + ',' + str(rec.etime_epoch_secs) + ']]},' #Index the values / Indexamos los valores
	                 elif (seleccion_aux_pie) == 'IPS': #If Ips wil be represented / Si se representarán IPs

	                     for rec in infile: #For each key of the registers / Para cada registro del archivo de registros
	                         try:
	                             my_dict[rec.sip] += 1 #Index it to the dict / La indexamos en el diccionario
	                         except:
	                             hostPort = 9000
	                     for key, value in sorted(my_dict.items(), key=lambda x: x[1], reverse=True): #For each key of the dict in reverse order / Para cada clave del diccionario ordenado de menor a mayor
	                         values = values + '{"target": ' + '"' + str(key) + '", "datapoints": [[' + str(value) + ',' + str(rec.etime_epoch_secs) + ']]},' #Index the values / Indexamos los valores

	                 elif (seleccion_aux_pie) == 'PortS': #If Ips wil be represented / Si se representarán puertos

	                     for rec in infile: #For each key of the registers / Para cada registro del archivo de registros
	                         try:
	                             my_dict[rec.sport] += 1 #Index it to the dict / La indexamos en el diccionario
	                         except:
	                             hostPort = 9000
	                     for key, value in sorted(my_dict.items(), key=lambda x: x[1], reverse=True): #For each key of the dict in reverse order / Para cada clave del diccionario ordenado de menor a mayor
	                         values = values + '{"target": ' + '"' + str(key) + '", "datapoints": [[' + str(value) + ',' + str(rec.etime_epoch_secs) + ']]},' #Index the values / Indexamos los valores

	                 elif (seleccion_aux_pie) == 'application': #If Ips wil be represented / Si se representarán aplicaciones

	                     for rec in infile: #For each key of the registers / Para cada registro del archivo de registros
	                         try:
	                             my_dict[rec.application] += 1 #Index it to the dict / La indexamos en el diccionario
	                         except:
	                             hostPort = 9000
	                     for key, value in sorted(my_dict.items(), key=lambda x: x[1], reverse=True): #For each key of the dict in reverse order / Para cada clave del diccionario ordenado de menor a mayor
	                         values = values + '{"target": ' + '"' + str(key) + '", "datapoints": [[' + str(value) + ',' + str(rec.etime_epoch_secs) + ']]},' #Index the values / Indexamos los valores

	                 values = values[:-1] + "]" #Close JSON object / Cerramos el objeto JSON

	             else: #If maxdatapoints isn't neither 1 or 3 / Si no tiene ni 1 ni 3 en el maxdatopints

	                 if 'target' in (body_aux['targets']): #If target exists in targets / SI existe el campo
	                     filters = ((body_aux['targets'])['target']) #Filters are saved / Se guarda en filters
	                     #Filter is done with the counting / Se realiza el filtro concatenado con el cuenteo
	                     comando = 'sudo rwfilter --start-date='+str(time_min.year)+'/'+str(time_min.month)+'/'+str(time_min.day)+':'+str(time_min.hour)+' --end-date='+str(time_max.year)+'/'+str(time_max.month)+'/'+str(time_max.day)+':'+str(time_max.hour)+' --type=all ' + str(filters) + str(variables) + ' --proto=6 --pass=stdout | rwcount --start-time=' + str(time_min.year) + '/' + str(time_min.month) + '/' + str(time_min.day) + ':'  +  str(time_min.hour) + ':' + str(time_min.minute) + ':' + str(time_min.second) + ' --end-time=' + str(time_max.year) + '/' + str(time_max.month) + '/' + str(time_max.day) + ':'  +  str(time_max.hour) + ':' + str(time_max.minute) + ':' + str(time_max.second) + ' --bin-size=' + str(interval) + '>cuenta.txt'
	             
	                 else: #If there are no variables / Si no existen variables
	                     comando = 'sudo rwfilter --start-date='+str(time_min.year)+'/'+str(time_min.month)+'/'+str(time_min.day)+':'+str(time_min.hour)+' --end-date='+str(time_max.year)+'/'+str(time_max.month)+'/'+str(time_max.day)+':'+str(time_max.hour)+' --type=all ' + str(variables) + ' --proto=6 --pass=stdout | rwcount --start-time=' + str(time_min.year) + '/' + str(time_min.month) + '/' + str(time_min.day) + ':'  +  str(time_min.hour) + ':' + str(time_min.minute) + ':' + str(time_min.second) + ' --end-time=' + str(time_max.year) + '/' + str(time_max.month) + '/' + str(time_max.day) + ':'  +  str(time_max.hour) + ':' + str(time_max.minute) + ':' + str(time_max.second) + ' --bin-size=' + str(interval) + '>cuenta.txt'
	              
	                 os.system(comando) #It is done at terminal / Se ejecuta
	                 
	                 if (body_aux['maxDataPoints']) == 1: #If maxdatapoints is 1 / En el caso de que maxdatapoints sea 1
	                     global auxi1 #Variable is load / Se invoca la variable
	                     seleccion_aux = (auxi1%3)+1 #Add 1 to seleeccion_aux / Se incrementa en 1
	                     auxi1 += 1 #Add 1 to aux var / Se incrementa en 1

	                 elif (body_aux['maxDataPoints']) == 100: #If maxdatapoints is 100 / En el caso de que maxdatapoints sea 100
	                     global auxi2 #Variable is load / Se invoca la variable
	                     seleccion_aux = (auxi2%3)+1 #Add 1 to seleeccion_aux / Se incrementa en 1
	                     auxi2 += 1 #Add 1 to aux var / Se incrementa en 1

	                 elif (body_aux['maxDataPoints']) == 3: #If maxdatapoints is 3 / En el caso de que maxdatapoints sea 3
	                     auxi4 +=1 #Add 1 to aux var / Se incrementa en 1

	                 else: #If datapoints isnt any of the ones before / En el caso de que no sea ninguno
	                     global auxi3 #Variable is load / Se invoca la variable
	                     seleccion_aux = (auxi3%3)+1 #Add 1 to seleeccion_aux / Se incrementa en 1
	                     auxi3 += 1 #Add 1 to aux var / Se incrementa en 1

	                 time_min_filter = time_min_aux #Save timerange in an aux time var / Guardamos el tiempo en una variable auxiliar

	                 try: #If it can be done / Se intenta

	                     with open(r"/data/prueba2/cuenta.txt", "r+") as f: #Open the results / Abrimos el resultado
	                         values = '[{"datapoints": [' #Create values variable / Creamos la variable con los valores
	                         global coloumn2 #Load variables in the with / Cargamos variables globales dentro del with
	                         coloumn2 = [] #Create the variable which be filled / Creamos la variable que será rellenada
	                         global n
	                         n = 0 #Create a control values / Creamos un valor de control
	                         data = f.readlines() #Reed lines / Leemos las lineas
	                 
	                         for line in data: #FOr each line / Para cada linea
	                             if (n==1): #If n is 1 / Si n es 1
	                                 if (body_aux['maxDataPoints']) == 100: #If maxdatapoints is 100 / Si el maxdatapoints es 100
	                                     coloumn2.append(str(float(line.strip().split("|")[seleccion_aux])/5.95)) #Index value / Indezamos el valor 
	                                 else: #If not / Sino
	                                     coloumn2.append(line.strip().split("|")[seleccion_aux]) #Index value / Indexamos el valor

	                             n=1 #Control to jump the first line / Ya nos hemos saltado la primera linea

	                         while True: #Forever / Para siempre
	                             values = values + "[" + str(coloumn2[n-1][:].strip()) + ", " + str(time_min_filter*1000) + "], " #Index value / Indexamos el valor
	                             time_min_filter += interval #Add indexed time to the time range / Sumamos el tiempo indexado al intervalo
	                             n+=1 #Add 1 to n / Aumentamos n

	                             if(time_min_filter>=(time_max_aux)): #If time is out of time range / Si nos hemos pasado de tiempo
	                                 break #Jump out of the loop / Salimos del bucle

	                         values = values + "[" + str(coloumn2[n-2][:].strip()) + ", " + str(time_min_filter*1000) + "]]}]"  #Index last value and close / Indexamos el último valor y cerramos
	                 except:
	                 	 hostPort = 9000  

	             #We just need to send it / Aqui ya lo tenemos para enviar

	             self.send_response(200) #Send an OK / Enviamos un OK
	             self.send_header("Content-type", "application/json; charset=UTF-8") #INdex type / Indicamos el tipo
	             self.end_headers()
	             self.wfile.write(str.encode(values)) #Send JSON / Enviamos el JSON
myServer = HTTPServer((hostName, hostPort), MyServer) #Define server / Definimos el servidor
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort)) #Print query in terminal / Imprimimos petición por pantalla

try:
    myServer.serve_forever() #Forever executing / Se ejecuta siempre
except KeyboardInterrupt: #If it is not interrupted / Mientras no se interrumpa
    pass
reader.close() #Close reader / Cerramos el reader
myServer.server_close() #Close server / Cerramos el servidor
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort)) #Print close message / Imprimimos mensaje de cierre
