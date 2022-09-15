#-Begin-----------------------------------------------------------------
'''
Este proyecto es el puerto de Consolid8 original, escrito en C++.
<<<DESCREVER DETALHADAMENTE APÓS 1o PROTÓTIPO>>>
'''
#-Includes--------------------------------------------------------------
import cMateriais
import cUnidades
import cInfofile
import libVeiculos, libItens, libBins
import libClarkWright


class cRoteirizador(object):
    def __init__(self):
        self.buffer_infos = cInfofile.cInfos() #objeto que retendrá los dataframes de las planillas de entrada, configuraciones de ambiente # -> VISTO
        self.info_unidades = cUnidades.cUnidades(self) # -> VISTO
        self.info_materiais = cMateriais.cMateriais(self) # -> VISTO
        self.info_veiculos = libVeiculos.cVeiculos(self) # -> VISTO
        self.lista_itens = libItens.cItens(self) #lista de items para rotar # -> VISTO
        self.lista_bins = libBins.cBinPack(self) # -> VISTO

    def inicializa(self):
        self.info_unidades.load_data()
        self.info_materiais.load_data_familia()
        self.info_materiais.load_data_macro_micro()
        self.info_veiculos.load_data()
        self.lista_itens.load_data()

def Main():
    roteirizador = cRoteirizador()
    print('Proyecto Consolid8 Python')
    print('Instanciando clases de proceso')
    try:
        roteirizador.inicializa()
        #---=== Fin de carga de datos de configuración ===---
        roteirizador.lista_bins.best_f_decreasing()
        #fazer um output da best decreasing para comparação, excel x excel
        #roteirizador.lista_bins.outputCSV();
        roteirizador.lista_bins.outputBPP();


        cw = libClarkWright.cRotasPack()
        cw.gera_combinacoes(roteirizador.lista_bins.conteiner_entregas_consolidadas, roteirizador.info_unidades.df_distancia_cidades, roteirizador.info_unidades.v_cidade_usina)
        #cw.dumpEconomiasCSV();
        cw.constroe_populacao(roteirizador.lista_bins.conteiner_entregas_consolidadas, roteirizador.info_veiculos.binCap, roteirizador.info_materiais.compatibilidade_familia, roteirizador.info_unidades.vraio_consolidacao, roteirizador.info_unidades.quantidade_clientes_maximo_rota)
        cw.outputCKCSV()

        #en este punto, tengo la lista organizada en lista de objetos del tipo cBin.
        #transformar eso en un pandas dataframe y exportar para eggs-cell.

        #for property, value in vars(lista_bins.conteiner_entregas_consolidadas[0][1].lista_itens[0]).keys().iteritems():
        #    print (property, ": ", value)
        #    buffer_df = PendingDeprecationWarning.DataFrame
    except:
        print(sys.exc_info()[0])
    else:
        pass
    finally:
        pass
#-Main------------------------------------------------------------------
if __name__ == "__main__":
    Main()

#-End-------------------------------------------------------------------