/* Файл описывает структуру класса имитатора */

#ifndef ImitatorReceivAlm_HPP
#define ImitatorReceivAlm_HPP

#include <math.h>
#include <vector>
#include <array>

#include <Almanah.hpp>

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
   *  \@param:  0 = Успешное завершение
   *           -2 = Файл c альманахом по данному пути невозможно открыть/не существует
  */
  int SetPathAlmFile(std::string path_alm);

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

private:

  /* Поля */

  std::string path_alm_file; // Путь до файла с альманахом
  std::string path_di_file; // Путь до файла с сформированной ЦИ

  std::vector<Almanah> vec_alm; // Вектор со значениями альманаха для каждого КА
  map_for_di di_system; // Словарь, который хранит в себе ЦИ, которую передает данная система

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

  /*! Метод перевода даты в секунды с 1996 года
   * Вх. аргументы:
   *  @\param: date_rec_alm - дата, которую необходимо перевести в секунды
   * Вых. аргументы:
   *  @\param: sec_of_1996 - переведенная дата в секунды
  */
  double ConvertDateOfSeconds1996(Date date_rec_alm);

  /*! Метод расчета координат всех КА в системе
   * Вх. аргументы:
   *  \@param: curr_time - текущее время, на которое необходимо посчитать координаты КА, сек
   *  \@param: vec_alm - вектор с альманахом для каждого КА
   *  \@param: vec_sat_coor - ссылка на вектор с рассчитанными координатами для каждого КА в системе
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



};

#endif // ImitatorReceivAlm_HPP
