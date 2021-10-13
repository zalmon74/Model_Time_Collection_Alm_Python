from numpy import matrix, array, empty
from random import shuffle

import global_constants as gc

def formation_matrix_units(count_str: int, vec_count_units_for_str: list):
  """
  Функция формироваия матрицы, которая имеет размер count_str x global_constants.ALL_SIGNALS.size
  и в каждой строке содержит определенное кол-во единиц

  Вх. аргументы: 
    # count_str - количество строк в матрице
    # vec_count_units_for_str - количество единиц в соот. строке

  Вых. аргументы: 
    # mat_units - сформированная матрица
  """

  # Формируем список с 1 и 0 для формирования матрицы
  list_for_matr = []
  for i in range(count_str):
    # Заполнение списка 1
    list_temp = [1 for _ in range(vec_count_units_for_str[i])]
    # Вычисляем, сколько еще необходимо добавить 0 в список, если вычисленное
    # значение равно 0, то ничего не добавляем
    dif_len = abs(len(list_temp) - gc.ALL_SIGNALS.size)
    if (dif_len):
      list_temp = [*list_temp, *[0 for _ in range(dif_len)] ]
      # Перемешиываем список, чтобы не во всех строках в разных местах отсутств. 
      # единицы
      shuffle(list_temp)
    # Формируем общий список
    list_for_matr = [*list_for_matr, list_temp]

  # Формируем матрицу из списка
  mat_units = matrix(list_for_matr)
  return mat_units
  
def formation_vec_l_psk(start_len: int, step_len: int):
  """
  Функция формирования вектора с ИД, который характеризует размер ПСК для каждого
  сигнала.

  Вх. аргументы:
    # start_len - стартовый размер ПСК (не может быть < 3)
    # step_len  - шаг размера ПСК (не может быть < 0)

  Вых. аргументы: 
    # vec_l_psk - вектор, который хранит в себе разрмер ПСК для каждого сигнала.
                  Если стартовый размер не соот. входным данным, то объект будет
                  None
  """
  vec_l_psk = None
  if ((start_len >= 3) and (step_len >= 0)):
    vec_l_psk = [start_len+(i*step_len) for i in range(gc.ALL_SIGNALS.size)]
    vec_l_psk = array(vec_l_psk)
  return vec_l_psk

def formation_vec_t(start_val: int, step_val: int):
  """
  Функция формирования вектора с ИД, который характеризует интервал актуальности
  опред. параметра для каждого сигнала.

  Вх. аргументы: 
    # start_val - стартовое значение  (не может быть < 0)
    # step_val  - шаг по времени (не может быть < 0)

  Вых. аргументы:
    # vec_t - вектор с ИД, который характеризует интервал актуальности.
              Если не соот. входным условиями, то объет будет None 
  """
  vec_t = None
  if ((start_val >= 0) and (step_val >= 0)):
    vec_t = [start_val+(i*step_val) for i in range(gc.ALL_SIGNALS.size)]
    vec_t = array(vec_t)
  return vec_t

def formation_mat_raw_data(start_val: int, step_mat_str: int, step_mat_col: int, max_val = 9999999):
  """
  Функция формирования матриц для необходим. ИД

  Вх. аргументы:
    # start_val    - начальное значение (не может быть < 0)
    # step_mat_str - шаг по времени между строками матрицы (не может быть  < 0)
    # step_mat_col - шаг по времени между столбцами матрицы (не может быть  < 0)
    # max_val      - максимальное значение параметра 

  Вых. аргументы:
    # mat_output - сформированная матрица
                  Если не соот. входным условиями, то объет будет None
  """
  mat_output = empty([gc.ALL_STRINGS.size, gc.ALL_SIGNALS.size], dtype=int)
  if ((start_val >=0) and (step_mat_str >= 0) and (step_mat_col >= 0)): 
    # Цикл перебора строк
    for n_str in gc.ALL_STRINGS:
      # Получаем соот. индекс строки
      ind_str = gc.DIC_NUM_STR_IN_IND[n_str]
      # Получаем список, который содержит индексы сигналов, которые не имеют
      # данную строку
      list_not_bel_str = gc.DIC_IND_STR_IN_IND_SIG_NOT_BEL.get(ind_str)
      # Цикл по сигналами
      for n_sig in gc.ALL_SIGNALS:
        # Получаем соот. индекс сигнала
        ind_sig = gc.DIC_NAME_SIG_IN_IND[n_sig]
        # Проверяем, имеет ли данный сигнал данную строку, если нет, то записыв.
        # определенное число в данный элемент, иначе заполняем матрицу
        if ((list_not_bel_str != None) and (ind_sig in list_not_bel_str)):
          mat_output[ind_str, ind_sig] = gc.NOT_BEL_STR
        else:
          val = start_val+(ind_str*step_mat_str)+(ind_sig*step_mat_col)
          if (val > max_val):
            val -= max_val
          mat_output[ind_str, ind_sig] = val
  else:
    mat_output = None
  return mat_output

def formation_raw_data():
  """
  Функция формирования исходных данных для моделирования

  Вых. аргументы:
    ### Параметры для сигналов ###

    # vec_l_psk - Каждый эл. в данном векторе характеризует размер ПСК для соот. сигнала
    # vec_t_oi  - Каждый эл. в данном векторе характеризует интервал актуальности строк с ОИ
    # vec_t_as  - Каждый эл. в данном векторе характеризует интервал актуальности строк с АС

    ### Параметры для строк ###

    # mat_t_str - Матрица характеризует интервал актуальности строки опред. сигнала
    # mat_kps   - Матрица характеризует количество повторов строк для опред. сигнала
    # mat_sync  - Матрица характеризует значение синхронизации строки для опред. сигнала
    # mat_pps   - Матрица характеризует значение периода повторения строки для опред. сигнала
    # mat_prior - Матрица характеризует значение приоритета строки для опред. сигнала
    # mat_pvs   - Матрица характеризует порядок включения строки для опред. сигнала
  """
  # Начальные параметры для ИД
  start_l_psk = 14
  start_t_oi  = 0
  start_t_as  = 2000
  start_t_str = 0
  start_kps   = 11
  start_sync  = 0
  start_pps   = 0
  start_prior = 5
  start_pvs   = 0
  # Шаги для ИД
  step_l_psk = 1
  step_t_oi  = 0
  step_t_as  = 1000
  step_str_t_str = 200 ; step_col_t_str = 100 
  step_str_kps   = 10  ; step_col_kps   = 1 
  step_str_sync  = 3   ; step_col_sync  = 1 
  step_str_pps   = 3   ; step_col_pps   = 1
  step_str_prior = 10  ; step_col_prior = 2 
  step_str_pvs   = 0   ; step_col_pvs   = 0

  # Формируем ИД
  vec_l_psk = formation_vec_l_psk(start_l_psk, step_l_psk) 
  vec_t_oi  = formation_vec_t(start_t_oi, step_t_oi)
  vec_t_as  = formation_vec_t(start_t_as, step_t_as)
  mat_t_str = formation_mat_raw_data(start_t_str, step_str_t_str, step_col_t_str)
  mat_kps   = formation_mat_raw_data(start_kps, step_str_kps, step_col_kps)
  mat_sync  = formation_mat_raw_data(start_sync, step_str_sync, step_col_sync, 15)
  mat_pps   = formation_mat_raw_data(start_pps, step_str_pps, step_col_pps, 15)
  mat_prior = formation_mat_raw_data(start_prior, step_str_prior, step_col_prior)
  mat_pvs   = formation_mat_raw_data(start_pvs, step_str_pvs, step_col_pvs)

  return vec_l_psk, vec_t_oi, vec_t_as, \
         mat_t_str, mat_kps , mat_sync, mat_pps, mat_prior, mat_pvs

def formation_std_raw_data():
  """
  Функция формирования исходных данных, необходимых для моделирования при условии
  что:
    count_sat (КА в системе)                   = 24
    count_sig (кол-во сигналов у каждого КА)   =  4
    count_str (кол-во строк у каждого сигнала) =  7
  
  Порядок строк и сигналов след.
  сигналы: "L3OC", "L2SC", "L1SC", "L1OC"
  строки:  13, 16, 25, 31, 32, 50, 60

  Вых. агументы: 
    ### Параметры, которые формируются другой программой ###

    # vec_seq  - Вектор с последовательностью, которая была сформирована программой
    # step_seq - Шаг между последовательностями
    # max_seq  - Максимальное значение последовательности

    ### Параметры для сигналов ###

    # vec_l_psk - Каждый эл. в данном векторе характеризует размер ПСК для соот. сигнала
    # vec_t_oi  - Каждый эл. в данном векторе характеризует интервал актуальности строк с ОИ
    # vec_t_as  - Каждый эл. в данном векторе характеризует интервал актуальности строк с АС

    ### Параметры для строк ###

    # mat_t_str - Матрица характеризует интервал актуальности строки опред. сигнала
    # mat_kps   - Матрица характеризует количество повторов строк для опред. сигнала
    # mat_sync  - Матрица характеризует значение синхронизации строки для опред. сигнала
    # mat_pps   - Матрица характеризует значение периода повторения строки для опред. сигнала
    # mat_prior - Матрица характеризует значение приоритета строки для опред. сигнала
    # mat_pvs   - Матрица характеризует порядок включения строки для опред. сигнала
  """

  ## Данные ниже, берутся с другой программы (до след. ##)

  # Вектор с последовательностью, которая была сформирована программой
  vec_seq = array([4, 7, 2, 5, 8, 3, 6, 1, 7, 2, 5, 8, 3, 6, 1, 4, 8, 5, 2, 7, 4, 1, 6, 3])
  # Шаг между последовательностями
  step_seq = 3
  # Максимальное значение последовательности
  max_seq  = 8

  ## ИД для строк

  # Каждый эл. в данном векторе характеризует размер ПСК для соот. сигнала
  vec_l_psk = [14, 15, 16, 17]
  # Каждый эл. в данном векторе характеризует интервал актуальности строк с ОИ
  vec_t_oi = [0, 0, 0, 0]
  # Каждый эл. в данном векторе характеризует интервал актуальности строк с АС
  vec_t_as = [2000, 3000, 4000, 5000]
  # Каждый эл. в данной матрице характеризует интервал актуальности строки 
  # опред. сигнала
  mat_t_str = matrix(
                     [
                      [gc.NOT_BEL_STR, 0             , 0             , gc.NOT_BEL_STR]
                     ,[200           , 300           , 400           , 500           ]
                     ,[2000          , 3000          , 4000          , 5000          ]
                     ,[2000          , 3000          , 4000          , 5000          ]
                     ,[2000          , 3000          , 4000          , 5000          ]
                     ,[gc.NOT_BEL_STR, gc.NOT_BEL_STR, gc.NOT_BEL_STR, 200           ]
                     ,[20000         , 30000         , 40000         , 50000         ]
                     ]
                    )
  # Каждый эл. в данной матрице характеризует количество повторов строк для
  # соот. строке и определенного сигнала
  mat_kps = matrix(
                   [
                    [gc.NOT_BEL_STR, 12            , 13            , gc.NOT_BEL_STR]
                   ,[21            , 22            , 23            , 24            ]
                   ,[31            , 32            , 33            , 34            ]
                   ,[41            , 42            , 43            , 44            ]
                   ,[41            , 42            , 43            , 44            ]
                   ,[gc.NOT_BEL_STR, gc.NOT_BEL_STR, gc.NOT_BEL_STR, 64            ]
                   ,[71            , 72            , 73            , 74            ]
                   ]
                  )
  # Каждый эл. в данной матрице характеризует значение синхронизации для соот.
  # строке и определенного сигнала
  mat_sync = matrix(
                    [
                     [gc.NOT_BEL_STR, 1             , 2             , gc.NOT_BEL_STR]
                    ,[3             , 4             , 5             , 6             ]
                    ,[7             , 8             , 9             , 10            ]
                    ,[11            , 12            , 13            , 14            ]
                    ,[11            , 12            , 13            , 14            ]
                    ,[gc.NOT_BEL_STR, gc.NOT_BEL_STR, gc.NOT_BEL_STR, 4             ]
                    ,[5             , 6             , 7             , 8             ]
                    ]
                   )
  # Каждый эл. в данной матрице характеризует значение периода повторения строки
  # для соот. строке и определенного сигнала
  mat_pps = matrix(
                   [
                    [gc.NOT_BEL_STR, 1             , 2             , gc.NOT_BEL_STR]
                   ,[3             , 4             , 5             , 6             ]
                   ,[7             , 8             , 9             , 10            ]
                   ,[11            , 12            , 13            , 14            ]
                   ,[11            , 12            , 13            , 14            ]
                   ,[gc.NOT_BEL_STR, gc.NOT_BEL_STR, gc.NOT_BEL_STR, 0             ]
                   ,[5             , 6             , 7             , 8             ]
                   ]
                  )
  # Каждый эл. в данной матрице характеризует значение приоритета для 
  # соот. строке и определенного сигнала
  mat_prior = matrix(
                     [
                      [gc.NOT_BEL_STR, 6             , 5             , gc.NOT_BEL_STR]
                     ,[9             , 4             , 0             , 2             ]
                     ,[30            , 45            , 55            , 1             ]
                     ,[15            , 60            , 50            , 40            ]
                     ,[15            , 60            , 50            , 40            ]
                     ,[gc.NOT_BEL_STR, gc.NOT_BEL_STR, gc.NOT_BEL_STR, 8             ]
                     ,[6             , 4             , 2             , 0             ]
                     ]
                    )

  # Каждый эл. в данной матрице характеризует порядок включения для соот. строке
  # и определенного сигнала
  mat_pvs = matrix(
                   [
                    [gc.NOT_BEL_STR, 0             , 0             , gc.NOT_BEL_STR]
                   ,[0             , 0             , 0             , 0             ]
                   ,[0             , 0             , 0             , 0             ]
                   ,[0             , 0             , 0             , 0             ]
                   ,[0             , 0             , 0             , 0             ]
                   ,[gc.NOT_BEL_STR, gc.NOT_BEL_STR, gc.NOT_BEL_STR, 0             ]
                   ,[0             , 0             , 0             , 0             ]
                   ]
                  )

  return vec_seq  , step_seq, max_seq , \
         vec_l_psk, vec_t_oi, vec_t_as, \
         mat_t_str, mat_kps , mat_sync, mat_pps, mat_prior, mat_pvs
