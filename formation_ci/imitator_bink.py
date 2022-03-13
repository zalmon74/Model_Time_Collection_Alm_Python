from numpy import mat, matrix, array, zeros, where, nonzero, full

import global_constants as gc
from functions import my_round_vec


def imitator_bink(mat_mi_n: matrix, arr_mi_epi: array):
    """
    Функция моделирования работы БИНК

    Вх. аргумнты:
      # mat_mi_n - матрица, которая содержит объекты типа УИ-Н для каждого КА
      # arr_mi_epi - массив, который содержит объекты типа УИ-ЭИ для каждого КА
    """
    # Декодируем данные (получем ИД)
    vec_l_psk, vec_t_oi, vec_t_as, \
    dic_ind_sig_name_sig, dic_name_sig_ind_sig, \
    mat_t_oi, mat_kps, mat_sync, mat_pps, mat_prior, mat_pvs = decode_info_for_bink(mat_mi_n, arr_mi_epi)
    # Определяем наличие сигналов у КА
    mat_av_sig_for_sat, arr_n_as = decode_mat_av_sig_for_sat(mat_mi_n)
    # Вычисляем кол-во ПСК передаваемых за время gc.TIME_MAX
    vec_count_psk = calculation_count_psk_for_all_signals(vec_l_psk)
    # Вызываем функцию формирования ЦИ для одного сигнала
    ci = generator_ci_for_all_sat(mat_av_sig_for_sat, vec_count_psk, vec_l_psk, arr_n_as, mat_sync, mat_pps,
                                  mat_kps, mat_prior)
    return ci


def decode_info_for_bink(mat_mi_n: matrix, arr_mi_epi: array):
    """
    Функция декодирования информации. Которая преобразует информацию из матриц и
    массивов обратно в ИД. Необходимо для упрощения доступа к данным.
    Так как на вход в имитатор данные приходят в сформированный обьъектах

    # Вх. аргументы:
      # mat_mi_n - матрица, которая содержит объекты типа УИ-Н для каждого КА
      # arr_mi_epi - массив, который содержит объекты типа УИ-ЭИ для каждого КА

    # Вых. аргументы:
      # vec_l_psk - вектор, который хранит в себе размер ПСК для каждого сигнала
      # vec_t_oi  - вектор, который хранит интервал актуальности строк с ОИ
      # vec_t_as  - вектор, который хранит интервал актуальности строк с АС
      # mat_t_oi  - матрица с интервалом актуальности
      # mat_kps   - матрица с количеством повторов строк
      # mat_sync  - матрица с синхронизациями строк
      # mat_pps   - матрица с периодом повторения строк
      # mat_prior - матрица с приоритетами строк
      # mat_pvs   - матрица с порядком включения строк
    """
    # Декодируем информацию
    vec_l_psk, vec_t_oi, vec_t_as, \
    dic_ind_sig_name_sig, dic_name_sig_ind_sig = decode_mat_mi_n(mat_mi_n)
    mat_t_oi, mat_kps, mat_sync, mat_pps, mat_prior, mat_pvs = decode_arr_mi_epi(arr_mi_epi)

    return vec_l_psk, vec_t_oi, vec_t_as, \
           dic_ind_sig_name_sig, dic_name_sig_ind_sig, \
           mat_t_oi, mat_kps, mat_sync, mat_pps, mat_prior, mat_pvs


def decode_mat_mi_n(mat_mi_n: matrix):
    """
    Функция декодирования матрицы (преобразование в ИД), которая хранит объекты
    типа УИ-Н для каждого КА

    # Вх. аргументы:
      # mat_mi_n - матрица, которая содержит объекты типа УИ-Н для каждого КА

    # Вых. аргументы:
      # vec_l_psk - вектор, который хранит в себе размер ПСК для каждого сигнала
      # vec_t_oi  - вектор, который хранит интервал актуальности строк с ОИ
      # vec_t_as  - вектор, который хранит интервал актуальности строк с АС
      # dic_ind_sig_name_sig - словарь, который содержит сопоставление индекса
                               сигнала с его именем
      # dic_name_sig_ind_sig - словарь, который содержит сопоставление имени
                               сигнала с его индексом
    """
    count_sat, count_sig = mat_mi_n.shape
    # Выходные парамтеры
    vec_l_psk = zeros(count_sig)
    vec_t_oi = zeros(count_sig)
    vec_t_as = zeros(count_sig)
    dic_ind_sig_name_sig = {}
    dic_name_sig_ind_sig = {}
    # Цикл для нахождения КА, у которого имеются все сигнала
    for ind_sat in range(count_sat):
        # Если имеется в данном сигнале None, то переходим на след. КА, так как
        # в данном сигнале нет опред. сигнала
        if None in mat_mi_n[ind_sat]:
            continue
        else:
            # Цикл по сигналам
            for ind_sig in range(count_sig):
                obj = mat_mi_n[ind_sat, ind_sig]
                vec_l_psk[ind_sig] = obj.l_psk
                vec_t_oi[ind_sig] = obj.t_oi
                vec_t_as[ind_sig] = obj.t_as
                # dic_ind_sig_name_sig[obj.type_sig] = obj.name_sig
                # dic_name_sig_ind_sig[obj.name_sig] = obj.type_sig
            break;
    return vec_l_psk, vec_t_oi, vec_t_as, \
           dic_ind_sig_name_sig, dic_name_sig_ind_sig


def decode_arr_mi_epi(arr_mi_epi: array):
    """
    Функция декодирования массива (преобразование в ИД), которая хранит объекты
    типа УИ-ЭпИ для каждого КА

    Вх. аргументы:
      # arr_mi_epi - массив, который содержит объекты типа УИ-ЭпИ для каждого КА

    Вых. аргументы:
      # mat_t_oi  - матрица с интервалом актуальности
      # mat_kps   - матрица с количеством повторов строк
      # mat_sync  - матрица с синхронизациями строк
      # mat_pps   - матрица с периодом повторения строк
      # mat_prior - матрица с приоритетами строк
      # mat_pvs   - матрица с порядком включения строк
    """
    count_sat, count_str, count_sig = arr_mi_epi.shape
    mat_t_oi = zeros([count_str, count_sig], dtype=int)
    mat_kps = zeros([count_str, count_sig], dtype=int)
    mat_sync = zeros([count_str, count_sig], dtype=int)
    mat_pps = zeros([count_str, count_sig], dtype=int)
    mat_prior = zeros([count_str, count_sig], dtype=int)
    mat_pvs = zeros([count_str, count_sig], dtype=int)
    # Подсчитываем сколько строк отсутствуют в каждом КА
    vec_cunt_dont_str = calculation_vec_count_dont_str_sat(arr_mi_epi)
    # Определяем, где отсутствуют меньше всего строк, тот КА и будем использовать
    ind_sat = where(vec_cunt_dont_str.min())[0][0]
    # Цикл перебора строк
    for ind_str in range(count_str):
        # Цикл перебора сигналов
        for ind_sig in range(count_sig):
            # Если данной строки нет для соот. сигнала, то переходим к следующей,
            # а матрицу заполняем соот. числом
            if arr_mi_epi[ind_sat, ind_str, ind_sig] is None:
                mat_t_oi[ind_str, ind_sig] = gc.SET_FORM_CI.not_bel_str
                mat_kps[ind_str, ind_sig] = gc.SET_FORM_CI.not_bel_str
                mat_sync[ind_str, ind_sig] = gc.SET_FORM_CI.not_bel_str
                mat_pps[ind_str, ind_sig] = gc.SET_FORM_CI.not_bel_str
                mat_prior[ind_str, ind_sig] = gc.SET_FORM_CI.not_bel_str
                mat_pvs[ind_str, ind_sig] = gc.SET_FORM_CI.not_bel_str
                continue
            else:
                mat_t_oi[ind_str, ind_sig] = arr_mi_epi[ind_sat, ind_str, ind_sig].t_oi
                mat_kps[ind_str, ind_sig] = arr_mi_epi[ind_sat, ind_str, ind_sig].kps
                mat_sync[ind_str, ind_sig] = arr_mi_epi[ind_sat, ind_str, ind_sig].sync
                mat_pps[ind_str, ind_sig] = arr_mi_epi[ind_sat, ind_str, ind_sig].pps
                mat_prior[ind_str, ind_sig] = arr_mi_epi[ind_sat, ind_str, ind_sig].prior
                mat_pvs[ind_str, ind_sig] = arr_mi_epi[ind_sat, ind_str, ind_sig].pvs

    return mat_t_oi, mat_kps, mat_sync, mat_pps, mat_prior, mat_pvs


def calculation_vec_count_dont_str_sat(arr_mi_epi: array):
    """
    Функция расчета кол-ва строк, которые отсутствуют в данном КА

    # Вх. аргументы:
      #arr_mi_epi - массив, который содержит объекты типа УИ-ЭпИ для каждого КА

    # Вых. аргументы:
      # vec_count_dont_str - вектор, который характеризует какое кол-во строк отс.
                             в соот. КА
    """
    count_sat, count_str, count_sig = arr_mi_epi.shape
    vec_count_dont_str = zeros(count_sat, dtype=int)
    # Цикл перебора КА
    for ind_sat in range(count_sat):
        vec_count_dont_str[ind_sat] = (arr_mi_epi[ind_sat] == None).sum()
    return vec_count_dont_str


def decode_mat_av_sig_for_sat(mat_mi_n: matrix):
    """
    Функция декдоирования матрицы, которая характеризует наличие опред. сигнала
    у КА

    Вх. аргументы:
      # mat_mi_n - матрица, которая содержит объекты типа УИ-Н для каждого КА

    # Вых. аргументы:
      # mat_av_sig_for_sat - матрица, описывающая наличие опред. сигнала в соот. КА
      # arr_n_as - массив, который содержит посследовательность передачи альманаха
                   для всех КА и сигналов
    """
    count_sat, count_sig = mat_mi_n.shape
    mat_av_sig_for_sat = zeros([count_sat, count_sig])
    arr_n_as = zeros([count_sat, count_sig, gc.MAX_COUNT_ALM])
    # Цикл перебора КА
    for ind_sat in range(count_sat):
        # Цикл перебора сигналов
        for ind_sig in range(count_sig):
            temp_value = 0
            if mat_mi_n[ind_sat, ind_sig] is not None:
                temp_value = 1
            mat_av_sig_for_sat[ind_sat, ind_sig] = temp_value
            arr_n_as[ind_sat, ind_sig] = mat_mi_n[ind_sat, ind_sig].vec_n_as
    return mat_av_sig_for_sat, arr_n_as


def calculation_count_psk_for_all_signals(vec_l_psk: array):
    """
    Функция расчета количества ПСК для каждого сигнала на время передачи gc.MAX_TIME

    Вх. аргументы:
      # vec_l_psk - размер ПСК для каждого сигнала

    Вых. аргументы:
      # vec_count_psk - количество ПСК для каждого сигнала на время передачи gc.MAX_TIME
    """
    vec_count_psk = zeros(vec_l_psk.size)
    # Цикл перебора сигналов
    for ind_sig in range(vec_l_psk.size):
        # Определяем имя сигнала
        name_sig = gc.DIC_IND_SIG_IN_NAME[ind_sig]
        # Рассчитываем кол-во ПСК
        vec_count_psk[ind_sig] = gc.SET_FORM_CI.max_time / (vec_l_psk[ind_sig] * gc.DIC_NAME_SIG_IN_TRANS_TIME[name_sig])
    # Округляем кол-во ПСК в большую сторону
    vec_count_psk = my_round_vec(vec_count_psk)
    return vec_count_psk


def generator_ci_for_all_sat(mat_av_sig_for_sat: matrix, vec_count_psk: array, vec_l_psk: array, arr_n_as: array,
                             mat_sync: matrix, mat_pps: matrix, mat_kps: matrix, mat_prior: matrix):
    """
    Функция формирования ЦИ для всех КА

    Вх. аргументы:
      # mat_av_sig_for_sat - матрица, описывающая наличие опред. сигнала в соот. КА
      # vec_count_psk - вектор с количеством ПСК для каждого сигнала
      # vec_l_psk - вектор с количеством ПСК для каждого сигнала
      # arr_n_as  - массив с индексами альманаха
      # mat_sync  - матрица со значениями синхронизации строк
      # mat_pps   - матрица со значениями периода повтороения строк
      # mat_kps   - матрица со значениями количества повторов строк
      # mat_prior - матрица со значениями приоритетов строк

    Вых. аргументы:
      # dic_ci - ЦИ в виде словаря, где ключ это номер КА, а данные словарь с
                 сигналами с ЦИ
    """
    count_sat, count_sig, count_max_alm = arr_n_as.shape
    ci = {}
    # Цикл перебора КА
    for ind_sat in range(count_sat):
        ci[int(ind_sat + 1)] = generator_ci_for_all_signals(mat_av_sig_for_sat[ind_sat, :], vec_count_psk, vec_l_psk,
                                                            arr_n_as[ind_sat, :, :], mat_sync,
                                                            mat_pps, mat_kps, mat_prior, count_sat)
    return ci


def generator_ci_for_all_signals(vec_av_sig_for_sat: array, vec_count_psk: array, vec_l_psk: array, mat_n_as: matrix,
                                 mat_sync: matrix, mat_pps: matrix, mat_kps: matrix, mat_prior: matrix, count_sat: int):
    """
    Функция формирования ЦИ для всех сигналов одного КА

    Вх. аргументы:
      # vec_av_sig_for_sat - вектор, который характеризует доступность сигналов
      # vec_count_psk - вектор с количеством ПСК для каждого сигнала
      # mat_n_as  - матрица с индексами альманаха, которые передаются в данном КА
      # mat_sync  - матрица со значениями синхронизации строк
      # mat_pps   - матрица со значениями периода повтороения строк
      # mat_kps   - матрица со значениями количества повторов строк
      # mat_prior - матрица со значениями приоритетов строк
      # count_psk - кол-во КА

    Вых. аргументы:
      # ci_for_sat - сформированная ЦИ для одного КА в виде словаря, где
                     ключ: имя сигнала, а данные ЦИ
    """
    count_sig = nonzero(vec_av_sig_for_sat != None)[0].size
    ci_for_sat = {}
    # Цикл перебора сигналов
    for ind_sig in range(count_sig):
        name_sig = gc.DIC_IND_SIG_IN_NAME[ind_sig]
        ci_for_sat[name_sig] = generator_ci_for_signal(vec_count_psk[ind_sig], vec_l_psk[ind_sig], mat_sync[:, ind_sig],
                                                       mat_pps[:, ind_sig], mat_kps[:, ind_sig], mat_prior[:, ind_sig],
                                                       mat_n_as[ind_sig, :], gc.DIC_NAME_SIG_IN_TRANS_TIME[name_sig],
                                                       count_sat)
    return ci_for_sat


def generator_ci_for_signal(count_psk: int, size_psk: int, vec_sync: array, vec_pps: array, vec_kps: array,
                            vec_prior: array, vec_n_as: array, time_slot: int, count_sat: int):
    """
    Функция формирования ЦИ для одного сигнала

    Вх. аргументы:
      # count_psk - количество ПСК в данном сигнале
      # size_psk  - размер ПСК
      # vec_sync  - вектор со значениями синхронизации строк для данного сигнала
      # vec_pps   - вектор со значениями периода повтороения строк для данного сигнала
      # vec_kps   - вектор со значениями количества повторов строк для данного сигнала
      # vec_prior - вектор со значениями приоритетов строк для данного сигнала
      # vec_n_as  - вектор с индексами альманаха, который должен передаваться
      # time_slot - время передачи одного слота
      # count_sat - количество КА

    Вых. аргументы:
      # vec_ci_sig - сформированный список с ЦИ
    """
    # Формируем словарь, который содержит сопоставление номера ПСК номера строк
    # строк с ЭИ, которые передаются в нем
    dic_num_psk_in_str = formation_dic_num_psk_in_ind_str(count_psk, vec_sync, vec_pps, vec_kps, vec_prior)
    count_str = vec_sync.size
    tr_slot = 0  # Кол-во переданных слотов в ПСК
    tr_psk = 0  # Номер передаваемого ПСК
    tr_ind_alm = 0  # Индекс последнего переданного альманаха
    vec_tr_epi = zeros(count_str)  # Вектор, с кол-вом переданных строк с ЭИ
    vec_ci_sig = [0 for _ in range(gc.SET_FORM_CI.max_time)]
    # Вектор содержит номер последеного ПСК в котором передавалась данная строка
    vec_last_psk_tr_str = zeros(count_str)
    time = 0
    # Цикл по времмени для формирования ЦИ
    while time < gc.SET_FORM_CI.max_time:
        # Условие передачи ОИ в ПСК
        if tr_slot < gc.VEC_NUM_OI.size:
            vec_ci_sig[time] = int(gc.VEC_NUM_OI[tr_slot])
            # Проверка на передачу одного слота соот. сигнала
            # +1, т. к. нумерация осуществляется с 0
            if ((time + 1) % time_slot) == 0:
                tr_slot += 1
            # Проверка на окончание ПСК (-1 т. к. нумерация начинается с 0)
            if tr_slot == size_psk - 1:
                tr_slot = 0
                tr_psk += 1
            time += 1
        else:  # Передача всех остальных строк
            # Определяем наличие строк с ЭИ в данном ПСК
            str_ei = dic_num_psk_in_str.get(tr_psk)
            # Проверяем на наличие строк с ЭИ, если None, то заполняем ПСК альманахом
            if not (str_ei is None):  # Заполняем ПСК ЭИ
                # Цикл по строкам с ЭИ
                for num_str in str_ei:
                    # Определяем индекс строки
                    ind_str = gc.DIC_NUM_STR_IN_IND[num_str]
                    # Локальный цикл по времени для затаскивания в ПСК полную строку
                    for l_time in range(time_slot):
                        vec_ci_sig[time] = int(num_str)
                        time += 1
                    # Заполняем соот. переменные о том, что строка была передана
                    vec_tr_epi[ind_str] += 1
                    vec_last_psk_tr_str[ind_str] = tr_psk
                    tr_slot += 1
                    # Проверка на окончание ПСК
                    if tr_slot == size_psk:
                        tr_slot = 0
                        tr_psk += 1
                        # Так. как места больше нет, для последующих строк в данном ПСК
                        break
                        # Заполняем ПСК альманахом
            # Вычисляем кол-во слотов для передачи альманаха
            count_rem_slot = int(size_psk - tr_slot)
            # Цикл заполнения оставшихся строк
            for i_slot in range(count_rem_slot):
                # Текущий индекс альманаха
                ind_alm = tr_ind_alm
                # Локальный цикл по времени для формирования слота
                for l_time in range(time_slot):
                    vec_ci_sig[time] = int(vec_n_as[ind_alm] + gc.SET_FORM_CI.num_con_alm)
                    time += 1
                    # Проверка на окончание формирования по времени
                    if time >= gc.SET_FORM_CI.max_time:
                        return vec_ci_sig
                # Т. к. передался один слот, необходимо инкрементировать соот. параметры
                tr_slot += 1
                tr_ind_alm += 1
                # Проверка на выход за границы индекса
                if tr_ind_alm >= count_sat:
                    tr_ind_alm = 0
                # Проверка на окончание ПСК
                if tr_slot == size_psk:
                    tr_slot = 0
                    tr_psk += 1
    return vec_ci_sig


def formation_dic_num_psk_in_ind_str(count_psk: int, vec_sync: array, vec_pps: array, vec_kps: array, vec_prior: array):
    """
    Функция формирования словаря, который будет сопоставлять номер передаваемого
    ПСК и строки с ЭИ, которые он передает

    Вх. аргументы:
      # count_psk - количество ПСК в данном сигнале
      # vec_sync  - вектор со значениями синхронизации строк для данного сигнала
      # vec_pps   - вектор со значениями периода повтороения строк для данного сигнала
      # vec_kps   - вектор со значениями количества повторов строк для данного сигнала
      # vec_prior - вектор со значениями приоритетов строк для данного сигнала

    Вых. аргументы:
      # dic_output - сформированный словарь
    """
    count_str = vec_sync.shape
    dic_output = {}
    # Вектор, который будет характеризовать, сколько раз передаавась строка
    vec_count_tr_str = zeros(count_str, dtype=int)
    # Вектор, который будет содеражть в каком следующем ПСК будет передоваться строка
    # изначально данный вектор, будет равен вектору синхронизации для данного сигнала
    vec_next_psk = vec_sync
    # Цикл перебора ПСК
    for num_psk in range(count_psk):
        # Определяем веткор, который хранит в себе индексы строк с ЭИ, которые
        # передаются в данном ПСК
        vec_ind_str_cur_psk = array(where(vec_next_psk == num_psk)[0])
        # Если получен вектор, не содержит элементов, то переходим к след. ПСК
        if vec_ind_str_cur_psk.size == 0:
            continue
        # Вектор, который хранит номера строк, которые будут передаваться в данном ПСК
        vec_str_cur_psk = full(vec_ind_str_cur_psk.size, gc.SET_FORM_CI.not_bel_str, dtype=int)
        # Цикл перебора передающихся строк
        for ind_loc_str in range(vec_ind_str_cur_psk.size):
            # Определяем индекс строки, которая передается
            ind_str = vec_ind_str_cur_psk[ind_loc_str]
            # Проверяем на кол-во переданных строк, если данная строка уже превысила
            # лимит передачи, то пропускаем ее
            if vec_count_tr_str[ind_str] == vec_kps[ind_str]:
                continue
            # Определяем номер строки, которая передается
            vec_str_cur_psk[ind_loc_str] = gc.DIC_IND_STR_IN_STR[ind_str]
            # Записываем в каком след. ПСК будет данная строка
            vec_next_psk[ind_str] += vec_pps[ind_str]
            # Фиксируем, что данная строка передалась
            vec_count_tr_str[ind_str] += 1
        # Из-за того, что передача строк может быть ограничена (превышен лимит)
        # То необходимо отсеять, строки, которые не передавались в данном ПСК
        # Данные строки равные парамтеру gc.NOT_BEL_STR
        # Определяем локальные индексы строк, которые передавались в данном ПСК
        vec_loc_ind_tr_str = nonzero(vec_str_cur_psk != gc.SET_FORM_CI.not_bel_str)[0]
        # Определяем номера строк
        vec_str_cur_psk = vec_str_cur_psk[vec_loc_ind_tr_str]
        # Сортируем полученный вектор с номерами строк в соот. с приоритетом, если
        # размер больше 1, иначе смысла нет
        if vec_str_cur_psk.size > 1:
            vec_str_cur_psk = sort_vec_str_relatively_prior(vec_str_cur_psk, vec_prior)
        # Записываем полученный вектор в словарь
        dic_output[num_psk] = vec_str_cur_psk

    return dic_output


def sort_vec_str_relatively_prior(vec_need_sort: array, vec_prior: matrix):
    """
    Функция сортировки вектора с номерами строк в соответсвии с их приоритетом

    Вх. аргументы:
      # vec_need_sort - вектор, который необходимо отсортировать
      # vec_prior - вектор со значениями приоритета строк для данного сигнала
      # ind_sig   - индекс сигнала

    Вых. аргументы:
      # vec_sorted - отсортированный словарь
    """
    vec_sorted = vec_need_sort
    # Цикл перебора вектора
    for ind in range(vec_need_sort.size - 1):
        # Определяем индекс строки
        ind_str = gc.DIC_NUM_STR_IN_IND[vec_need_sort[ind]]
        # Определяем номер строки
        num_str_i = gc.DIC_IND_STR_IN_STR[ind_str]
        # Определяем приоритет тек. строки
        prior_ind = vec_prior[ind_str]
        # Цикл для сортировки
        for jnd in range(ind + 1, vec_need_sort.size):
            # Определяем индекс второй строки
            jnd_str = gc.DIC_NUM_STR_IN_IND[vec_need_sort[jnd]]
            # Определяем номер второй строки
            num_str_j = gc.DIC_IND_STR_IN_STR[jnd_str]
            # Определяем приоритет второй строки
            prior_jnd = vec_prior[jnd_str]
            # Условие сортировки
            if ((prior_jnd == prior_ind) and (num_str_j < num_str_i)) or \
                    (prior_jnd < prior_ind):
                temp = vec_sorted[ind]
                vec_sorted[ind] = vec_sorted[jnd]
                vec_sorted[jnd] = temp
                ind = jnd

    return vec_sorted
