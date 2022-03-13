import structs


def read_conf_file(path_file: str) -> list:
    """
    Функция чтения конфигурационного файла

    Вх. аргументы:
        # path_fil - путь до файла

    Вых. аргументы:
        # par_list - считанный список со строками, которые содержат конфигурационные параметры
    """
    with open(path_file, 'r') as file:
        par_list = file.readlines()

    return par_list


def convert_str_list_par_seq_alg(par_list: list) -> structs.ConfSettingsForSequencingAlgorithm:
    """
    Функция преобразлвания из списка с конфигурационными параметрами для алгоритма формирования последовательностей
    в соответствующую структуру

    Вх. аргументы:
        # par_list - Список с соответствующими параметрами
    Вых. аргументы:
        par_seq_alg - объект с считанными параметрами
    """
    par_seq_alg = structs.ConfSettingsForSequencingAlgorithm()
    for par in par_list:
        par_str, value = par.split('=')
        par_str = par_str.strip()
        value = int(value)
        if par_str == "IND_CALCUINAV_NKA":
            par_seq_alg.ind_calcui_nav_nka = value
        elif par_str == "IND_CALCUINAV_SIGNALID":
            par_seq_alg.ind_calcui_nav_signalid = value
        elif par_str == "IND_CALCUINAV_SYSTEMPOINT":
            par_seq_alg.ind_calcui_nav_systempoint = value
        elif par_str == "IND_CALCUINAV_L_AS":
            par_seq_alg.ind_calcui_nav_l_as = value
        elif par_str == "IND_CALCUINAV_L_PSK":
            par_seq_alg.ind_calcui_nav_l_psk = value
        elif par_str == "IND_CALCUINAV_N_ST":
            par_seq_alg.ind_calcui_nav_n_st = value
        elif par_str == "IND_CALCUINAV_T_OI":
            par_seq_alg.ind_calcui_nav_t_oi = value
        elif par_str == "IND_CALCUINAV_T_AS":
            par_seq_alg.ind_calcui_nav_t_as = value
        elif par_str == "IND_CALCUINAV_START_NAVPOINTS":
            par_seq_alg.ind_calcui_nav_start_navpoints = value
        elif par_str == "IND_CALCUINAV_END_NAVPOINTS":
            par_seq_alg.ind_calcui_nav_end_navpoints = value
        elif par_str == "IND_CALCUIEPIS_NKA":
            par_seq_alg.ind_calcui_epis_nka = value
        elif par_str == "IND_CALCUIEPIS_SIGNALID":
            par_seq_alg.ind_calcui_epis_signalid = value
        elif par_str == "IND_CALCUIEPIS_SYSTEMPOINT":
            par_seq_alg.ind_calcui_epis_systempoint = value
        elif par_str == "IND_CALCUIEPIS_ID":
            par_seq_alg.ind_calcui_epis_id = value
        elif par_str == "IND_CALCUIEPIS_IDSI":
            par_seq_alg.ind_calcui_epis_idsi = value
        elif par_str == "IND_CALCUIEPIS_SIZE":
            par_seq_alg.ind_calcui_epis_size = value
        elif par_str == "IND_CALCUIEPIS_MODE":
            par_seq_alg.ind_calcui_epis_mode = value
        elif par_str == "IND_CALCUIEPIS_T_STR":
            par_seq_alg.ind_calcui_epis_t_str = value
        elif par_str == "IND_CALCUIEPIS_KPS_STR":
            par_seq_alg.ind_calcui_epis_kps_str = value
        elif par_str == "IND_CALCUIEPIS_SS_STR":
            par_seq_alg.ind_calcui_epis_ss_str = value
        elif par_str == "IND_CALCUIEPIS_PPS_PSK":
            par_seq_alg.ind_calcui_epis_pps_psk = value
        elif par_str == "IND_CALCUIEPIS_PRIO_STR":
            par_seq_alg.ind_calcui_epis_prio_str = value
        elif par_str == "IND_CALCUIEPIS_PVS_PSK":
            par_seq_alg.ind_calcui_epis_pvs_psk = value
    return par_seq_alg


def get_conf_par_seq_alg(path_file) -> structs.ConfSettingsForSequencingAlgorithm:
    """
    Функция получения объекта с конфигурационными параметрами для алгоритма формирования последовательностей

    Вх. аргументы:
        # path_file - путь до конфигурационного файла

    Вых. аргументы:
        # par_seq_alg - объект с конфигурационными параметрами
    """
    sequenc_alg_par = read_conf_file(path_file)
    par_seq_alg = convert_str_list_par_seq_alg(sequenc_alg_par)
    return par_seq_alg

def get_path_conf_form_ci_file(par_list: list):
    """
    Функция выбирает из списка путь до файла с конфигурациями для формирования ЦИ, а также
    путь для сохранения сформированного файла с ЦИ

    Вх. аргументы:
        # par_list - Список с путями до файлов с конфигурациями
    Вых. аргументы:
        # (path_to_conf_form_ci, path_to_save_ci)
    """
    path_to_conf_form_ci = None
    path_to_save_ci = None
    for par in par_list:
        par_str, value = par.split("=")
        par_str = par_str.strip()
        value = value.strip()
        if par_str == "PATH_CONF_FORMATION_CI":
            path_to_conf_form_ci = value
        elif par_str == "RESULT_CI_FORMATION_FILE":
            path_to_save_ci = value
    return path_to_conf_form_ci, path_to_save_ci


def convert_str_list_par_set_form_ci(par_list: list) -> structs.ConfSettingsForFormationCI:
    """
    Функция получения объекта с конфигурационными параметрами для алгоритма формирования последовательностей

    Вх. аргументы:
        # par_list - Список с соответствующими параметрами
    Вых. аргументы:
        par_form_ci - объект с считанными параметрами
    """
    par_form_ci = structs.ConfSettingsForFormationCI()
    for par in par_list:
        par_str, value = par.split("=")
        par_str = par_str.strip()
        value = int(value)
        if par_str == "MAX_TIME":
            par_form_ci.max_time = value
        elif par_str == "NUM_CON_ALM":
            par_form_ci.num_con_alm = value
        elif par_str == "NOT_BEL_STR":
            par_form_ci.not_bel_str = value
    return par_form_ci


def get_conf_set_formation_ci(path_file_paths: str) -> structs.ConfSettingsForFormationCI:
    """
    Функция получения объекта с конфигурационными параметрами для формирования ЦИ

    Вх. аргументы:
        # path_file - путь до файла с конфигруциями

    Вых. аргументы:
        # conf_set_form_ci - объект, который содержит конфигурационные данные для формирования ЦИ
    """
    par_paths = read_conf_file(path_file_paths)
    path_to_conf_form_ci, path_to_save_ci = get_path_conf_form_ci_file(par_paths)
    par_set_form_ci = read_conf_file(path_to_conf_form_ci)
    conf_set_form_ci = convert_str_list_par_set_form_ci(par_set_form_ci)
    conf_set_form_ci.patH_to_save_ci_file = path_to_save_ci
    return conf_set_form_ci
