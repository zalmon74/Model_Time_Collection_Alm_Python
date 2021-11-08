import math
import time
import datetime
from pathlib import Path 
from re import split
from json import dump, load, JSONDecodeError

from numpy import array

import global_constants as gc

def calcultion_coor_alm_glo(ti, n, na, ta_lym, dta, ddta, lyma, oma, epsa, dia):
  """
  Функция расчета координат и скоростей КА по данным альманаха.
  Метод расчета взят из ИКД 2016 г. для кодовых сигналов 

  Вх. аргументы:
    # ti - момент времени, на который необходимо рассчитать координаты КА в сек.
    # n  - номер суток внутри четырехлетнего периода, на которых необходимо
           рассчитать координаты КА
    # na - календарный номер суток по шкале МДВ внутри четырехлетнего интервала,
          передаваемый НКА в составе неоперативной информации
    # ta_lym - время восходящего узла КА в сек.
    # dta  - поправка к среднему значению драконического периода обращения в сек.
    # ddta - половинная скорость изменения драконического периода
    # lyma - долгота восходящего узла в полуциклах
    # oma  - аргумент перигея орбиты на момент времени ta_lym в полуциклах
    # epsa - эксцентриситет орбиты НКА на момент времени ta_lym в полуциклах
    # dia  - поправка к среднему значению наклонения орбиты в полуциклах

  Вых. аргументы: 
    # coor  - расчитанные координаты КА в км.
    # speed - расчитанные сокрости КА в км/c.
  """

  # Константы
  I_CR = 63 # Среднее наклонение орбит в град. (для CD = 63, OF = 64.8)
  T_CR = 43200 # Драконический период обращения в с. (для CD = 43200, OF = 40544)
  GM   = 398600.441 # Гравитационное поле Земли км3/с2
  A_E  = 6378.136 # Экваториальный радиус Земли в км.
  OM_Z = 7.2921150e-5 # Угловая скорость вращения Земли в рад/с
  # Коэффициент при второй зональной гармонике разложения геопотенциала в ряд
  # по сферическим функциям
  J0_2 = 1082.62575e-6 
  MU = 398600.4418

  # 1
  d_na = n-na-round((n-na)/1461)*1461
  d_tpr = d_na*86400+(ti-ta_lym)

  # 2
  w = d_tpr//(T_CR+dta)

  # 3
  i = (I_CR/180+dia)*math.pi

  # 4
  t_dr = T_CR+dta+(2*w+1)*ddta
  n = 2*math.pi/t_dr

  # 5 
  t_osk = t_dr
  am = 0
  a = 1
  while (abs(a-am) >= gc.EPS_A):
    am = a
    a = (((t_osk/(2*math.pi)))**2*GM)**(1/3)
    p=a*(1-epsa**2)
    t_osk = t_dr/(1-3/2*J0_2*(A_E/p)**2*((2-5/2*math.sin(i)**2)*((1-epsa**2)**\
            (3/2)/((1+epsa*math.cos(oma*math.pi))**2))+((1+epsa*\
            math.cos(oma*math.pi))**3/(1-epsa**2))))
  
  # 6
  lym = lyma*math.pi-(OM_Z+3/2*J0_2*n*(A_E/p)**2*math.cos(i))*d_tpr
  om = oma*math.pi-3/4*J0_2*n*(A_E/p)**2*(1-5*math.cos(i)**2)*d_tpr

  # 7
  e0 = -2*math.atan(math.sqrt((1-epsa)/(1+epsa))*math.tan(om/2))
  l1 = om+e0-epsa*math.sin(e0)

  # 8 
  l_u = [l1]
  l_u.append(l1+n*(d_tpr-(T_CR+dta)*w-ddta*w**2))

  # 9
  h = epsa*math.sin(om)
  l = epsa*math.cos(om)
  b = 3/2*J0_2*(A_E/a)**2
  
  dela   = [0 for _ in range(len(l_u))]
  delh   = [0 for _ in range(len(l_u))]
  dell   = [0 for _ in range(len(l_u))]
  dellym = [0 for _ in range(len(l_u))]
  deli   = [0 for _ in range(len(l_u))]
  dell_u = [0 for _ in range(len(l_u))]

  for k in range(len(l_u)):

    a_1 = 2*b*(1-3/2*math.sin(i)**2)
    a_2 = l*math.cos(l_u[k])+h*math.sin(l_u[k])
    a_3 = 1/2*h*math.sin(l_u[k])-1/2*l*math.cos(l_u[k])+math.cos(2*l_u[k])+\
          7/2*l*math.cos(3*l_u[k])+7/2*h*math.sin(3*l_u[k])
    dela[k] = (a_1*a_2+b*math.sin(i)**2*a_3)*a

    h_1 = b*(1-3/2*math.sin(i)**2);
    h_2 = math.sin(l_u[k])+3/2*l*math.sin(2*l_u[k])-3/2*h*math.cos(2*l_u[k])
    h_3 = math.sin(l_u[k])-7/3*math.sin(3*l_u[k])+5*l*math.sin(2*l_u[k])-17/2*\
          l*math.sin(4*l_u[k])+17/2*h*math.cos(4*l_u[k])+h*math.cos(2*l_u[k])
    h_4 = -1/2*b*math.cos(i)**2*l*math.sin(2*l_u[k])
    delh[k] = h_1*h_2-1/4*b*math.sin(i)**2*h_3+h_4

    l_1 = b*(1-3/2*math.sin(i)**2);
    l_2 = math.cos(l_u[k])+3/2*l*math.cos(2*l_u[k])+3/2*h*math.sin(2*l_u[k]);
    l_3 = -math.cos(l_u[k])-7/3*math.cos(3*l_u[k])-5*h*math.sin(2*l_u[k])-\
          17/2*l*math.cos(4*l_u[k])-17/2*h*math.sin(4*l_u[k])+l*math.cos(2*l_u[k])
    l_4 = 1/2*b*math.cos(i)**2*h*math.sin(2*l_u[k])
    dell[k] = l_1*l_2-1/4*b*math.sin(i)**2*l_3+l_4

    lym_1 = 7/2*l*math.sin(l_u[k])-5/2*h*math.cos(l_u[k])-1/2*math.sin(2*l_u[k])-\
            7/6*l*math.sin(3*l_u[k])+7/6*h*math.cos(3*l_u[k])
    dellym[k] = -b*math.cos(i)*lym_1

    i_1 = -l*math.cos(l_u[k])+h*math.sin(l_u[k])+math.cos(2*l_u[k])+7/3*l*\
          math.cos(3*l_u[k])+7/3*h*math.sin(3*l_u[k])
    deli[k] = 1/2*b*math.sin(i)*math.cos(i)*i_1

    l_1 = 2*b*(1-3/2*math.sin(i)**2)*(7/4*l*math.sin(l_u[k])-7/4*h*math.cos(l_u[k]))
    l_2 = -7/24*h*math.cos(l_u[k])-7/24*l*math.sin(l_u[k])-49/72*h*\
          math.cos(3*l_u[k])+49/72*l*math.sin(3*l_u[k])+1/4*math.sin(2*l_u[k])
    l_3 = 7/2*l*math.sin(l_u[k])-5/2*h*math.cos(l_u[k])-1/2*math.sin(2*l_u[k])-\
          7/6*l*math.sin(3*l_u[k])+7/6*h*math.cos(3*l_u[k])
    dell_u[k] = l_1+3*b*math.sin(i)**2*l_2+b*math.cos(i)**2*l_3

  # Проверка dell_u
  a_= a+dela[1]-dela[0]
  h_= h+delh[1]-delh[0]
  l_= l+dell[1]-dell[0]
  i_= i+deli[1]-deli[0]
  lym_ = lym+dellym[1]-dellym[0]
  eps_ = math.sqrt(h_**2+l_**2)
  om_ = math.atan2(h_, l_)
  l_ = l_u[1]+dell_u[1]-dell_u[0]

  # 10
  e1 = 0
  e = l_-om_

  while (abs(e-e1) >= gc.EPS_E):    
    e1 = e
    e = l_-om_+eps_*math.sin(e1)

  # 11
  v = 2*math.atan(math.sqrt((1+eps_)/(1-eps_))*math.tan(e/2))
  u = v+om_

  # 12
  p = a_*(1-eps_**2)
  r = p/(1+eps_*math.cos(v))
  coor = [0 for _ in range(3)]
  coor[0] = r*(math.cos(lym_)*math.cos(u)-math.sin(lym_)*math.sin(u)*math.cos(i_))
  coor[1] = r*(math.sin(lym_)*math.cos(u)+math.cos(lym_)*math.sin(u)*math.cos(i_))
  coor[2] = r*math.sin(u)*math.sin(i_)

  # 13
  v_r = math.sqrt(MU/p)*eps_*math.sin(v)
  v_u = math.sqrt(MU/p)*(1+eps_*math.cos(v))

  speed = [0 for _ in range(3)]

  v_1_1 = math.cos(lym_)*math.cos(u)-math.sin(lym_)*math.sin(u)*math.cos(i_)
  v_1_2 = math.cos(lym_)*math.sin(u)+math.sin(lym_)*math.cos(u)*math.cos(i_)
  speed[0] = v_r*v_1_1-v_u*v_1_2+OM_Z*coor[1]

  v_2_1 = math.sin(lym_)*math.cos(u)+math.cos(lym_)*math.sin(u)*math.cos(i_)
  v_2_2 = math.sin(lym_)*math.sin(u)-math.cos(lym_)*math.cos(u)*math.cos(i_)
  speed[1] = v_r*v_2_1-v_u*v_2_2-OM_Z*coor[0]

  speed[2] = v_r*math.sin(u)*math.sin(i_)+v_u*math.cos(u)*math.sin(i_)

  return coor, speed

def read_my_alm_file(name_file):
  """
  Функция чтения файла с альманахом

  Вх. аргументы:
    # name_file - имя файла с альманахом, который необходимо считать

  Вых. аргументы:
    # time_beg - Время начала измерений 
    # na - Номер дня в четырехлетнем периоде
    # count_sat - Количество КА
    # l_lett - список литерами для НКА
    # l_ta_lym - список времен с восходящими узлами для НКА
    # l_tau_n - 
    # l_lyma - список с долготами восходящих узлов НКА
    # l_dia - список с поправками к сред. значению наклонения орбиты НКА
    # l_oma - список с аргументами Перигея НКА
    # l_eps - список с эксцентриситетами орбит НКА
    # l_dta - список с поправками к среднему значению драконического периода обращения
    # l_ddta - список с половинными скоростями изменения драконического периода
  """
  # Считываем с файла все строки
  with open(name_file, "r") as file:
    text_in_file = file.read()
  # Формируем из строк список
  list_text_in_file = split(" |\n", text_in_file)
  # Удаляем все пустые строки в списке
  while ("" in list_text_in_file):
    list_text_in_file.remove("")
  # Вытаскиваем данные из списка и переводим время из часов в сек.
  time_beg = float(list_text_in_file[gc.IND_TIME_BEG])*3600
  na = int(list_text_in_file[gc.IND_DAY_NA])
  count_sat = int(list_text_in_file[gc.IND_COUNT_SAT])
  # Списки для хранения данных по КА
  l_lett = [] # Литеры для НКА
  l_ta_lym = [] # Время восходящего узла НКА
  l_tau_n = [] 
  l_lyma = [] # Долгота восходящего узла НКА
  l_dia = [] # Поправка к сред. наклонению орбиты НКА
  l_oma = [] # Аргумент Перигея НКА
  l_eps = [] # Эксцентриситет орбиты НКА
  l_dta = [] # Поправка к среднему значению драконического периода обращения
  l_ddta = [] # Половинная скорость изменения драконического периода
  # Цикл по КА
  for ind_sat in range(count_sat):
    l_lett.append(int(list_text_in_file[gc.IND_LET_FIRST+ind_sat*gc.COUNT_PAR_IN_STR]))
    l_ta_lym.append(float(list_text_in_file[gc.IND_TA_LYM_FIRST+ind_sat*gc.COUNT_PAR_IN_STR]))
    l_tau_n.append(float(list_text_in_file[gc.IND_TAU_N_FIRST+ind_sat*gc.COUNT_PAR_IN_STR]))
    l_lyma.append(float(list_text_in_file[gc.IND_LYMA_FIRST+ind_sat*gc.COUNT_PAR_IN_STR]))
    l_dia.append(float(list_text_in_file[gc.IND_DIA_FIRST+ind_sat*gc.COUNT_PAR_IN_STR]))
    l_oma.append(float(list_text_in_file[gc.IND_OMA_FIRST+ind_sat*gc.COUNT_PAR_IN_STR]))
    l_eps.append(float(list_text_in_file[gc.IND_EPSA_FIRST+ind_sat*gc.COUNT_PAR_IN_STR]))
    l_dta.append(float(list_text_in_file[gc.IND_DTA_FIRST+ind_sat*gc.COUNT_PAR_IN_STR]))
    l_ddta.append(float(list_text_in_file[gc.IND_DDTA_FIRST+ind_sat*gc.COUNT_PAR_IN_STR]))
  return time_beg, na, count_sat, l_lett, l_ta_lym, l_tau_n, l_lyma, l_dia,\
         l_oma, l_eps, l_dta, l_ddta

def read_file_di(path_file: str):
  """
  Функция чтения файла, который содержит ЦИ.

  Вх. аргументы:
    # path_file - путь до файла с ЦИ

  # Вых. аргументы:
    # dic_ci - считанный словарь с ЦИ
  """
  try: # Считываем содержимое файла
    with open(path_file, "r", encoding="utf-8") as file:
      dic_ci = load(file)
  # Если файл отсутствует, то возвращаем None
  except (FileNotFoundError, JSONDecodeError):
    dic_ci = None 
  return dic_ci

def blh2xyz(coor_blh: tuple, a: float = gc.R_EARTH, ex: float = gc.E_EARTH):
  """
  Функция перевода координат из геодезической СК в геоцентрическую СК.

  Вх. аргументы:
    # coor_blh - кортеж с координатами в геодезической СК ([0] - широта
                                                           [1] - долгота
                                                           [2] - высота) в рад.
    # a  - радиус Земли
    # ex - эксцентриситет Земли

  Вых. аргументы:
    # coor_xyz - кортеж с координатами в геоцентрической СК 
  """
  # Переводим в рад.
  B, L, H = coor_blh
  N = a/math.sqrt(1-ex**2*math.sin(B))
  X = (N+H)*math.cos(B)*math.cos(L)
  Y = (N+H)*math.cos(B)*math.sin(L)
  Z = ((1-ex**2)*N+H)*math.sin(B)
  return (X, Y, Z)

def calculation_um(coor_sat, coor_pos):
  """
  Функция расчета угла места между КА и тек. позицией

  Вх. аргументы:
    # coor_sat - координаты КА
    # coor_pos - координаты антенны, которая принимает альманах

  Вых. аргументы:
    # um - рассчитанный УМ в град.
  """
  rang = math.sqrt((coor_sat[0] - coor_pos[0])**2+\
                   (coor_sat[1] - coor_pos[1])**2+\
                   (coor_sat[2] - coor_pos[2])**2)
  kx = (coor_sat[0]-coor_pos[0])/rang
  ky = (coor_sat[1]-coor_pos[1])/rang
  kz = (coor_sat[2]-coor_pos[2])/rang
  um = math.asin((kx*coor_pos[0]+ky*coor_pos[1]+kz*coor_pos[2])/\
                  math.sqrt(coor_pos[0]**2+coor_pos[1]**2+coor_pos[2]**2))*180/math.pi
  return um

def formation_dict_f_receiv_alm(count_sat):
  """
  Функция создания словарь, который будет след. типа:
  dict = {(lat, lon) : array(Bool(range(count_sat)))}
  lat - значение широты
  lon - значение долготы
  array(range(count_sat, Bool)) - вектор, который хранит в себе флаг принятия
                                  альманаха для конкретного КА

  Вх. аргументы:
    # count_sat - количество КА
  Вых. аргументы:
    # form_dic - сформированный словарь
  """
  list_for_dic = [False for _ in range(count_sat)]
  from_dic = {}
  # Цикл по широте
  for lat in range(gc.START_LATITUDE, gc.END_LATITUDE, gc.STEP_LATITUDE):
    # Цикл по долготе
    for lon in range(gc.START_LONGITUDE, gc.END_LONGITUDE, gc.STEP_LONGITUDE):
      from_dic[(lat, lon)] = array(list_for_dic)
  return from_dic

def formation_dict_time_rec_alm():
  """
  Функция создания словаря, который будет след. типа
  dict = {(lat, lon) : int(time)}
  lat - значение широты
  lon - значение долготы
  time - текущее время приема полного альманаха

  Вых. аргументы:
    # from_dic - сформированный словарь
  """
  from_dic = {}
  # Цикл по широте
  for lat in range(gc.START_LATITUDE, gc.END_LATITUDE, gc.STEP_LATITUDE):
    # Цикл по долготе
    for lon in range(gc.START_LONGITUDE, gc.END_LONGITUDE, gc.STEP_LONGITUDE):
      from_dic[(lat, lon)] = 0
  return from_dic

def formation_dict_list_time_rec_alm():
  """
  Функция создания словарь, который будет след. типа
  dict = {(lat, lon) : []}
  lat - значение широты
  lon - значение долготы
  [] - пустой список, который будет содержать времена приема полного альманаха

  Вых. аргументы:
    # from_dic - сформированный словарь
  """
  from_dic = {}
  # Цикл по широте
  for lat in range(gc.START_LATITUDE, gc.END_LATITUDE, gc.STEP_LATITUDE):
    # Цикл по долготе
    for lon in range(gc.START_LONGITUDE, gc.END_LONGITUDE, gc.STEP_LONGITUDE):
      from_dic[(lat, lon)] = []
  return from_dic

def modeling_receiv_alm():
  """
  Функция моделирования принятия альманаха.
  """
  # Формируем словарь, который будет содержать время приема текущего альманаха
  # для каждой точки
  dic_time_rec_alm = formation_dict_time_rec_alm()
  # Формируем словарь, который будет содержать список времен приема полного
  # альманаха
  dic_list_time_rec_alm = formation_dict_list_time_rec_alm()
  # Формируем имя файла с ЦИ
  path_file_di = gc.PATH_DI_FILE
  # Считываем ЦИ с файла
  dic_ci = read_file_di(path_file_di)
  # Если такого файла нет или он пустой, то сообщаем об этом
  if (dic_ci == None):
    raise Exception(f"Файлс с ЦИ ({path_file_di}) отсутствует или пуст")
  # Считываем альманах с файла
  tup_alm = read_my_alm_file(gc.PATH_ALM+gc.STD_NAME_ALM_FILE)
  # Формируем словарь, который будет содержать флаги принятия альманаха для соот.
  # точки
  dic_f_receiv_alm = formation_dict_f_receiv_alm(tup_alm[2])
  # Основной цикл по времени
  for time in range(gc.TIME_MODELING):
    # Цикл по широте
    for lat in range(gc.START_LATITUDE, gc.END_LATITUDE, gc.STEP_LATITUDE):
      # Цикл по долготе
      for lon in range(gc.START_LONGITUDE, gc.END_LONGITUDE, gc.STEP_LONGITUDE):
        modeling_receiv_alm_one_point(time, tup_alm
                                     ,(lat, lon), dic_ci
                                     ,dic_f_receiv_alm[(lat, lon)]
                                     ,dic_time_rec_alm, dic_list_time_rec_alm)
  # Сохраняем полученный словарь в файл
  path_name_save_dic = gc.PATH_LIST_TIME_REC_ALM
  save_res_dic_in_file(path_name_save_dic, dic_list_time_rec_alm)

def modeling_receiv_alm_one_point(time: int, tup_alm: tuple
                                 ,tup_coor_point: tuple, dic_ci: dict
                                 ,vec_f_receiv_alm: array, dic_time_rec_alm: dict
                                 ,dic_list_time_rec_alm: dict):
  """
  Функция моделирования принятия альманаха в одной точке на один момент времени

  Вх. аргументы:
    # time - текущее время
    # tup_alm - кортеж, который хранит альманах
    # tup_coor_point - котреж с текущими координатами в град
    # dic_ci - словарь, который содержит ЦИ для всех КА и сигналов
    # vec_f_receiv_alm - вектор, который будет содержать флаги принятия
                         альманаха для соот. КА для соот. точки на карте
    # dic_time_rec_alm - словарь, который будет содержать время приема текущего
                         альманаха для каждой точки
    # dic_list_time_rec_alm - словарь, который будет содержать список времен
                              приема полного альманаха
  """
  coor_point = blh2xyz((tup_coor_point[0]*math.pi/180, tup_coor_point[1]*math.pi/180, gc.HEIGHT_POS))
  # Определяем видимые КА
  list_vis_sat = definition_visible_sat(time, tup_alm, coor_point)
  # Заполняем вектор с переданными строками альманаха
  passing_str(time, list_vis_sat, dic_ci, vec_f_receiv_alm)
  # Определяем приняли ли в данной точке полный альманах
  f_full_alm = not(False in vec_f_receiv_alm)
  # Если альманах принят полностью, то добавляем полученное время в соот. список
  # из словаря, а также обнуляем это время и устанавливаем в False флаги
  # принятия альманха
  if (f_full_alm):
    dic_list_time_rec_alm[tup_coor_point].append(dic_time_rec_alm[tup_coor_point])
    dic_time_rec_alm[tup_coor_point] = 0
    vec_f_receiv_alm[:] = False
  else: # Инкрементируем время приема полного альманаха
    dic_time_rec_alm[tup_coor_point] += 1
  
def definition_visible_sat(time: int, tup_alm: tuple
                          ,coor_point: tuple):
  """
  Функция определения видимых КА в определенной точке.

  Вх. аргументы:
    # time - текущее время
    # tup_alm - кортеж, который хранит альманах
    # tup_coor_point - котреж с текущими координатами в рад
  
  Вых. аргументы:
    # vis_sat - список в видимыми КА
  """
  # Список, который будет содежрать номера КА, который видны в данной точке
  vis_sat = []
  # Цикл перебора КА для определения их видимости
  for ind_sat in range(tup_alm[2]):
    num_sat = ind_sat+1
    # Рассчитываем координаты
    coor_sat, speed_sat = calcultion_coor_alm_glo(time+tup_alm[0], tup_alm[1]+1
                                                 ,tup_alm[1], tup_alm[4][ind_sat]
                                                 ,tup_alm[10][ind_sat]
                                                 ,tup_alm[11][ind_sat]
                                                 ,tup_alm[6][ind_sat]
                                                 ,tup_alm[8][ind_sat]
                                                 ,tup_alm[9][ind_sat]
                                                 ,tup_alm[7][ind_sat])
    # Рассчитываем УМ между КА и тек. позицией
    um = calculation_um(coor_sat, coor_point)
    # Если КА видим, то добавлем его в список
    if (um > gc.MIN_UM):
      vis_sat.append(num_sat)
  return vis_sat

def passing_str(time, list_vis_sat, dic_ci, vec_f_receiv_alm):
  """
  Функция, которая заполняет вектор с принятыми альманахами КА для опред. точки

  Вх. аргументы:
    # time - текущее время
    # list_vis_sat - список с видимыми КА
    # dic_ci - словарь с ЦИ для всех КА и сигналов
    # vec_f_receiv_alm - вектор, который содержит флаги принятия альманахи
                         для соот. точки
  """
  for num_sat in list_vis_sat:
    passing_str_from_sat(time, dic_ci[str(num_sat)], vec_f_receiv_alm)
    
def passing_str_from_sat(time, dic_ci_sat, vec_f_receiv_alm):
  """
  Функция, которая заполняет вектор с принятыми альманахами КА для опред. точки
  от одного КА

  Вх. аргументы:
    # time - текущее время
    # dic_ci_sat - ЦИ для выбранного КА
    # vec_f_receiv_alm - вектор, который содержит флаги принятия альманахи
                         для соот. точки
  """
  # Цикл по сигналам
  for name_sig in gc.ALL_SIGNALS:
    time_tran_sig = gc.DIC_NAME_SIG_IN_TRANS_TIME[name_sig]
    # Заполняем флаг, если строка передалась
    if((time%time_tran_sig) == 0) and (dic_ci_sat[name_sig][time%gc.MAX_TIME_DI] >= gc.NUM_CON_ALM):
      ind_sat = dic_ci_sat[name_sig][time%gc.MAX_TIME_DI]-gc.NUM_CON_ALM
      vec_f_receiv_alm[ind_sat] = True

def save_res_dic_in_file(path_file: str, dic_obj: dict):
  """
  Функция сохранения в файл в файл типа json.

  Вх. аргументы:
    # dic_obj - ЦИ, которую необходимо записать
  """
  # Проверяем наличие каталога, если нет, создаем его
  time = datetime.datetime
  path_file += time.today().strftime('%Y_%m_%d_%H_%M_%S')+"/"
  my_mkdir(path_file)
  path_file += "list_rec_alm/"
  my_mkdir(path_file)
  # Цикл для перебора всех точек
  for cur_point in dic_obj.keys():
    # Распоковываем кортеж, т. к. json.dump не умеет записывать в файлы
    # списка, у которых в качестве ключа кортеж
    lat, lon = cur_point
    # Создаем каталог, который будет содержать все точки на данной широте
    path_result_file = path_file+f"{lat}/"
    my_mkdir(path_result_file)
    path_result_file += f"{lon}.json"
    data = dic_obj[cur_point]
    with open(path_result_file, "w", encoding="utf-8") as file:
      dump(data, file, indent=2) 

def my_mkdir(path_dir):
  """
  Функция создания каталога с проверкой на его отсутствие

  Вх. аргументы:
    # path_dir - путь до каталога
  """
  obj_path = Path(path_dir)
  f_dir = obj_path.is_dir()
  if (not f_dir):
      obj_path.mkdir()