# Точность для определения большой полуоси орбиты методом последовательных
# приблежений
EPS_A = 1.0e-06
# Точность для решения уравнения кеплера
EPS_E = 1.0e-09
# Путь до файлов с альманахом
PATH_ALM = "./../alm/"
# Имя файла с альманахом, который сейчас в системе
STD_NAME_ALM_FILE = "alm_17_07_2018_10_30_11_00_929_KA_24.txt"
# Ниже приведены индексы параметров для получения их списка после прочтения файла
IND_TIME_BEG = 0 # Время начала измерений 
IND_DAY_NA = 5 # Номер дня в четырехлетнем периоде
IND_COUNT_SAT = 6 # Количество КА в данном альманахе
IND_LET_FIRST = 9 # Номер литеры для первого НКА
IND_TA_LYM_FIRST = 10 # Время восходящего узла НКА
IND_TAU_N_FIRST = 11 
IND_LYMA_FIRST = 12 # Долгота восходящего узла НКА
IND_DIA_FIRST  = 13 # Поправка к сред. значению наклонения орбиты НКА
IND_OMA_FIRST  = 14 # Аргумент Перигея НКА
IND_EPSA_FIRST = 15 # Эксцентриситет орбиты НКА
IND_DTA_FIRST  = 16 # Поправка к среднему значению драконического периода обращения
IND_DDTA_FIRST = 17 # Половинная скорость изменения драконического периода
# Количество параметров в строке
COUNT_PAR_IN_STR = 9 