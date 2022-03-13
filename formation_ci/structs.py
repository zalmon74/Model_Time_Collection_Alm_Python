from numpy import array 


class STRUCT_MI_N:
    """
    Структура описания фразы УИ-Н (Управляющая Информация - Навигационная)

    Поля структуры:
      # n_ka_sys - Системный номер КА - (1...63)
      # n_ka_con - Условные номер КА - (1...1023)
      # type_sig - тип сигнала (соот. структуре описания типов сигнала) - (0...15)
      # name_sig - Имя сигнала
      # l_as  - количество строк АС (соот. кол-ву КА в системе) - (1...63)
      # l_psk - Общее количество строк в ПСК - (3...63)
      # t_oi  - Интервал актуальности строк ОИ, сек - (0...28800)
      # t_as  - Интервал актуальности строк АС, сек - (1800...5184000)
      # vec_n_as - Вектор из 63 элементов, который содержит системные номера КА,
                   которые передается в i-ой строке - (1...63)
    """

    def __init__(self, n_ka_sys: int, n_ka_con: int, type_sig: int,
                 l_as: int, l_psk: int, t_oi: int, t_as: int, vec_n_as: array):
        self.n_ka_sys = n_ka_sys
        self.n_ka_con = n_ka_con
        self.type_sig = type_sig
        # self.name_sig = name_sig
        self.l_as     = l_as
        self.l_psk    = l_psk
        self.t_oi     = t_oi
        self.t_as     = t_as
        self.vec_n_as = vec_n_as
  
    def print_all_fields(self):
        """
        Метод печати на экран всех полей объекта
        """
        print_str = f"{self.n_ka_sys=} \n"
        print_str += f"{self.n_ka_con=} \n"
        print_str += f"{self.type_sig=} \n"
        print_str += f"{self.name_sig=} \n"
        print_str += f"{self.l_as=} \n"
        print_str += f"{self.l_psk=} \n"
        print_str += f"{self.t_oi=} \n"
        print_str += f"{self.t_as=} \n"
        print_str += f"{self.vec_n_as=} \n"
        print(print_str)


class STRUCT_E_STR:
    """
    Структура описания типов строк

    Поля структуры:
      # type_str - Тип строки
      # type_sig - Тип сигнала
      # name_sig - Имя сигнала
      # name_si  - Наименование фразы СИ
      # content  - Содержание строки
    """

    def __init__(self, type_str: int, type_sig: array, name_sig: array, name_si: str, content: str):
        self.type_str = type_str
        self.type_sig = type_sig
        self.name_sig = name_sig
        self.name_si  = name_si
        self.content  = content
  
    def print_all_fields(self):
        """
        Метод печати на экран всех полей объекта
        """
        print_str = f"{self.type_str=} \n"
        print_str += f"{self.type_sig=} \n"
        print_str += f"{self.name_sig=} \n"
        print_str += f"{self.name_sig=} \n"
        print_str += f"{self.name_si=} \n"
        print_str += f"{self.content=} \n"
        print(print_str)


class STRUCT_MI_EPI:
    """
    Структура описания УИ-ЭпИ (Управляющая Информация - Эпизодической Информации)

    Поля структуры:
      # n_ka_sys - Системный номер КА - (1...63)
      # n_ka_con - Условные номер КА - (1...1023)
      # type_str - Тип строки
      # type_sig - Тип сигнала
      # name_sig - Имя сигнала
      # t_oi - Интервал актуальности строк ОИ, сек: при УИ-ФЦ   = 0
      #                                                 УИ-УР   = (60...1800)
      #                                                 УИ-ПВЗ  = (1800...5184000)
      #                                                 УИ-ПУМД = (1800...360000)
      #                                                 УИ-КС   = (60...1800)
      #                                                 УИ-ЕС   = (0...5184000)
      # kps   - Количество повторов строки - (0...255)
      # sync  - Синхронизация строки с началом получаса - (0...15)
      # pps   - Переодичность повтора строк в каждом ПСК - (0...15)
      # prior - Приоритет строки - (0...63)
      # pvs   - Порядок включения в ПСК - (0...1)
    """

    def __init__(self, n_ka_sys: int, n_ka_con: int, type_str: int, type_sig: int,
                 t_oi: int, kps: int, sync: int, pps: int, prior: int, pvs: bool):
        self.n_ka_sys = n_ka_sys
        self.n_ka_con = n_ka_con
        self.type_str = type_str
        self.type_sig = type_sig
        # self.name_sig = name_sig
        self.t_oi     = t_oi
        self.kps      = kps
        self.sync     = sync
        self.pps      = pps
        self.prior    = prior
        self.pvs      = pvs
  
    def print_all_fields(self):
        """
        Метод печати на экран всех полей объекта
        """

        print_str = f"{self.n_ka_sys=} \n"
        print_str += f"{self.n_ka_con=} \n"
        print_str += f"{self.type_str=} \n"
        print_str += f"{self.type_sig=} \n"
        # print_str += f"{self.name_sig=} \n"
        print_str += f"{self.t_oi=} \n"
        print_str += f"{self.kps=} \n"
        print_str += f"{self.sync=} \n"
        print_str += f"{self.pps=} \n"
        print_str += f"{self.prior=} \n"
        print_str += f"{self.pvs=} \n"
        print(print_str)
  

class ConfSettingsForSequencingAlgorithm:
    """
    Структура содержит конфигурационные параметры для парсинга результатов работы программы
    формирования последовательностей
    """

    def __init__(self):
        self.ind_calcui_nav_nka = None
        self.ind_calcui_nav_signalid = None
        self.ind_calcui_nav_systempoint = None
        self.ind_calcui_nav_l_as = None
        self.ind_calcui_nav_l_psk = None
        self.ind_calcui_nav_n_st = None
        self.ind_calcui_nav_t_oi = None
        self.ind_calcui_nav_t_as = None
        self.ind_calcui_nav_start_navpoints = None
        self.ind_calcui_nav_end_navpoints = None
        self.ind_calcui_epis_nka = None
        self.ind_calcui_epis_signalid = None
        self.ind_calcui_epis_systempoint = None
        self.ind_calcui_epis_id = None
        self.ind_calcui_epis_idsi = None
        self.ind_calcui_epis_size = None
        self.ind_calcui_epis_mode = None
        self.ind_calcui_epis_t_str = None
        self.ind_calcui_epis_kps_str = None
        self.ind_calcui_epis_ss_str = None
        self.ind_calcui_epis_pps_psk = None
        self.ind_calcui_epis_prio_str = None
        self.ind_calcui_epis_pvs_psk = None


class ConfSettingsForFormationCI:
    """
    Класс, который содержит конфигурационные данные для формирования ЦИ
    """
    def __init__(self):
        # Значение, с которого начинается условный номер КА
        self.num_con_alm = None
        # Условное значение, которое определяет, что данная строка не может передоваться
        # в соот. сигнале
        self.not_bel_str = None
        # Время в сек. на формирование ЦИ
        self.max_time = None
        # путь до файла с ЦИ
        self.patH_to_save_ci_file = None
