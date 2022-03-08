/* Файл содержит различные вспомогательные функции для работы имитатора */

#ifndef FUNCTIONS_HPP
#define FUNCTIONS_HPP

#include <string>

#include "ImitatorReceivAlm.hpp"
#include "json.hpp"

using json = nlohmann::json;

/*! Функция определения наличия файла по заданному пути
 *  Вх аргументы:
 *    \@param: path_file - путь до файла
 *  Вых. аргументы:
 *    \@param: True - Файл имеется и открывается, False - файл невозможно открыть/отсутствует
*/
bool CheckFileExist(std::string path_file);

/*! Функция перевода координат из геодезической СК в геоцентрическую СК.
 *  Вх аргументы:
 *    \@param: coor_blh - координаты в геодезической СК, которые необходимо перевести, [рад.]
 *  Вых. аргументы:
 *    \@param: coor_xyz - координаты в геоцентрической СК, [км.]
*/
Coordinates BLH2XYZ(Coordinates coor_blh);

/*! Функция вычисления УМ между двумя точками (между КА и прием. антенной)
 *  Вх аргументы:
 *    \@param: coor_1 - первые координаты (КА), [км]
 *    \@param: coor_2 - вторые координаты (Прием. антенна), [км]
 *  Вых. аргументы:
 *    \@param: um - рассчитанный УМ, [град.]
*/
double CalculationAngleElevation(Coordinates coor_1, Coordinates coor_2);

/*! Функция определения текущей даты в виде строки YYYY_M_D
 *  Вх. аргументы:
 *    \@param: delimitor - разделить между числами
 *  Вых. аргументы:
 *    \@param: cur_date - текущая дата в виде строки
*/
std::string DeterminingCurrentDateSTR(std::string delimitor);

/*! Функция сохранения json объекта в файл
 *  Вх. аргументы:
 *    \@param: obj - объект, который необходимо сохранить в файл
 *    \@param: path_file - путь до файла
 *  Вых. аргументы:
 *    \@param - Ошибки
*/
int SaveJSONObjToFile(json obj, std::string path_file);

/*! Функция разделения строки по подстроками по входному разделителю
 *  Вх. аргументы:
 *    \@param: str - строка, которую необходимо разделить
 *    \@param: delim - разделитель
 *  Вых. аргументы:
 *    \@param: vec_str - вектор, который содержит подстроки
*/
std::vector<std::string> SplitString(const std::string &str, char delim='=');

#endif // FUNCTIONS_HPP
