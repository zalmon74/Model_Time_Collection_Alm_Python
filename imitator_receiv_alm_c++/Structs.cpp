#include <fstream>

#include "Functions.hpp"
#include "Structs.hpp"

ErrorsSettings::ErrorsSettings(const std::string& path_to_file_errors)
{
  bool f_exist = CheckFileExist(path_to_file_errors);
  if (f_exist)
  {
    std::ifstream file(path_to_file_errors);
    if (file.is_open())
    {
      std::string str_file;
      while(std::getline(file, str_file))
      {
        auto vec_str = SplitString(str_file);
        this->SwitchNameForValue(vec_str);
      }
    }
    else
      throw std::invalid_argument("Error path file or file empty: " + path_to_file_errors);
  }
  else
    throw std::invalid_argument("Error path file or file empty: " + path_to_file_errors);
}

void ErrorsSettings::SwitchNameForValue(const std::vector<std::string> &vec_str)
{
  if (vec_str.size() == 0)
    return;
  int value = std::atoi(vec_str[1].c_str());
  if (vec_str[0] == "SUCCESFUL_COMPLETION")
    this->succesful_completion = value;
  else if (vec_str[0] == "ERROR_EMPTY")
    this->error_empty = value;
  else if (vec_str[0] == "ERROR_MISS_FILE")
    this->error_miss_file = value;
  else if (vec_str[0] == "ERROR_OLD_ALMANAC")
    this->error_old_almanac = value;
  else if (vec_str[0] == "ERROR_CONVERT_TEXT_TO_JSON")
    this->error_convert_text_to_json = value;
  else if (vec_str[0] == "ERROR_CONVERT_JSON_TO_MAP")
    this->error_convert_json_to_map = value;
  else if (vec_str[0] == "ERROR_SET_NOT_CORRERCT_LATITUDE")
    this->error_set_not_correct_latitude = value;
  else if (vec_str[0] == "ERROR_SET_NOT_CORRERCT_LONGITUDE")
    this->error_set_not_correct_longitude = value;
  else if (vec_str[0] == "ERROR_NULL_STEP")
    this->error_null_step = value;
  else if (vec_str[0] == "ERROR_SET_NOT_CORRECT_ANGLE_ELEV")
    this->error_set_not_correct_angle_elev = value;
  else if (vec_str[0] == "ERROR_CREATE_RESULT_FILE")
    this->error_create_result_file = value;
}


PathsFiles::PathsFiles(const std::string& path_to_file)
{
  bool f_exist = CheckFileExist(path_to_file);
  if (f_exist)
  {
    std::ifstream file(path_to_file);
    if (file.is_open())
    {
      std::string str_file;
      while(std::getline(file, str_file))
      {
        auto vec_str = SplitString(str_file);
        this->SwitchNameForValue(vec_str);
      }
    }
    else
      throw std::invalid_argument("Error path file or file empty: " + path_to_file);
  }
  else
    throw std::invalid_argument("Error path file or file empty: " + path_to_file);
}

void PathsFiles::SwitchNameForValue(const std::vector<std::string>& vec_str)
{
  if (vec_str.size() == 0)
    return;
  std::string path = vec_str[1].substr(1);
  if (vec_str[0] == "PATH_ERRORS_FILE ")
    this->path_errors_file = path;
  else if (vec_str[0] == "ALMANAH_FILE ")
    this->path_alm_file = path;
  else if (vec_str[0] == "RESULT_CI_FORMATION_FILE ")
    this->path_di_file = path;
  else if (vec_str[0] == "PATH_CONF_FORMATION_CI ")
    this->path_conf_formation_di = path;
  else if (vec_str[0] == "RESULT_MODELING_RECIVE ")
    this->path_result = path;
  else if (vec_str[0] == "PATH_CONF_IMITATOR_RECEIV_ALM ")
    this->path_conf_imitator_receiv_alm = path;
}

DiSettings::DiSettings(const std::string& path_to_file)
{
  bool f_exist = CheckFileExist(path_to_file);
  if (f_exist)
  {
    std::ifstream file(path_to_file);
    if (file.is_open())
    {
      std::string str_file;
      while(std::getline(file, str_file))
      {
        auto vec_str = SplitString(str_file);
        this->SwitchNameForValue(vec_str);
      }
    }
    else
      throw std::invalid_argument("Error path file or file empty: " + path_to_file);
  }
  else
    throw std::invalid_argument("Error path file or file empty: " + path_to_file);
}

void DiSettings::SwitchNameForValue(const std::vector<std::string>& vec_str)
{
  if (vec_str.size() == 0)
    return;
  int value = std::atoi(vec_str[1].c_str());
  if (vec_str[0] == "MAX_TIME ")
    this->time_di = value;
  else if (vec_str[0] == "NUM_CON_ALM ")
    this->num_con_aml = value;
}

ImitatorReceivAlmSettings::ImitatorReceivAlmSettings(const std::string& path_to_file_conf_di
                                                    ,const std::string& path_to_file_imit_receiv_alm) : di_sett(path_to_file_conf_di)
{
  bool f_exist = CheckFileExist(path_to_file_imit_receiv_alm);
  if (f_exist)
  {
    std::ifstream file(path_to_file_imit_receiv_alm);
    if (file.is_open())
    {
      std::string str_file;
      while(std::getline(file, str_file))
      {
        auto vec_str = SplitString(str_file);
        this->SwitchNameForValue(vec_str);
      }
    }
    else
      throw std::invalid_argument("Error path file or file empty: " + path_to_file_imit_receiv_alm);
  }
  else
    throw std::invalid_argument("Error path file or file empty: " + path_to_file_imit_receiv_alm);
}

void ImitatorReceivAlmSettings::SwitchNameForValue(const std::vector<std::string>& vec_str)
{
  if (vec_str.size() == 0)
    return;
  int value = std::atoi(vec_str[1].c_str());
  if (vec_str[0] == "TIME_SIMULATION ")
    this->time_simulation = value;
  else if (vec_str[0] == "START_LATITUDE ")
    this->start_latitude = value;
  if (vec_str[0] == "END_LATITUDE ")
    this->end_latitude = value;
  else if (vec_str[0] == "STEP_LATITUDE ")
    this->step_latitude = value;
  if (vec_str[0] == "START_LONGITUDE ")
    this->start_longitude = value;
  else if (vec_str[0] == "END_LONGITUDE ")
    this->end_longitude = value;
  if (vec_str[0] == "STEP_LONGITUDE ")
    this->step_longitude = value;
  else if (vec_str[0] == "MIN_ANGLE_ELEV ")
    this->min_angle_elev = value;
  if (vec_str[0] == "HEIGHT_POS ")
    this->height_pos = value;
  else if (vec_str[0] == "MIN_CORRECT_ANGLE_ELEV ")
    this->min_correct_angle_elev = value;
  if (vec_str[0] == "MAX_COORECT_ANGLE_ELEV ")
    this->max_correct_angle_elev = value;
  else if (vec_str[0] == "PROG_LVL_OPT ")
    this->prog_lvl_opt = value;
  if (vec_str[0] == "COUNT_VAR_TO_STR_IN_FILE_ALM ")
    this->count_var_to_str_in_file_alm = value;
  else if (vec_str[0] == "IND_TIME_BEG_FILE_ALM ")
    this->ind_time_beg_file_alm = value;
  if (vec_str[0] == "IND_TIME_END_FILE_ALM ")
    this->ind_time_end_file_alm = value;
  else if (vec_str[0] == "IND_DAY_REC_FILE_ALM ")
    this->ind_day_rec_file_alm = value;
  if (vec_str[0] == "IND_MON_REC_FILE_ALM ")
    this->ind_mon_rec_file_alm = value;
  else if (vec_str[0] == "IND_YEAR_REC_FILE_ALM ")
    this->ind_year_rec_file_alm = value;
  if (vec_str[0] == "IND_NA_FILE_ALM ")
    this->ind_NA_file_alm = value;
  else if (vec_str[0] == "IND_COUNT_SAT_FILE_ALM ")
    this->ind_count_sat_file_alm = value;
  if (vec_str[0] == "IND_LITTER ")
    this->ind_liiter = value;
  else if (vec_str[0] == "IND_TA_LYM ")
    this->ind_ta_lym = value;
  if (vec_str[0] == "IND_TAU_N ")
    this->ind_tau_n = value;
  else if (vec_str[0] == "IND_LYMA ")
    this->ind_lyma = value;
  if (vec_str[0] == "IND_DIA ")
    this->ind_dia = value;
  else if (vec_str[0] == "IND_OMA ")
    this->ind_oma = value;
  if (vec_str[0] == "IND_EPSA ")
    this->ind_epsa = value;
  else if (vec_str[0] == "IND_DTA ")
    this->ind_dta = value;
  else if (vec_str[0] == "IND_DDTA ")
    this->ind_ddta = value;
  else if (vec_str[0] == "VALUE_INDENT_JSON_RESULT ")
    this->value_indent_json_result = value;
}
