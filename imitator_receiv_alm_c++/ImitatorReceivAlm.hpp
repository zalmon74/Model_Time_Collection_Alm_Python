/* Файл описывает структуру класса имитатора */

#ifndef ImitatorReceivAlm_HPP
#define ImitatorReceivAlm_HPP

#include <math.h>
#include <vector>
#include <list>
#include <array>

#include "Almanah.hpp"

/* Структура для описание координатов КА */
struct Coordinates : std::array<double,3>
{
  // Конструктор
  Coordinates()
  {
    this->at(0) = NAN;
    this->at(1) = NAN;
    this->at(2) = NAN;
  }
};
/* Структура для описание даты */
struct Date : std::array<uint16_t, 3>
{
  // Конструктор
  Date()
  {
    this->at(0) = UNDEFINE_UINT16; // День
    this->at(1) = UNDEFINE_UINT16; // Месяц
    this->at(2) = UNDEFINE_UINT16; // Год
  }
};

class ImitatorReceivAlm
{
public:
  /* Конструкторы */
  ImitatorReceivAlm();

  /* Сеттеры */
  /*! Сеттер для установки пути до файла с альманахом
   * Вх. аргументы:
   *  \@param: path_alm - путь до файла с альманахом, который необходимо установить в имитаторе
   * Вых. аргументы:
   *  \@param: SUCCESSFUL_COMPLETION = Успешное завершение
   *           ERROR_MISS_ALM_FILE = Файл c альманахом по данному пути невозможно открыть/не существует
  */
  int SetPathAlmFile(std::string path_alm);

  /*! Сеттер для установки пути до файла с ЦИ
   * Вх. аргументы:
   *  \@param: path_di - путь до файла с ЦИ, который необходимо установить в имитаторе
   * Вых. аргументы:
   *  \@param: SUCCESSFUL_COMPLETION = Успешное завершение
   *           ERROR_MISS_DI_FILE = Файл c альманахом по данному пути невозможно открыть/не существует
  */
  int SetPathDIFile(std::string path_di);

  /*! Сеттер для установки парамтеров широты для формирования карты моделирования
   * Вх. аргументы:
   *  \@param: start - начало широты
   *  \@param: end - конец широты
   *  \@param: step - шаг по широте
   * Вых. аргументы:
   *  \@param: SUCCESSFUL_COMPLETION = Успешное завершение
   *           ERROR_SET_NOT_CORRERCT_LATITUDE = Не правильно заданы координаты широты (end < start)
  */
  int SetMapCoordinatesLatitude(int8_t start, int8_t end, uint8_t step);

  /*! Сеттер для установки парамтеров долготы для формирования карты моделирования
   * Вх. аргументы:
   *  \@param: start - начало долготы
   *  \@param: end - конец долготы
   *  \@param: step - шаг по долготе
   * Вых. аргументы:
   *  \@param: SUCCESSFUL_COMPLETION = Успешное завершение
   *           ERROR_SET_NOT_CORRERCT_LONGITUDE = Не правильно заданы координаты долготы (end < start)
  */
  int SetMapCoordinatesLongitude(int16_t start, int16_t end, uint8_t step);

  /*! Сеттер для установки минимального УМ
   * Вх. аргументы:
   *  \@param: min_angle_elev - минимальный УМ, котором КА считается видимым [град.]
   *                            диапозон [MIN_CORRECT_ANGLE_ELEV, MAX_CORRECT_ANGLE_ELEV]
   * Вых. аргументы:
   *  \@param: SUCCESSFUL_COMPLETION = Успешное завершение
   *           ERROR_SET_NOT_CORRECT_ANGLE_ELEV = Не правильно задан УМ (вне диапозона)
  */
  int SetMinAngleElev(double angle_elev);

  /*! Сеттер для установки времени моделирования
   * Вх. аргументы:
   *  \@param: time - время, которое необходимо установить, [сек.]
  */
  void SetTimeSimulation(uint32_t time) {this->time_simulation = time;}

  /*! Сеттер для пути сохранения файла с результатами
   * Вх. аргументы:
   *  \@param: path_result_file - путь до файла с результатами
  */
  void SetPathResultFile(std::string path_result_file) {this->path_result_file = path_result_file; }

  /*! Метод для запуска имитатора
   * Вых. аргументы (Ошибки):
   *                          SUCCESSFUL_COMPLETION = Успешное завершение
   *                          ERROR_OLD_ALM = Старый альманах (Альманах устарел больше чем на 90 дней)
   *                          ERROR_MISS_ALM_FILE = Файл c альманахом по заданному пути
   *                                                невозможно открыть/не существует
   *                          ERROR_MISS_DI_FILE = Файл c ЦИ по данному пути невозможно открыть/не существует
   *                          ERROR_CONVERT_TEXT_TO_JSON = Ошибка при конвертировании текста в JSON объект
   *                          ERROR_CONVERT_JSON_TO_MAP = Ошибка при конвертации JSON объекта в словарь
  */
  int StartImitator();

  /*! Метод сохранения полученных результатов в файл */
  int SaveResultToJSONFile();

private:

  /* Поля */

  std::string path_alm_file; // Путь до файла с альманахом
  std::string path_di_file; // Путь до файла с сформированной ЦИ
  std::string path_result_file; // Путь до файла с результатами

  std::vector<Almanah> vec_alm; // Вектор со значениями альманаха для каждого КА
  map_for_di di_system; // Словарь, который хранит в себе ЦИ, которую передает данная система

  // Словарь, который содежрит время приема альманаха для конкретной точки
  // first = координаты точки типа BL
  // second = время приема
  std::map<bl_coor_point, int> dic_time_rec_alm;
  // Словарь, который будет содержать список времен приема полного альманаха
  // first = координаты точки типа BL
  // second = список времен
  std::map<bl_coor_point, std::list<int>> dic_list_time_rec_alm;
  // Словарь, который будет содержать флаги приема альманаха для соот. точки
  // first = координаты точки типа BL
  // second = список времен
  std::map<bl_coor_point, std::vector<bool>> dic_flag_rec_alm;

  uint32_t time_simulation; // Время моделирования, [сек]
  uint32_t time_start_calculation_coor; // Начальное время на которое необходимо рассчитывать коориданты КА, [сек]

  /* Широта изменяется в диапозоне [-90:90] */
  int8_t  start_latitude;   // Начало широты для моделирования, [град.]
  int8_t  end_latitude;     // Конец широты для моделирования, [град.]
  uint8_t step_latitude;    // Шаг по широте, [град.]
  /* Долгота изменяется в диапозоне [-180:180] */
  int16_t start_longitude; // Начало долготе для моделирования, [град.]
  int16_t end_longitude;   // Конец долготе для моделирования, [град.]
  uint8_t step_longitude;  // Шаг по долготе, [град.]
  // Минимальный УМ, при котором КА считается видимым
  double min_angle_elev;

  /* Методы */

  /*! Метод считывания данные альманаха с файла
   * Вх. аргументы:
   *  \@param: path_alm_file - путь до файла с альманахом
   *  \@param: vec_alm - ссылка на вектор с альманахом, который считан с файла
   *  \@param: date_rec_alm - хранит в себе дату измерения альманаха
   * Вых. аргументы:
   *  \@param:  SUCCESSFUL_COMPLETION = Успешное завершение
   *            ERROR_MISS_ALM_FILE = Файл c альманахом по данному пути невозможно открыть/не существует
  */
  int ReadDataAlmFromFile(std::string path_alm_file, std::vector<Almanah>& vec_alm, Date& date_rec_alm);

  /*! Метод чтения json файла с ЦИ для текущей конфигурации системы
   * Вх. аргументы:
   *  \@param: path_di_file - путь до файла с ЦИ
   *  \@param: text_in_file - указатель на считанный текст из файла с ЦИ
   * Вых. аргументы:
   *  \@param: SUCCESSFUL_COMPLETION = Успешное завершение
   *           ERROR_MISS_DI_FILE = Файл c ЦИ по данному пути невозможно открыть/не существует
  */
  int ReadDIFromFile(std::string path_di_file, char*& text_in_file);

  /*! Метод формирования объекта map из текста
   * Вх. аргументы:
   *  @\param: text - указатель на текст, который необходимо преобразовать
   *  @\param: di - сформированный map из текста
   * Вых. аргументы:
   *  @\param: SUCCESSFUL_COMPLETION = Успешное завершение
   *           ERROR_CONVERT_TEXT_TO_JSON = Ошибка при конвертировании текста в JSON объект
   *           ERROR_CONVERT_JSON_TO_MAP = Ошибка при конвертации JSON объекта в словарь
  */
  int Text2MapWithJSONObj(char* text, map_for_di& di);

  /*! Метод перевода даты в секунды с 2000 года
   * Вх. аргументы:
   *  @\param: date_rec_alm - дата, которую необходимо перевести в секунды
   * Вых. аргументы:
   *  @\param: sec_of_2000 - переведенная дата в секунды
  */
  double ConvertDateOfSeconds2000(Date date_rec_alm);

  /*! Метод, который создает словари (map) необходимые для моделирования */
  void FormationAllDic();

  /*! Метод, который создает словарь (map), который будет содержать время приема текущего альманаха
   *  для каждой точки */
  void FormationDicTimeRecAlm(bl_coor_point cur_point);

  /*! Метод, который создает словарь (map), который будет содержать список времен полного альманаха */
  void FormationDicListRecAlm(bl_coor_point cur_point);

  /*! Метод, который создает словарь (map), который будет содержать флаги приема альманаха для соот. точки */
  void FormationDicFlagRecAlm(bl_coor_point cur_point);

  /*! Метод моделирования принятия альманаха
   *  Вых. аргументы:
   *    @\param: SUCCESSFUL_COMPLETION = Успешное завершение
  */
  int ModelingReceivAlm();

  /*! Метод моделирования принятия альманаха для одной точки
   *  Вх. аргументы:
   *    @\param: time - время моделирования
   *    @\param: vec_coor_all_sat - вектор, который хранит в себе координаты всех КА
   *    @\param: coor_bl_point - координаты точки типа BL
   *  Вых. аргументы:
   *    @\param: SUCCESSFUL_COMPLETION = Успешное завершение
  */
  int ModelingReceivAlmOnePoint(uint32_t time, std::vector<Coordinates>& vec_coor_all_sat, bl_coor_point coor_bl_point);

  /*! Метод расчета координат всех КА в системе
   * Вх. аргументы:
   *  \@param: curr_time - текущее время, на которое необходимо посчитать координаты КА, сек
   *  \@param: vec_alm - вектор с альманахом для каждого КА
   *  \@param: vec_sat_coor - ссылка на вектор с рассчитанными координатами для каждого КА в системе [км.]
   * Вых. аргументы:
   *  @\param: SUCCESSFUL_COMPLETION = Успешное завершение
   *           ERROR_OLD_ALM = Старый альманах (Альманах устарел больше чем на 90 дней)
  */
  int CalculationCoordinatesAllSat(uint32_t curr_time, const std::vector<Almanah>& vec_alm
                                  ,std::vector<Coordinates>& vec_sat_coor);

  /*! Метод расчета координат КА
   * Вх. аргументы:
   *  \@param: curr_time - текущее время, на которое необходимо посчитать координаты КА, сек
   *  \@param: almanah - альманах, по которому необходимо рассчитать координаты КА
   *  \@param: sat_coor - ссылка на объект с рассчитанными координатами, м.
   * Вых. аргументы:
   *  \@param: SUCCESSFUL_COMPLETION = Успешное завершение
   *           ERROR_OLD_ALM = Старый альманах (Альманах устарел больше чем на 90 дней)
   *
  */
  int CalcultionCoordinatesSat(uint32_t curr_time, const Almanah& almanah, Coordinates& sat_coor);

  /*! Метод определения списка видимости КА в заданной точке
   *  Вх. аргументы:
   *    \@param: vec_sat_coor - ссылка на вектор с рассчитанными координатами для каждого КА в системе, [км.]
   *    \@param: coor_point - координат антенны XYZ, [км.]
   *  Вых. аргументы:
   *    \@param: список видимых КА
  */
  std::list<uint8_t> DefinitionVisibleSat(std::vector<Coordinates>& vec_sat_coor, Coordinates coor_point);

  /*! Метод заполнения вектора с принятыми альманахами КА для опред. точки
   *  Вх. аргументы:
   *    \@param: time - текущее время, [сек]
   *    \@param: list_vis_sat - список видимых КА
   *    \@param: cur_point - текущие координаты точки
  */
  void PassingStr(uint32_t time, std::list<uint8_t>& list_vis_sat, bl_coor_point cur_point);

};

#endif // ImitatorReceivAlm_HPP
