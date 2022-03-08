#include <fstream>

#include "Parser.hpp"
#include "Functions.hpp"
#include "SettingsAndGlobalConstants.hpp"

/* Parser: public */

int Parser::SetPathFile(std::string path_file)
{
  int output_err = SUCCESFUL_COMPLETION_D;
  if (path_file.size() == 0)
    output_err = ERROR_EMPTY_D;
  else if (!CheckFileExist(path_file))
    output_err = ERROR_MISS_FILE_D;
  else
    this->path_to_file = path_file;
  return output_err;
}

/* Parser:private */

int AlmanahParser::ReadFile()
{
  int output_err = SUCCESFUL_COMPLETION_D;
  bool f_file_exit = CheckFileExist(this->path_to_file);
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
      for (uint8_t ind_r = 0; ind_r < COUNT_VAR_TO_STR_IN_FILE_ALM; ind_r++)
      {
        switch(ind_r)
        {
        case IND_DAY_REC_FILE_ALM:
          file >> day;
          break;
        case IND_MON_REC_FILE_ALM:
          file >> mon;
          break;
         case IND_YEAR_REC_FILE_ALM:
          file >> year;
          break;
        case IND_NA_FILE_ALM:
          file >> na;
          break;
        case IND_COUNT_SAT_FILE_ALM:
          file >> count_sat;
          break;
         default:
          file >> temp;
          break;
        }
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
    output_err = ERROR_MISS_FILE_D;
  return output_err;
}
