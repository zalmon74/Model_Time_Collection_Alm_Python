#include <fstream>
#include <ctime>

#include "Functions.hpp"

bool CheckFileExist(std::string path_file)
{
  bool output = true;
  // Открываем файл для проверка его наличия
  std::ifstream file(path_file);
  if (!file.is_open())
    output = false;
  file.close();
  return output;
}

Coordinates BLH2XYZ(Coordinates coor_blh)
{
  Coordinates coor_xyz;
  double N = R_EARHT/sqrt(1-E_EARHT*E_EARHT*sin(coor_blh[0]));
  coor_xyz[0] = (N+coor_blh[2])*cos(coor_blh[0])*cos(coor_blh[1]);
  coor_xyz[1] = (N+coor_blh[2])*cos(coor_blh[0])*sin(coor_blh[1]);
  coor_xyz[2] = ((1-E_EARHT*E_EARHT)*N+coor_blh[2])*sin(coor_blh[0]);
  return coor_xyz;
}

double CalculationAngleElevation(Coordinates coor_1, Coordinates coor_2)
{
  double angle_elev = NAN;
  //Вычисляем радиус-вектор
  double rang = 0;
  Coordinates coef;
  for (uint8_t i = 0; i < 3; i++)
  {
    coef[i] = coor_1[i]-coor_2[i];
    rang += (coef[i]*coef[i]);
  }
  rang = sqrt(rang);
  double numerator = 0, denominator = 0;
  for (uint8_t i = 0; i < 3; i++)
  {
    coef[i] /= rang;
    numerator += coef[i]*coor_2[i];
    denominator += (coor_2[i]*coor_2[i]);
  }
  denominator = sqrt(denominator);
  // Рассчитываем УМ
  angle_elev = asin(numerator/denominator)*180/M_PI;
  return angle_elev;
}

std::string DeterminingCurrentDateSTR(std::string delimitor)
{
  // Формируем объект времени
  std::time_t timer = std::time(0);
  // Определяем текущее время
  std::tm* now = std::localtime(&timer);
  // Формируем строку с датой
  std::string date_str = std::to_string(now->tm_year + 1900)+delimitor+
                         std::to_string(now->tm_mon+1)+delimitor+
                         std::to_string(now->tm_mday);
  return date_str;
}
