import numpy as np

import global_constants as gc
import support_function as sf
import functions as f
import imitator_bink as ib

def main():

  count_sat = 24 # Количество КА в системе
  count_sig = 4  # Количество сигналов в каждом КА
  count_str = 7  # Количество строк в каждом сигнале
  # Количество сигналов у каждого КА
  vec_count_sig = [count_sig for _ in range(count_sat)]
  # Количество строк с ЭИ у каждого сигнала
  vec_count_str = [count_sig for _ in range(count_str)]

  # Формируем матрицу с доступными сигналами у каждого КА
  mat_av_sig_for_sat = sf.formation_matrix_units(count_sat, vec_count_sig)
  mat_av_str_for_sig = sf.formation_matrix_units(count_str, vec_count_str)
  # Заполняем матрицу параметром NOT_BEL_STR.
  for ind_sig in range(count_sig):
    for ind_str in range(count_str):
      if (gc.DIC_IND_STR_IN_IND_SIG_NOT_BEL.get(ind_str) == None):
        continue
      else:
        if (ind_sig in gc.DIC_IND_STR_IN_IND_SIG_NOT_BEL[ind_str]):
          mat_av_str_for_sig[ind_str, ind_sig] = gc.NOT_BEL_STR

  # Формируем ИД
  vec_seq, step_seq, max_seq, vec_l_psk, vec_t_oi, vec_t_as, \
  mat_t_str, mat_kps , mat_sync, mat_pps, mat_prior, mat_pvs = sf.formation_std_raw_data()

  # Формируем матрицу с объектами, которые хранят УИ-Н
  mat_mi_n = f.formation_mat_obj_mi_n(mat_av_sig_for_sat, vec_l_psk, vec_t_oi, vec_t_as
                                     ,vec_seq, step_seq, max_seq)
  # Формируем матрицу с объектами, которые хранят УИ-ЭпИ
  arr_mi_epi = f.formation_arr_obj_mi_epi(count_sat, mat_av_str_for_sig, mat_t_str
                                         ,mat_kps, mat_sync, mat_pps, mat_prior
                                         ,mat_pvs)
  ci = ib.imitator_bink(mat_mi_n, arr_mi_epi)
  f.save_ci_in_file(ci)

if (__name__) == ("__main__"):
  main()