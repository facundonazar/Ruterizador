class cClarkWright(object):
    import itertools
    """description of class"""

    #tendré un array con as N bins em main.lista_bins.conteiner_entregas_consolidadas
    #preciso hacer el ciclo por cada permutación posible

    self.conteiner_economias = [] #irá reter una lista de items del tipo cEconomiaItem

    def gera_combinacoes(self, conteiner_entregas_consolidadas):
        #bitmask = [1,1] + [0]*len(conteiner_entregas_consolidadas) #índice para permutações
        for combo in itertools.permutations(conteiner_entregas_consolidadas, 2):
            #aqui teremos combo[0,1] com cada combinação possível das entregas consolidadas
            #combo[0] e combo[1] trarão as respectivas entregas que deverão serem analisadas
            #a estrutura dessas entregas está definida em libBins, na rotina de ordenação best_f_decreasing
            recordEconomia = cEconomiaItem(combo)

            self.conteiner_economias.append(recordEconomia)
            pass
        pass

class cEconomiaItem:    
    def __init__(self, combo):
        #combo é um par de valores de entregas oriundas de main.lista_bins.conteiner_entregas_consolidadas
        self.economia = 0;
        self.cidade1 = -1;
        self.cidade2 = -1;
        self.distancia = 0;
        pass