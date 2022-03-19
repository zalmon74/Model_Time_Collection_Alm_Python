#ifndef STRUCTS_H
#define STRUCTS_H

#include <stdint.h>
#include <iostream>
#include <iomanip>
#include <math.h>
#include <vector>

#define UNDEFINE_UINT8  0xFF
#define UNDEFINE_INT16  0x7FFF
#define UNDEFINE_UINT16 0xFFFF

template <class T>
struct SimpleArray
{
  std::vector<T> elements;

  size_t GetSlotCount() { return elements.size(); }
  size_t GetSlotCount() const { return elements.size(); }
  T& operator[](const int ind) { return this->elements[ind]; }
  const T& operator[](const int ind) const { return this->elements[ind]; }
  void operator+=(const T& right) {this->elements.push_back(right);}
};

#pragma pack(1)
struct Nf501  // Альманах
{
  int16_t nka;
  uint8_t num;         // Номер системной точки НКА (255 --- недействительный номер)
  int8_t lit;          // Номер литерной частоты, от 0 до 32; 24 --- недействительная
  uint8_t  n4;         // Число четырехлетних циклов от 1996 г.
  uint16_t na;         // День в четырехлетнем цикле
  long double lambda;  // Гринвичская долгота восходящего узла орбиты в СК ПЗ-90, радианы
  long double lambdaT; // МДВ прохождения восходящего узла орбиты, секунды
  long double dI;      // Поправка к среднему значению наклонения орбиты радианы
  long double dT;      // Поправка к среднему значению драконического периода обращения секунды
  long double ddT;     // Скорость изменения поправки
  long double e;       // Эксцентриситет орбиты
  long double omega;   // Аргумент перигея, радианы
  long double tau;

  Nf501()
  {
    this->nka = UNDEFINE_INT16;
    this->num = UNDEFINE_UINT8;
    this->lit = UNDEFINE_UINT8;
    this->n4  = UNDEFINE_UINT8;
    this->na  = UNDEFINE_UINT16;
    this->lambda  = NAN;
    this->lambdaT = NAN;
    this->dI      = NAN;
    this->dT      = NAN;
    this->ddT     = NAN;
    this->e       = NAN;
    this->omega   = NAN;
    this->tau     = NAN;
  }

  void PrintData()
  {
    std::cout << std::setw(5) << "  NKA = " << static_cast<int16_t>(nka) << '\t'
                              << "  NUM = " << static_cast<uint16_t>(num) << '\t'
                              << "  LIT = " << static_cast<uint16_t>(lit) << '\t'
                              << "   N4 = " << static_cast<uint16_t>( n4) << '\t'
                              << "   Na = " <<                         na << '\t'
                              << "  LYM = " <<                     lambda << '\t'
                              << "LYM_T = " <<                    lambdaT << '\t'
                              << "   dT = " <<                         dT << '\t'
                              << "  ddT = " <<                        ddT << '\t'
                              << "  EXC = " <<                          e << '\t'
                              << "   OM = " <<                      omega << '\t'
                              << "  TAU = " <<                        tau << '\n';
  }

  friend bool operator==(const Nf501& left, const Nf501& other)
  {
    return left.nka     == other.nka     &&
           left.num     == other.num     &&
           left.lit     == other.lit     &&
           left.n4      == other.n4      &&
           left.na      == other.na      &&
           left.lambda  == other.lambda  &&
           left.lambdaT == other.lambdaT &&
           left.dI      == other.dI      &&
           left.dT      == other.dT      &&
           left.ddT     == other.ddT     &&
           left.e       == other.e       &&
           left.omega   == other.omega   &&
           left.tau     == other.tau;
  }
};

typedef SimpleArray<Nf501> Nf501StructList;
#pragma pack()

#pragma pack(1)
struct Almanah
{
  uint8_t num;         // Номер системной точки НКА (255 --- недействительный номер)
  int8_t lit;         // Номер литерной частоты, от 0 до 32; 24 --- недействительная
  uint8_t  n4;         // Число четырехлетних циклов от 1996 г.
  uint16_t na;         // День в четырехлетнем цикле
  long double lambda;  // Гринвичская долгота восходящего узла орбиты в СК ПЗ-90, радианы
  long double lambdaT; // МДВ прохождения восходящего узла орбиты, секунды
  long double dI;      // Поправка к среднему значению наклонения орбиты радианы
  long double dT;      // Поправка к среднему значению драконического периода обращения секунды
  long double ddT;     // Скорость изменения поправки
  long double e;       // Эксцентриситет орбиты
  long double omega;   // Аргумент перигея, радианы
  long double tau;

  Almanah()
  {
    this->num = UNDEFINE_UINT8;
    this->lit = UNDEFINE_UINT8;
    this->n4  = UNDEFINE_UINT8;
    this->na  = UNDEFINE_UINT16;
    this->lambda  = NAN;
    this->lambdaT = NAN;
    this->dI      = NAN;
    this->dT      = NAN;
    this->ddT     = NAN;
    this->e       = NAN;
    this->omega   = NAN;
    this->tau     = NAN;
  }

  void PrintData()
  {
    std::cout << std::setw(5) << "  NUM = " << static_cast<uint16_t>(num) << '\t'
                              << "  LIT = " << static_cast<uint16_t>(lit) << '\t'
                              << "   N4 = " << static_cast<uint16_t>( n4) << '\t'
                              << "   Na = " <<                         na << '\t'
                              << "  LYM = " <<                     lambda << '\t'
                              << "LYM_T = " <<                    lambdaT << '\t'
                              << "   dT = " <<                         dT << '\t'
                              << "  ddT = " <<                        ddT << '\t'
                              << "  EXC = " <<                          e << '\t'
                              << "   OM = " <<                      omega << '\t'
                              << "  TAU = " <<                        tau << '\n';
  }
};
#pragma pack()

#pragma pack(1)
struct ErrorsSettings
{
  int succesful_completion; // Успешное выполнение (ошибок нет)
  int error_empty; // Пустой файл
  int error_miss_file; // Отсутствует определенный файл
  int error_old_almanac; // Старый альманах
  int error_convert_text_to_json; // Ошибка во время конвертации строки в json-объект
  int error_convert_json_to_map; // Ошибка во время конвертации json-объекта в словарь
  // Не правильно заданы координаты широты (end < start)
  int error_set_not_correct_latitude;
  // Не правильно заданы координаты долготы (end < start)
  int error_set_not_correct_longitude;
  // Ошибка, характеризующая бесконечную карту (step == 0)
  int error_null_step;
  // Не правильно задан УМ (вне диапозона)
  int error_set_not_correct_angle_elev;
  // Не удалось создать файл с результатами
  int error_create_result_file;

  /*! Конструктор
   *  Вх. аргументы:
   *    \@param: path_to_file_errors - путь до файла с ошибками
  */
  ErrorsSettings(const std::string& path_to_file_errors);

 private:
  void SwitchNameForValue(const std::vector<std::string>& vec_str);
};
#pragma pack()

#pragma pack(1)
struct PathsFiles
{
  std::string path_errors_file; // Путь до файла с ошибками
  std::string path_alm_file; // Путь до файла с альманахом
  std::string path_di_file; // Путь до файла с ЦИ  
  std::string path_result; // Путь до каталога с результатами
  std::string path_conf_formation_di; // Путь до файла с конфигурационными данными для формирования ЦИ
  // Путь до файла с конфигурационными данными для программы имитации приема альманаха
  std::string path_conf_imitator_receiv_alm;

  /*! Конструктор
   *  Вх. аргументы:
   *    \@param: path_to_file - путь до файла с кофигурационными данными
  */
  PathsFiles(const std::string& path_to_file);

private:
  void SwitchNameForValue(const std::vector<std::string>& vec_str);
};
#pragma pack()

#pragma pack(1)
struct DiSettings
{
  uint16_t num_con_aml; // Значение, с которого начинается условный номер КА
  uint32_t time_di; // Время в сек. на формирование ЦИ

  /*! Конструктор
   *  Вх. аргументы:
   *    \@param: path_to_file - путь до файла с кофигурационными данными
  */
  DiSettings(const std::string& path_to_file);

private:
  void SwitchNameForValue(const std::vector<std::string>& vec_str);
};
#pragma pack()

#pragma pack(1)
struct ImitatorReceivAlmSettings
{
  DiSettings di_sett; // Настроечные параметры для обработки ЦИ
  uint32_t time_simulation; // Время симуляции (имитации приема альманаха)
  int8_t start_latitude; // Начало широты для моделирования в град.
  int8_t end_latitude; // Конец широты для моделирования в град.
  int8_t step_latitude; // Шаг по широте для моделирования в град.
  int16_t start_longitude; // Начало долготы для моделирования в град.
  int16_t end_longitude; // Конец долготы для моделирования в град.
  int8_t step_longitude; // Шаг по долготе для моделирования в град.
  int8_t min_angle_elev; // Минимальный УМ, при котором КА считается видимым
  uint16_t height_pos; //  Высота антенны, принимающая альманах
  // Диапозон корректных значений УМ
  int8_t min_correct_angle_elev;
  int8_t max_correct_angle_elev;
  // Уровень оптимизации при расчете прогноза (рассчета координат КА)
  // 0 - Оптимазация отсутствует, 1 - оптимизация первого уровня,
  // 2 - Оптимизация второго уровня
  uint8_t prog_lvl_opt;
  // Количество параметров в строке с файлом альманаха
  uint8_t count_var_to_str_in_file_alm;
  /* Индексы в файле с альманахом соот. параметрам в первой строке */
  uint8_t ind_time_beg_file_alm; // Время начала моделирования (не используемый параметр)
  uint8_t ind_time_end_file_alm; // Время окончания моделирования (не используемый параметр)
  uint8_t ind_day_rec_file_alm; // День в месяце, в котром был получен альманах
  uint8_t ind_mon_rec_file_alm; // Месяц, в котором был получен альманах
  uint8_t ind_year_rec_file_alm;// Год, в котором был получен альманах
  uint8_t ind_NA_file_alm; // День в четырехлетнем цикле
  uint8_t ind_count_sat_file_alm; // Кол-во КА в альманахе
  /* Индексы в файле с альманахом соот. параметрам альманаха */
  uint8_t ind_liiter; // Номер литеры НКА
  uint8_t ind_ta_lym; // Время восходящего узла НКА
  uint8_t ind_tau_n;
  uint8_t ind_lyma; // Долгота восходящего узла НКА
  uint8_t ind_dia; // Поправка к сред. значению наклонения орбиты НКА
  uint8_t ind_oma; // Аргумент Перигея НКА
  uint8_t ind_epsa; // Эксцентриситет орбиты НКА
  uint8_t ind_dta; // Поправка к среднему значению драконического периода обращения
  uint8_t ind_ddta; // Половинная скорость изменения драконического периода
  // Значение оступа в JSON файле с результатами
  uint8_t value_indent_json_result;

  /*! Конструктор
   *  Вх. аргументы:
   *    \@param: path_to_file_conf_di - путь до файла с конфигурационными данными для обработки ЦИ
   *    \@param: path_to_file_imit_receiv_alm - путь до файла с кофигурационными данными для приема альманаха
  */
  ImitatorReceivAlmSettings(const std::string& path_to_file_conf_di, const std::string& path_to_file_imit_receiv_alm);

private:
  void SwitchNameForValue(const std::vector<std::string>& vec_str);
};
#pragma pack()

#endif // STRUCTS_H

