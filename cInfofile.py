import pandas as pd

class cInfos(object):
    filename = 'input.xls'
    path = 'C:\\Users\\diegog1\\source\\repos\\Python Consolid8\\Python Consolid8\\data\\' #'data\\'

    def __init__(self):
        print('Abriendo archivo emitido por la macro PREPARA MODELO - INPUT.XLS')

        self.xl = pd.ExcelFile(type(self).path + type(self).filename)
        if (self.xl == 0):
            raise FileNotFoundError

        #cargo las dos pestañas de interés en el dataframes de panda
        self.df1 = self.xl.parse('InfosUnidades', header=None)
        self.df2 = self.xl.parse('txt', header=None)

    def seta_path(self, path): #Suministrar el path SIN BARRA FINAL
        self.path = path + '\\'
        
        
        
        
        