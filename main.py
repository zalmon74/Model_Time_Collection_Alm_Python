import numpy as np

import support_function as sf

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

  print(f"{mat_av_sig_for_sat=}")
  print(mat_av_str_for_sig)


if (__name__) == ("__main__"):
  main()