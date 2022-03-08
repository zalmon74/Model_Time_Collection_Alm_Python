#include <fstream>
#include <ctime>

#include "Functions.hpp"
#include "SettingsAndGlobalConstants.hpp"

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
  double rang = sqrt(
                      (coor_1[0]-coor_2[0])*(coor_1[0]-coor_2[0])+
                      (coor_1[1]-coor_2[1])*(coor_1[1]-coor_2[1])+
                      (coor_1[2]-coor_2[2])*(coor_1[2]-coor_2[2])
                    );
  // Коэффициенту [0] = kx, [1] = ky, [2] = kz
  Coordinates coef;  
  coef[0] = (coor_1[0]-coor_2[0])/rang;
  coef[1] = (coor_1[1]-coor_2[1])/rang;
  coef[2] = (coor_1[2]-coor_2[2])/rang;
  // Рассчитываем УМ
  angle_elev = asin(
                      (coef[0]*coor_2[0]+coef[1]*coor_2[1]+coef[2]*coor_2[2])/
                      sqrt(coor_2[0]*coor_2[0]+coor_2[1]*coor_2[1]+coor_2[2]*coor_2[2])
                   );

  return angle_elev*180/M_PI;
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

int SaveJSONObjToFile(json obj, std::string path_file)
{
  int output_err = SUCCESFUL_COMPLETION_D;
  std::string result_str = obj.dump(VALUE_INDENT_JSON_RESULT);
  // Определяем текущую дату в виде строки
  std::string cur_date_str = DeterminingCurrentDateSTR("_");
  // Записываем результаты в файл
  std::ofstream result_file(path_file+cur_date_str+".json", std::ios_base::out);
  if (result_file.is_open())
    result_file << result_str;
  else
    output_err = ERROR_CREATE_RESULT_FILE;
  result_file.close();
  return output_err;
}

std::vector<std::string> SplitString(const std::string &str, char delim)
{
  std::vector<std::string> vec_str;
  std::stringstream ss(str);
  std::string sub_str;
  while (std::getline(ss, sub_str, delim))
    vec_str.push_back(sub_str);
  return vec_str;
}
