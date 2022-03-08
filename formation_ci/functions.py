from numpy import matrix, array, empty, full
import json
import datetime

import global_constants as gc
import structs

def formation_mat_obj_mi_n(mat_av_sig_for_sat: matrix, vec_l_psk: array 
                          ,vec_t_oi: array, vec_t_as: array, vec_seq: array
                          ,step_seq: int, max_seq: int):
  """
  Функция формирования матрицы с объектами типа УИ-Н

  Вх. аргументы:
    # mat_av_sig_for_sat - матрица, описывающая наличие опред. сигнала в соот. КА
    # vec_l_psk - вектор, который хранит в себе размер ПСК для каждого сигнала
    # vec_t_oi  - вектор, который хранит интервал актуальности строк с ОИ
    # vec_t_as  - вектор, который хранит интервал актуальности строк с АС
    # vec_seq   - вектор, который содержит номер последовательности для каждого КА
    # step_seq  - шаг по последовательностям
    # max_seq   - максимальное значение последовательности

  # Вых. аргументы:
    mat_mi_n - сформированная матрица
  """
  # Определяем количество КА и сигналов
  count_sat, count_sig = mat_av_sig_for_sat.shape
  # Формируем матрицу, которая будет содержать необходимые объекты
  mat_mi_n = empty([count_sat, count_sig], dtype=structs.STRUCT_MI_N)
  # Цикл перебора КА
  for ind_sat in range(count_sat):
    # Цикл перебора сигналов в каждом КА
    for ind_sig in range(count_sig):
      # Проверяем, что данный сигнал доступен для данного КА, если не доступен
      # то переходим к следующему
      if (mat_av_sig_for_sat[ind_sat, ind_sig] == 1):
        mat_mi_n[ind_sat, ind_sig] = structs.STRUCT_MI_N(ind_sat+1, ind_sat+1+gc.NUM_CON_ALM
                                                        ,ind_sig, gc.DIC_IND_SIG_IN_NAME[ind_sig]
                                                        ,count_sat, vec_l_psk[ind_sig]
                                                        ,vec_t_oi[ind_sig], vec_t_as[ind_sig]
                                                        ,full(63, gc.NOT_BEL_STR))
        # Формируем последовательность передачи альманаха
        vec_seq_alm = get_seq_alm(count_sat, ind_sat, count_sig, ind_sig
                                 ,vec_seq, step_seq, max_seq)
        mat_mi_n[ind_sat, ind_sig].vec_n_as[:count_sat] = vec_seq_alm[:]
      else:
        continue
  return mat_mi_n

def get_seq_alm(count_sat: int, ind_sat: int, max_count_sig: int, ind_sig: int
               ,vec_seq: array, step_seq: int, max_seq: int):
  """
  Функция формирования последовательности передачи альманаха для соот. КА и сиг.
  В данной версии программы утверждаем, что сигналы L1OC и L3OC в одной группе и
  сигналы L1SC и L2SC в другой группе.

  Вх. аргументы:
    # count_sat - количество КА
    # ind_sat   - индекс тек. КА
    # count_sig - максимальное количество сигналов
    # ind_sig   - индекс текущего сигнала
    # vec_seq   - вектор с последовательностями
    # step_seq  - шаг по последовательностям
    # max_seq   - максимальное значение последовательности
  
  Вых. аргументы:
    # vec_seq_alm - последовательность передачи альманаха для данного КА и сиг.
  """
  base = None
  vec_seq_alm = None 
  # Формируем последовательности альманаха
  # Принцип следующий: берем номер последовательности соот. КА и умножаем его
  # на шаг - это будет индекс первого КА, альманах которого будет передоваться
  # затем вектор достраивается, путем инкрементирования значения, до количества
  # КА. После чего формируется второй вектор, который содержит индексы от 0 до
  # вычисленного на первом шаге
  if (ind_sig == gc.DIC_NAME_SIG_IN_IND["L1OC"]) or \
     (ind_sig == gc.DIC_NAME_SIG_IN_IND["L1SC"]):
    first_base  = list(range(vec_seq[ind_sat]*step_seq-1, count_sat))
    second_base = list(range(vec_seq[ind_sat]*step_seq-1))
    base = array([*first_base, *second_base])
  elif (ind_sig == gc.DIC_NAME_SIG_IN_IND["L2SC"]) or \
       (ind_sig == gc.DIC_NAME_SIG_IN_IND["L3OC"]):
    # Если сигналы находится в одной группе, то они сдвигаются на половину
    # кол-во КА
    start = int(vec_seq[ind_sat]*step_seq+count_sat/2*step_seq-1)
    while ((start > (count_sat - 1)) and (count_sat > 1)):
      start -= (count_sat - 1)
      start = int(start)
    first_base  = list(range(start, count_sat))
    second_base = list(range(start))
    base = array([*first_base, *second_base])
  return base

def formation_arr_obj_mi_epi(count_sat: int, mat_av_str_for_sig: matrix
                            ,mat_t_oi: matrix, mat_kps: matrix, mat_sync: matrix
                            ,mat_pps: matrix, mat_prior: matrix, mat_pvs: matrix):
  """
  Функция формирования массива с объектами типа УИ-ЭпИ

  Вх. аргументы:
    # count_sat - кол-во КА
    # mat_av_str_for_sig - матрица, описывающая наличие опред. строки в соот. сигнале
    # mat_t_oi  - матрица с интервалом актуальности
    # mat_kps   - матрица с количеством повторов строк
    # mat_sync  - матрица с синхронизациями строк
    # mat_pps   - матрица с периодом повторения строк
    # mat_prior - матрица с приоритетами строк
    # mat_pvs   - матрица с порядком включения строк

  # Вых. аргументы:
    # arr_mi_epi - сформированная матрица
  """
  # Определяем кол-во строк и сигналов
  count_str, count_sig = mat_av_str_for_sig.shape
   # Формируем матрицу, которая будет содержать необходимые объекты
  arr_mi_epi = empty([count_sat, count_str, count_sig], dtype=structs.STRUCT_MI_EPI)
  # Цикл перебора КА
  for ind_sat in range(count_sat):
    # Цикл перебора строк
    for ind_str in range(count_str):
      # Цикл перебора сигналов
      for ind_sig in range(count_sig):
        # Если строка для данного сигнала не может существовать, то идем дальше
        if (mat_av_str_for_sig[ind_str, ind_sig] == gc.NOT_BEL_STR):
          continue
        arr_mi_epi[ind_sat, ind_str, ind_sig] = structs.STRUCT_MI_EPI(
                                                                      ind_sat+1
                                                                     ,ind_sat+1+gc.NUM_CON_ALM
                                                                     ,gc.DIC_IND_STR_IN_STR[ind_sig]
                                                                     ,ind_sig
                                                                     ,gc.DIC_IND_SIG_IN_NAME[ind_sig]
                                                                     ,mat_t_oi[ind_str, ind_sig]
                                                                     ,mat_kps[ind_str, ind_sig]
                                                                     ,mat_sync[ind_str, ind_sig]
                                                                     ,mat_pps[ind_str, ind_sig]
                                                                     ,mat_prior[ind_str, ind_sig]
                                                                     ,mat_pvs[ind_str, ind_sig]
                                                                     )
  return arr_mi_epi

def save_ci_in_file(ci):
  """
  Функция сохранения ЦИ в файл типа json.

  Вх. аргументы:
    # ci - ЦИ, которую необходимо записать
  """
  time = datetime.datetime
  path_file = gc.PATH_TO_CI_FILE+"ci_"+time.today().strftime('%Y_%m_%d_%H_%M_%S')+".json"
  with open(path_file, "w", encoding=gc.ENCODING_FOR_FILE) as file:
    json.dump(ci, file, indent=2) 