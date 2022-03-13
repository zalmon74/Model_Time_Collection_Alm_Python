from numpy import matrix, array, empty, full, append
import json
import datetime

import global_constants as gc
import structs


def formation_mat_obj_mi_n(mat_av_sig_for_sat: matrix, vec_l_psk: array, vec_t_oi: array, vec_t_as: array,
                           vec_seq: array, step_seq: int, max_seq: int):
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
            if mat_av_sig_for_sat[ind_sat, ind_sig] == 1:
                mat_mi_n[ind_sat, ind_sig] = structs.STRUCT_MI_N(ind_sat + 1, ind_sat + 1 + gc.NUM_CON_ALM, ind_sig,
                                                                 count_sat, vec_l_psk[ind_sig],
                                                                 vec_t_oi[ind_sig], vec_t_as[ind_sig],
                                                                 full(63, gc.NOT_BEL_STR))
                # Формируем последовательность передачи альманаха
                vec_seq_alm = get_seq_alm(count_sat, ind_sat, count_sig, ind_sig
                                          , vec_seq, step_seq, max_seq)
                mat_mi_n[ind_sat, ind_sig].vec_n_as[:count_sat] = vec_seq_alm[:]
            else:
                continue
    return mat_mi_n


def get_seq_alm(count_sat: int, ind_sat: int, max_count_sig: int, ind_sig: int
                , vec_seq: array, step_seq: int, max_seq: int):
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
        first_base = list(range(vec_seq[ind_sat] * step_seq - 1, count_sat))
        second_base = list(range(vec_seq[ind_sat] * step_seq - 1))
        base = array([*first_base, *second_base])
    elif (ind_sig == gc.DIC_NAME_SIG_IN_IND["L2SC"]) or \
            (ind_sig == gc.DIC_NAME_SIG_IN_IND["L3OC"]):
        # Если сигналы находится в одной группе, то они сдвигаются на половину
        # кол-во КА
        start = int(vec_seq[ind_sat] * step_seq + count_sat / 2 * step_seq - 1)
        while ((start > (count_sat - 1)) and (count_sat > 1)):
            start -= (count_sat - 1)
            start = int(start)
        first_base = list(range(start, count_sat))
        second_base = list(range(start))
        base = array([*first_base, *second_base])
    return base


def formation_arr_obj_mi_epi(count_sat: int, mat_av_str_for_sig: matrix
                             , mat_t_oi: matrix, mat_kps: matrix, mat_sync: matrix
                             , mat_pps: matrix, mat_prior: matrix, mat_pvs: matrix):
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
                if mat_av_str_for_sig[ind_str, ind_sig] == gc.NOT_BEL_STR:
                    continue
                arr_mi_epi[ind_sat, ind_str, ind_sig] = structs.STRUCT_MI_EPI(
                    ind_sat + 1
                    , ind_sat + 1 + gc.NUM_CON_ALM
                    , gc.DIC_IND_STR_IN_STR[ind_sig]
                    , ind_sig
                    , mat_t_oi[ind_str, ind_sig]
                    , mat_kps[ind_str, ind_sig]
                    , mat_sync[ind_str, ind_sig]
                    , mat_pps[ind_str, ind_sig]
                    , mat_prior[ind_str, ind_sig]
                    , mat_pvs[ind_str, ind_sig]
                )
    return arr_mi_epi


def save_ci_in_file(ci):
    """
      Функция сохранения ЦИ в файл типа json.

      Вх. аргументы:
        # ci - ЦИ, которую необходимо записать
      """
    time = datetime.datetime
    path_file = gc.SET_FORM_CI.patH_to_save_ci_file + "ci_" + time.today().strftime('%Y_%m_%d_%H_%M_%S') + ".json"
    with open(path_file, "w", encoding=gc.ENCODING_FOR_FILE) as file:
        json.dump(ci, file, indent=2)


def parsing_nav_info_seq_alg_result_file(nav_obj_json, conf_par_seq: structs.ConfSettingsForSequencingAlgorithm):
    """
    Функция для парсинга информации навигационной составляющей файла

    Вх. аргументы:
        # nav_obj_json - навигационная составляющая файла
        # conf_par_seq - объект с конфигурационными параметрами для парсинга файла с результатами работы
            алгоритма формирования последовательностей
    """
    mat_mi_n = []
    arr_nav = []
    for obj in nav_obj_json:
        vec_n_as = []
        for ind_obj in range(len(obj)):
            value = obj[ind_obj]
            # Заменить маг. числа на данные из конфигурационного файла
            if ind_obj == conf_par_seq.ind_calcui_nav_nka:
                num_sat = value
            elif ind_obj == conf_par_seq.ind_calcui_nav_signalid:
                signalid = value
            elif ind_obj == conf_par_seq.ind_calcui_nav_systempoint:
                systempoint = value
            elif ind_obj == conf_par_seq.ind_calcui_nav_l_as:
                l_as = value
            elif ind_obj == conf_par_seq.ind_calcui_nav_l_psk:
                l_psk = value
            elif ind_obj == conf_par_seq.ind_calcui_nav_n_st:
                n_st = value
            elif ind_obj == conf_par_seq.ind_calcui_nav_t_oi:
                t_oi = value
            elif ind_obj == conf_par_seq.ind_calcui_nav_t_as:
                t_as = value
            else:
                if obj[ind_obj] != 255:
                    vec_n_as.append(value)
                else:
                    vec_n_as.append(gc.SET_FORM_CI.not_bel_str)
        if len(arr_nav) == 0 or arr_nav[-1].n_ka_sys == systempoint:
            obj_for_append = structs.STRUCT_MI_N(systempoint, num_sat, signalid, l_as, l_psk, t_oi, t_as, vec_n_as)
            arr_nav.append(obj_for_append)
        else:
            mat_mi_n.append(arr_nav)
            arr_nav = []
            obj_for_append = structs.STRUCT_MI_N(systempoint, num_sat, signalid, l_as, l_psk, t_oi, t_as, vec_n_as)
            arr_nav.append(obj_for_append)
    # Необходимо добавить последний элемент, так как добавление происходит на итерации следующего элемента
    mat_mi_n.append(arr_nav)
    return mat_mi_n


def parsing_epis_info_seq_alg_result_file(epis_obj_json, conf_par_seq: structs.ConfSettingsForSequencingAlgorithm):
    """
    Функция для парсинга информации эпизодической составляющей файла

    Вх. аргументы:
        # epis_obj_json - навигационная составляющая файла
        # conf_par_seq - объект с конфигурационными параметрами для парсинга файла с результатами работы
            алгоритма формирования последовательностей
    """
    arr_mi_epis = []  # Выходной массив
    mat_epis = []  # Матрица, которая содержит параметры строк для каждого сигнала
    arr_str = []  # Массив, который содержит строки для одного сигнала
    for epis_obj in epis_obj_json:
        for ind_obj in range(len(epis_obj)):
            value = epis_obj[ind_obj]
            # Заменить маг. числа на параметры из конф. файла
            if ind_obj == conf_par_seq.ind_calcui_epis_nka:
                num_sat = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_signalid:
                signalid = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_systempoint:
                systempoint = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_id:
                num_str = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_idsi:
                idsi = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_size:
                size = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_mode:
                mode = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_t_str:
                t_str = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_kps_str:
                kps = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_ss_str:
                ss_str = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_pps_psk:
                pps = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_prio_str:
                prior = value
            elif ind_obj == conf_par_seq.ind_calcui_epis_pvs_psk:
                pvs = value
        mi_epis = structs.STRUCT_MI_EPI(systempoint, num_sat, num_str, signalid, t_str, kps, ss_str, pps, prior, pvs)
        if len(arr_str) == 0 or (arr_str[-1].n_ka_sys == systempoint and arr_str[-1].type_sig == signalid):
            arr_str.append(mi_epis)
        else:
            if len(mat_epis) == 0 or mat_epis[-1][-1].n_ka_sys == systempoint:
                mat_epis.append(arr_str)
            else:
                # Необходимо добавить последний элемент, так как добавление происходит на итерации следующего элемента
                mat_epis.append(arr_str)
                arr_mi_epis.append(mat_epis)
                mat_epis = []
            arr_str = []
            # Необходимо добавить последний элемент, так как добавление происходит на итерации следующего элемента
            arr_str.append(mi_epis)
    # Необходимо добавить последний элемент, так как добавление происходит на итерации следующего элемента
    mat_epis.append(arr_str)
    arr_mi_epis.append(mat_epis)
    return arr_mi_epis


def convert_list_to_array_3(arr_mi_epis):
    """
    Функция конвертации из списка в 3х мерный массив

    Вх. аргументы:
        # arr_mi_epis - массив, который необходиом переконвертировать
    """
    count_sat = len(arr_mi_epis)
    counts_sig = (len(list_) for list_ in arr_mi_epis)
    count_sig = max(counts_sig)
    count_str = gc.MAX_COUNT_STR
    output_arr = empty([count_sat, count_sig, count_str], dtype=structs.STRUCT_MI_EPI)
    # Цикл перебора КА
    for ind_sat in range(count_sat):
        # Цикл перебора сигналов
        for ind_sig in range(count_sig):
            # Цикл перебора строк
            for ind_str in range(count_str):
                if ind_str < len(arr_mi_epis[ind_sat][ind_sig]):
                    output_arr[ind_sat][ind_sig][ind_str] = arr_mi_epis[ind_sat][ind_sig][ind_str]
                else:
                    pass
    return output_arr


def read_result_sequencing_alg_result_file(path_file: str, conf_par_seq: structs.ConfSettingsForSequencingAlgorithm):
    """
    Функция чтения файла с результатами алгоритма, который формирует последовательности

    Вх. аргументы:
        # path_file - путь до файла
        # conf_par_seq - объект с конфигурационными параметрами для парсинга файла с результатами работы
            алгоритма формирования последовательностей
    """
    with open(path_file, 'r', encoding=gc.ENCODING_FOR_FILE) as file:
        json_obj = json.load(file)
    epis_obj_json = json_obj["EPIS"]
    nav_obj_json = json_obj["NAV"]
    mat_mi_n = parsing_nav_info_seq_alg_result_file(nav_obj_json, conf_par_seq)
    arr_mi_epis = parsing_epis_info_seq_alg_result_file(epis_obj_json, conf_par_seq)
    mat_mi_n = array(mat_mi_n)
    arr_mi_epis = convert_list_to_array_3(arr_mi_epis)
    return mat_mi_n, arr_mi_epis


def my_round_vec(vec_val):
    """
    Функция округления вектор каждого эл. до ближайшего целого

    Вх. аргументы:
    # vec_val - вектор, которой необходимо окргулить

    Вых. аргументы:
    # vec_out - округленный вектор
    """
    vec_out = empty(vec_val.size, dtype=int)
    # Перебор эл. вектора
    for ind in range(vec_val.size):
        el = vec_val[ind]
        if el > int(el):
            vec_out[ind] = int(el) + 1
        else:
            vec_out[ind] = int(el)
    return vec_out
