#include <fstream>

#include "Parser.hpp"
#include "Functions.hpp"
#include "SettingsAndGlobalConstants.hpp"

/* Parser: public */

int Parser::SetPathFile(std::string path_file)
{
  int output_err = errors.succesful_completion;
  if (path_file.size() == 0)
    output_err = errors.error_empty;
  else if (!CheckFileExist(path_file))
    output_err = errors.error_miss_file;
  else
    this->path_to_file = path_file;
  return output_err;
}

/* Parser:private */

int AlmanahParser::ReadFile()
{
  int output_err = errors.succesful_completion;
  bool f_file_exit = CheckFileExist(this->path_to_file);
  ImitatorReceivAlmSettings settings(PathsFiles(STD_PATH_PATHS).path_di_file
                                    ,PathsFiles(STD_PATH_PATHS).path_conf_imitator_receiv_alm);
  if (f_file_exit)
  {
    // Считываем файл
    std::ifstream file(this->path_to_file);
    if (file.is_open())
    {
      // Считанные параметры
      uint16_t day = UNDEFINE_UINT8;
      uint16_t mon = UNDEFINE_UINT8;
      uint16_t count_sat = UNDEFINE_UINT8;
      uint16_t year = UNDEFINE_UINT16;
      uint16_t na = UNDEFINE_UINT16;
      double temp = NAN;
      // Считываем первую строку с файла (В каждой строке файла COUNT_VAR_TO_STR_IN_FILE_ALM)
      for (uint8_t ind_r = 0; ind_r < settings.count_var_to_str_in_file_alm; ind_r++)
      {
        if (ind_r == settings.ind_day_rec_file_alm)
          file >> day;
        else if (ind_r == settings.ind_mon_rec_file_alm)
          file >> mon;
         else if (ind_r == settings.ind_year_rec_file_alm)
          file >> year;
        else if (ind_r == settings.ind_NA_file_alm)
          file >> na;
        else if (ind_r == settings.ind_count_sat_file_alm)
          file >> count_sat;
         else
          file >> temp;
      }
      // Рассчитываем число четырехлетних циклов от 1996 г.
      uint8_t n4 = static_cast<uint8_t>((year-1996)/4);
      // Цикл по КА
      for (uint8_t num_sat = 1; num_sat <= count_sat; num_sat++)
      {
        Nf501 alm;
        alm.num = num_sat;
        alm.n4  = n4;
        alm.na  = na;
        int16_t temp_lit;
        file >> temp_lit;
        alm.lit = static_cast<int8_t>(temp_lit);
        file >> alm.lambdaT;
        file >> alm.tau;
        file >> alm.lambda;
        file >> alm.dI;
        file >> alm.omega;
        file >> alm.e;
        file >> alm.dT;
        file >> alm.ddT;
        this->almanah += alm;
      }
    }
  }
  else
    output_err = errors.error_miss_file;
  return output_err;
}
