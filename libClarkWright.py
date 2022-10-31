import itertools
import libBins, copy

path = '//azrwcfs01acbr/Sectores/Ruteador_DLI/Data/'

class cRotasPack(object):    
    """
    Esta clase contiene los algoritmos necesarios para el calculo de costo por el metodo de Clark & Wright.
    Las listas ordenadas con las rutas estaran dentro de este mismo objeto.
    El constructor solo va a crear los arrays de instancia.
    """

    def __init__(self):
        self.conteiner_economias = []   # va a retener una lista de items del tipo cEconomiaItem
        self.conteiner_rotas = []       # contendra la poblacion de Clark Wright
        self.conteiner_rotas_bins = []  # temporario para debug, despues borrar

    # tendre un array con los N bins en main.lista_bins.conteiner_entregas_consolidadas     (RUTA, INDICE, CBIN)
    # preciso hacer el ciclo por cada permutacion posible

    def genera_combinaciones(self, conteiner_entregas_consolidadas, matriz_distancia_cidades, v_cidade_usina):
        for combo in itertools.combinations(conteiner_entregas_consolidadas, 2):  # aqui tendremos combo[0,1] con cada combinacion posible de las entregas consolidadas
            recordEconomia = cEconomiaItem(combo, matriz_distancia_cidades, v_cidade_usina) # creo un registro para cada combinacion de ciudades possible (dentro del universo de la lista de items)
            self.conteiner_economias.append(recordEconomia)
        self.conteiner_economias.sort(key=lambda econoRec: econoRec.economia, reverse = True)

    def construye_poblacion(self, conteiner_entregas_consolidadas, binCap, matriz_compatibilidade_familia, raio_consolidacao, cantidad_max_rutas_bsas, cantidad_max_rutas_arg):
        

        contador = -1
        for econoItem in self.conteiner_economias: # para cada item de la lista de economias (matriz con todas las combinaciones posibles entre entregas consolidadas)
            # econoItem traera un par de bins en una supuesta ruta calculada
            contador += 1

            bin1 = conteiner_entregas_consolidadas[econoItem.indiceBin1][1]
            bin2 = conteiner_entregas_consolidadas[econoItem.indiceBin2][1]

            if ((bin1.rota == -1) and (bin2.rota == -1)):   # testea si uno de los bins ya fue asignado en una ruta previa
            # si ninguno esta asignado crea nueva ruta.
            # obtiene las cargas de los dos bins, qt de clientes de las dos y hace el testeo de si se pueden juntar las dos en uno solo
                cenario = 1
                quantidade_clientes_no1 = bin1.soma_entregas()
                quantidade_clientes_no2 = bin2.soma_entregas()
                if (self.valida_volume_absorvido(cenario, econoItem, conteiner_entregas_consolidadas, binCap)): # antiguo resultado_soma, se refiere al peso real de los dos nodos
                   
                    #ACA RESOLVER CANTIDAD MAX
                #if ((quantidade_clientes_no1 + quantidade_clientes_no2) <= qt_max_clientes):
                    
                    if (self.valida_qt_rutas(bin1,bin2,cantidad_max_rutas_bsas,cantidad_max_rutas_arg)):
                        if (econoItem.distancia < raio_consolidacao):
                            if (self.valida_mistura_de_familias(1, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia)):
                                roteiro = len(self.conteiner_rotas)
                                self.conteiner_rotas.append(cRota(roteiro)) # contiene los transportes
                                self.conteiner_rotas[roteiro].insere_entregas(bin1.lista_itens)
                                self.conteiner_rotas[roteiro].insere_entregas(bin2.lista_itens)
                                
                                self.conteiner_rotas_bins.append(cRota(roteiro))
                                self.conteiner_rotas_bins[roteiro].insere_entregas(bin1)
                                self.conteiner_rotas_bins[roteiro].insere_entregas(bin2)
                                
                                bin1.rota = roteiro;
                                bin2.rota = roteiro;

            elif ((bin1.rota != -1) and (bin2.rota == -1)): # transporte 1 ya asignado
                cenario = 2
                roteiro_1 = bin1.rota
                rota1 = self.conteiner_rotas[roteiro_1];
                ponta_esquerda = rota1.entregas[0] # adquiero los bins de las esquinas de esta entrega
                ponta_direita = rota1.entregas[len(rota1.entregas)-1]
                quantidade_clientes_no1 = rota1.total_clientes(conteiner_entregas_consolidadas)
                quantidade_clientes_no2 = bin2.soma_entregas()
                if (self.valida_volume_absorvido(cenario, econoItem, conteiner_entregas_consolidadas, binCap)): # antiguo resultado_soma, se refiere al peso real de los dos nodos
                    #if ((quantidade_clientes_no1 + quantidade_clientes_no2) <= qt_max_clientes):
                    if (self.valida_qt_rutas(bin1,bin2,cantidad_max_rutas_bsas,cantidad_max_rutas_arg)):
                        if (econoItem.distancia < raio_consolidacao):
                            if (self.valida_mistura_de_familias(1, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia)):
                                if (econoItem.indiceBin1 == ponta_esquerda or econoItem.indiceBin1 == ponta_direita):
                                    self.conteiner_rotas[roteiro_1].insere_entregas(bin2.lista_itens)
                                    self.conteiner_rotas_bins[roteiro_1].insere_entregas(bin2)
                                    bin2.rota = roteiro;
                     

                     
            elif ((bin1.rota == -1) and (bin2.rota != -1)): # Transporte 2 ya alocado
                cenario = 3
                roteiro_2 = bin2.rota
                rota2 = self.conteiner_rotas[roteiro_2];
                ponta_esquerda = rota2.entregas[0]
                ponta_direita = rota2.entregas[len(rota2.entregas)-1]
                quantidade_clientes_no1 = bin1.soma_entregas()
                quantidade_clientes_no2 = rota2.total_clientes(conteiner_entregas_consolidadas)
                if (self.valida_volume_absorvido(cenario, econoItem, conteiner_entregas_consolidadas, binCap)): #antigo resultado_soma, se refere ao peso real dos dois nos
                    #if ((quantidade_clientes_no1 + quantidade_clientes_no2) <= qt_max_clientes):
                    if (self.valida_qt_rutas(bin1,bin2,cantidad_max_rutas_bsas,cantidad_max_rutas_arg)):
                        if (econoItem.distancia < raio_consolidacao):
                            if (self.valida_mistura_de_familias(1, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia)):
                                if (econoItem.indiceBin2 == ponta_esquerda or econoItem.indiceBin2 == ponta_direita):
                                    self.conteiner_rotas[roteiro_2].insere_entregas(bin1.lista_itens)
                                    self.conteiner_rotas_bins[roteiro_2].insere_entregas(bin1)
                                    bin1.rota = roteiro;

            else: # ambos asignados
                cenario = 4
                roteiro_1 = bin1.rota
                rota1 = self.conteiner_rotas[roteiro_1]
                rota1_bin = self.conteiner_rotas_bins[roteiro_1]
                ponta_esquerda_1 = rota1.entregas[0] # adquiero los bins de las esquinas de esta entrega
                ponta_direita_1 = rota1.entregas[len(rota1.entregas)-1]

                roteiro_2 = bin2.rota
                rota2 = self.conteiner_rotas[roteiro_2]
                rota2_bin = self.conteiner_rotas_bins[roteiro_2]
                ponta_esquerda_2 = rota2.entregas[0]
                ponta_direita_2 = rota2.entregas[len(rota2.entregas)-1]

                if (roteiro_1 < roteiro_2):
                    roteiro_atual = roteiro_1
                    roteiro_absorvido = roteiro_2
                else:
                    roteiro_atual = roteiro_2
                    roteiro_absorvido = roteiro_1
                
                quantidade_clientes_no1 = rota1.total_clientes(conteiner_entregas_consolidadas)
                quantidade_clientes_no2 = rota2.total_clientes(conteiner_entregas_consolidadas)

                if (self.valida_volume_absorvido(cenario, econoItem, conteiner_entregas_consolidadas, binCap)):
                    #if ((quantidade_clientes_no1 + quantidade_clientes_no2) < qt_max_clientes):
                    if (self.valida_qt_rutas(bin1,bin2,cantidad_max_rutas_bsas,cantidad_max_rutas_arg)):
                        if (econoItem.distancia < raio_consolidacao):
                            if (self.valida_mistura_de_familias(1, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia)): #
                                if (roteiro_absorvido != roteiro_atual): # junta las rutas que no excedan la capacidad de un bin, que no excedan el radio y que no esten en la misma ruta
                                    noesquerdo_absorvido = self.conteiner_rotas[roteiro_absorvido].roteiro; # podria tomar directamente roteiro_absorvido (chequear)
                                    nodireito_absorvido = len(self.conteiner_rotas[roteiro_absorvido].entregas) - 1;
                                    noesquerdo_prevalece = self.conteiner_rotas[roteiro_atual].roteiro;
                                    nodireito_prevalece = len(self.conteiner_rotas[roteiro_atual].entregas) - 1;

                                    if ((roteiro_1 == ponta_esquerda_1 or roteiro_1 == ponta_direita_1) and (roteiro_1 == ponta_esquerda_2 or roteiro_1 == ponta_direita_2) or (roteiro_2 == ponta_esquerda_1 or roteiro_2 == ponta_direita_1) and (roteiro_2 == ponta_esquerda_2 or roteiro_2 == ponta_direita_2)):
                                        if (noesquerdo_prevalece == roteiro_1 or noesquerdo_prevalece == roteiro_2): # el enlace es con el nodo izquierdo
                                            if (noesquerdo_absorvido == roteiro_1 or noesquerdo_absorvido == roteiro_2): # izquierdo con izquierdo
                                                rota1.insert(0,rota2.entregas)
                                                rota1_bin.insere_entregas(rota2.entregas)
                                            elif (nodireito_absorvido == roteiro_1 or nodireito_absorvido == roteiro_2): # si es izquierdo con derecho
                                                rota1.insert(0,rota2.entregas)
                                        elif (nodireito_prevalece == roteiro_1 or nodireito_prevalece == roteiro_2): # si es con derecho
                                            if (noesquerdo_absorvido == roteiro_1 or noesquerdo_absorvido == roteiro_2): # derecho con izquierdo
                                                rota1.insert(len(rota2.entregas),rota2.entregas)
                                            elif (nodireito_absorvido == roteiro_1 or nodireito_absorvido == roteiro_2): # derecho con derecho
                                                rota1.insert(len(rota2.entregas),rota2.entregas)
                                        
                                        for binIndex in rota1.entregas: # notifico las cargas que fueran movidas a la nueva ruta de la nueva ruta asimilada
                                            conteiner_entregas_consolidadas[binIndex].rota = roteiro_atual

                                        for binIndex in rota2.entregas: # notifico las cargas que fueran movidas a la nueva ruta de la nueva ruta asimilada
                                            conteiner_entregas_consolidadas[binIndex].rota = roteiro_atual

        for entrega in conteiner_entregas_consolidadas: # barrida final, quien quedo solo se lo asigna a una nueva ruta
            # entrega[1] es la entrega
            if (entrega[1].rota == -1):
                roteiro = len(self.conteiner_rotas)
                entrega[1].rota = roteiro
                self.conteiner_rotas.append(cRota(roteiro))
                self.conteiner_rotas[roteiro].insere_entregas(entrega[1].lista_itens)

                self.conteiner_rotas_bins.append(cRota(roteiro))
                self.conteiner_rotas_bins[roteiro].insere_entregas(entrega[1])

    def valida_mistura_de_familias(self, cenario, econoItem, conteiner_entregas_consolidadas, matriz_compatibilidade_familia):
        bin1 = conteiner_entregas_consolidadas[econoItem.indiceBin1][1]
        bin2 = conteiner_entregas_consolidadas[econoItem.indiceBin2][1]
        
        if (cenario == 1): # ninguno de los bins asignados, bate bin x bin para ver compatibilidade
            familias_bin1 = conteiner_entregas_consolidadas[econoItem.indiceBin1][1].get_familias()
            for familia in familias_bin1:
                 if (familia == '#N/D') or not (conteiner_entregas_consolidadas[econoItem.indiceBin2][1].valida_mistura_de_familias(familia, matriz_compatibilidade_familia)):
                     return(False) # encontro alguna incompatibilid, paraliza y devuelve la incomptabilidad.
            return(True) # testeo todas y no dio ningun error
        if (cenario == 2): # Transporte 1 asignado, calcula compatibilidad de todas las familias de rota1 para bin2
            rota = self.conteiner_rotas[bin1.rota];
            for binIndex in rota.entregas:
                familias_bin = conteiner_entregas_consolidadas[binIndex].get_familias()
                for familia in familias_bin:
                    if (familia == '#N/D') or not (conteiner_entregas_consolidadas[econoItem.indiceBin2][1].valida_mistura_de_familias(familia, matriz_compatibilidade_familia)):
                        return(False) # encontro alguna incompatibilid, paraliza y devuelve la incomptabilidad.
            return (True)
        if (cenario == 3): # Transporte 2 asignado, calcula compatibilidad de todas las familias de rota2 para bin1
            rota = self.conteiner_rotas[bin2.rota];
            for binIndex in rota.entregas:
                familias_bin = conteiner_entregas_consolidadas[binIndex].get_familias()
                for familia in familias_bin:
                    if (familia == '#N/D') or not (conteiner_entregas_consolidadas[econoItem.indiceBin1][1].valida_mistura_de_familias(familia, matriz_compatibilidade_familia)):
                        return(False) # encontro alguna incompatibilid, paraliza y devuelve la incomptabilidad.
            return (True)
        if (cenario == 4): # ambos transportes asignados, calcula todos los items de remessa1 para todos los bins de transpote 2
            rota1 = self.conteiner_rotas[bin1.rota];
            rota2 = self.conteiner_rotas[bin2.rota];
            for binIndex_r1 in rota1.entregas:
                familias_bin_r1 = conteiner_entregas_consolidadas[binIndex_r1].get_familias()
                #p/cada familia de cada bin de la ruta 1, testear compatibilidad con todos los bins de la ruta 1
                for familia in familias_bin_r1:
                    for binIndex_r2 in rota2.entregas:
                        if (familia == '#N/D') or not (conteiner_entregas_consolidadas[binIndex_r2].valida_mistura_de_familias(familia, matriz_compatibilidade_familia)):
                            return(False) # encontro alguna incompatibilid, paraliza y devuelve la incomptabilidad.
            return (True)
        return(False)


    def valida_qt_rutas(self,bin1,bin2,cantidad_max_rutas_bsas,cantidad_max_rutas_arg):
        
        qt_rutas1 = bin1.soma_entregas()
        qt_rutas2 = bin2.soma_entregas()
        #qt_rutas1 = len(set(bin1.econoItem.indiceBin1[1][2]))
        #qt_rutas2 = len(set(bin2.econoItem.indiceBin2[1][2]))
        set_rutas1 = set(bin1.econoItem.indiceBin1[1][2])
        set_rutas2 = set(bin2.econoItem.indiceBin2[1][2])
                         
        if set_rutas1 in ('7AR004','7AR269') or set_rutas2 in ('7AR004', '7AR269'):
            qt_rutas_max = cantidad_max_rutas_bsas
        else:
            qt_rutas_max = cantidad_max_rutas_arg
        if qt_rutas1 + qt_rutas2 <= qt_rutas_max:
            return True
        else:
            return False
        

    def valida_volume_absorvido(self, cenario, econoItem, conteiner_entregas_consolidadas, binCap): #verifica se todos os itens da 1a bin entram na 2a bin
        bin1 = conteiner_entregas_consolidadas[econoItem.indiceBin1][1]
        roteiro_1 = bin1.rota
        bin2 = conteiner_entregas_consolidadas[econoItem.indiceBin2][1]
        roteiro_2 = bin2.rota
        
        bin1_buffer = copy.deepcopy(bin1) # para efectuar las operaciones de testeo
        bin2_buffer = copy.deepcopy(bin2) # para efectuar las operaciones de testeo
        if (cenario == 1): # puedo testear si el volumen es suficiente sumando los dos bins en un esquema de items bin2 -> bin1
            for item in bin1.lista_itens:
                if (bin2_buffer.testa_item_entra_cacamba(item, binCap)): # entra, insertar el item y seguir al proximo
                    bin2_buffer.lista_itens.append(item) # guardo el item en este nuevo bin
                else:
                   return(False)
            return(True)
        elif (cenario == 2): # rota1 ya definida, verificar todos los bins de ruta 1 + a bin2
            rota1 = self.conteiner_rotas[roteiro_1]
            for binIndex_r1 in rota1.entregas:
                for item in binIndex_r1:
                    if bin2_buffer.testa_item_entra_cacamba(item, binCap):
                        bin2_buffer.lista_itens.append(item)
                    else:
                        return(False)
            return(True)
        elif (cenario == 3): # ruta 2 ya definida pero bin1 no asignado
            rota2 = self.conteiner_rotas[roteiro_2] # obtengo la ruta2 que ya esta definida
            for binIndex_r2 in rota2.entregas:
                for item in binIndex_r2:
                    if bin1_buffer.testa_item_entra_cacamba(item, binCap):
                        bin1_buffer.lista_itens.append(item)
                    else:
                        return(False)
            return(True)
        elif (cenario == 4): #ambas
            # en las otras verificaba con el algoritmo implementado en testa_item_entra_cacamba.
            # en esta de aqui, Leandro hizo suma simple y directa. Como para llegar aqui el ajuste ya fue hecho en las otras, puede ser que sea adminisible.
            # pero creo que deberia sumar las dos rutas en un bin virtual y testear
            rota1 = self.conteiner_rotas[roteiro_1]
            rota2 = self.conteiner_rotas[roteiro_2] # obtiene la ruta2 que ya esta definida
            buffer_bin = libBins.cBin() # bin vacio

            for buffer_entrega in rota1.entregas: # meto todo de la ruta 1 en el
                for item in buffer_entrega:
                    if buffer_bin.testa_item_entra_cacamba(item, binCap):
                        buffer_bin.lista_itens.append(item)
                    else:
                        return(False)

            for buffer_entrega in rota2.entregas:
                for item in buffer_entrega:
                    if buffer_bin.testa_item_entra_cacamba(item, binCap):
                        buffer_bin.lista_itens.append(item)
                    else:
                        return(False)
            return(True)
        
    def dumpEconomiasCSV(self):
        print('nico')
        buffer = [] # buffer para escribir en el disco
        
        buffer.append(['ECONOMIA','BIN1','BIN2','DIST','CID#1','CID#2'])
        for entrega in self.conteiner_economias:
            buffer.append([str(entrega.economia), str(entrega.indiceBin1 + 1), str(entrega.indiceBin2 + 1), str(entrega.distancia), str(entrega.cidade1), str(entrega.cidade2)])

        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv

        print('nico')
        print(path+'economias.txt')
        with open(path + 'economias.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)

        print('nico')

    def dumpCKCSV(self):
        buffer = [] # buffer para grabar en el disco
        
        buffer.append(['ROTEIRO','ID ITEM','CLIENTE','FAM','FAM_MACRO','RUTA_ITEM','PESO'])
        for conteiner_entrega in self.conteiner_rotas:
            for entrega in conteiner_entrega.entregas:
                for item in entrega:
                    buffer.append([str(conteiner_entrega.roteiro), str(item.index), str(item.cliente), str(item.destino), str(item.familia), str(item.familia_macro), str(item.ruta_item), str(item.peso)])

        # hacer un output de conteiner_entregas_consolidadas para archivo CSV
        import csv

        with open(path + 'ck.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)

    def outputCKCSV(self):
        buffer = [] # buffer para grabar en el disco
        
        buffer.append(['CONTADOR','MASSA','NoS'])
        for conteiner_entrega in self.conteiner_rotas_bins:
            indexes = []
            carga = 0
            for entrega in conteiner_entrega.entregas:
                indexes.append(entrega.indice + 1)
                carga += entrega.get_carga() #TO DO posible bug, ver si debemos usar la carga real o la aparente
            buffer.append([str(conteiner_entrega.roteiro+1), str(carga)] + indexes)
        import csv
        with open(path + 'CK.txt', 'w') as myfile:
            wr = csv.writer(myfile, lineterminator='\n')
            for val in buffer:
                wr.writerow(val)

class cRota:
    def __init__(self, roteiro):
        self.roteiro = roteiro;
        self.entregas = []; # array con los indices de los bins de insere_entregas

    def insere_entregas(self, indiceBin):   # insertar las entregas del bin en esta ruta
        self.entregas.append(indiceBin)     # las entregas de este bin ahora son de esta ruta 

    def total_clientes(self, conteiner_entregas_consolidadas):      #cantidad de distintos clientes del bin 
        clientes = []
        for entrega in self.entregas:
            for item in entrega: #conteiner_entregas_consolidadas[entrega][1].lista_itens:
                clientes.append(item.cliente)
        return(len(set(clientes)))


class cEconomiaItem:
    def __init__(self, combo, matriz_distancia_cidades, v_cidade_usina):
        # combo es un par de valores de entregas oriundas de main.lista_bins.conteiner_entregas_consolidadas
        # o sea, combo[0/1] seran dos bins, con sus respectivos internos como lista_itens
        self.cidade1 = combo[0][1].lista_itens[0].ruta_item
        self.indiceBin1 = combo[0][1].indice
        self.cidade2 = combo[1][1].lista_itens[0].ruta_item
        self.indiceBin2 = combo[1][1].indice
        self.columna1 = matriz_distancia_cidades.columns.get_loc(self.cidade1)
        self.columna2 = matriz_distancia_cidades.columns.get_loc(self.cidade2)
        self.distancia = int(matriz_distancia_cidades.iloc[self.columna2-1][self.columna1])
        distancia_usina_cidade1 = int(matriz_distancia_cidades[v_cidade_usina][self.columna1-1]); # distancia entre usina y ciudad 1
        distancia_usina_cidade2 = int(matriz_distancia_cidades[v_cidade_usina][self.columna2-1]); # distancia entre usina y ciudad 1
        self.economia = distancia_usina_cidade1 + distancia_usina_cidade2 - self.distancia
        