import math
from re import split 

import global_constants as gc

def alm_glo(ti, n, na, ta_lym, dta, ddta, lyma, oma, epsa, dia):
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