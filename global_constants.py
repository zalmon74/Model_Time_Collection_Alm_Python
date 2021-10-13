import numpy as np

# Вектор, который хранит в себе имена сигналов
ALL_SIGNALS = np.array(["L3OC", "L2SC", "L1SC", "L1OC"])
# Вектор, который хранит в себе номера строк
ALL_STRINGS = np.array([13, 16, 25, 31, 32, 50, 60])
# Значение, с которого начинается условный номер КА
NUM_CON_ALM = 700
# Условное значение, которое определяет, что данная строка не может передоваться
# в соот. сигнале
NOT_BEL_STR = 999999999
# Словарь, который содержит сопоставление индекса сигнала с его именем
DIC_IND_SIG_IN_NAME = {
                       0 : ALL_SIGNALS[0]
                      ,1 : ALL_SIGNALS[1]
                      ,2 : ALL_SIGNALS[2]
                      ,3 : ALL_SIGNALS[3]
                      }
# Словарь, который содержит сопоставление имени сигнала с его индексом
DIC_NAME_SIG_IN_IND = {
                       ALL_SIGNALS[0] : 0
                      ,ALL_SIGNALS[1] : 1
                      ,ALL_SIGNALS[2] : 2
                      ,ALL_SIGNALS[3] : 3
                      }
# Слорваь, который содержит сопоставление номера строки с индексом (по столб.)
# в матрице
DIC_NUM_STR_IN_IND = {
                      ALL_STRINGS[0] : 0
                     ,ALL_STRINGS[1] : 1
                     ,ALL_STRINGS[2] : 2
                     ,ALL_STRINGS[3] : 3
                     ,ALL_STRINGS[4] : 4
                     ,ALL_STRINGS[5] : 5
                     ,ALL_STRINGS[6] : 6  
                     }
# Слорваь, который содержит сопоставление индекса (по столб.) в матрице с
# номером строки
DIC_IND_STR_IN_STR = {
                      0 : ALL_STRINGS[0]
                     ,1 : ALL_STRINGS[1]
                     ,2 : ALL_STRINGS[2]
                     ,3 : ALL_STRINGS[3]
                     ,4 : ALL_STRINGS[4]
                     ,5 : ALL_STRINGS[5]
                     ,6 : ALL_STRINGS[6]  
                     }
# Словарь, который содержит сопоставление индекса строки со списокм индексов
# сигналов, которые не могут содержать данную строку
DIC_IND_STR_IN_IND_SIG_NOT_BEL = {
                                  DIC_NUM_STR_IN_IND[13] : [DIC_NAME_SIG_IN_IND["L3OC"], DIC_NAME_SIG_IN_IND["L1OC"]]
                                 ,DIC_NUM_STR_IN_IND[50] : [DIC_NAME_SIG_IN_IND["L3OC"], DIC_NAME_SIG_IN_IND["L1SC"], DIC_NAME_SIG_IN_IND["L2SC"]]
                                 }
                                 