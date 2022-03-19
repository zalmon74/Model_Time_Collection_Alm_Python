
#include <fstream>

#include "ImitatorReceivAlm.hpp"
#include "json.hpp"
#include "Functions.hpp"
#include "Parser.hpp"

using json = nlohmann::json;

/* Конструкторы */
ImitatorReceivAlm::ImitatorReceivAlm() : path_files(STD_PATH_PATHS), errors(this->path_files.path_errors_file)
                                       , settings(this->path_files.path_conf_formation_di
                                                 ,this->path_files.path_conf_imitator_receiv_alm)
{ }

/* Реализация public методов */

int ImitatorReceivAlm::StartImitator()
{
  int output_err = errors.succesful_completion;

  // Считываем ЦИ с файла
  char* p_text_from_file = nullptr;
  output_err = ReadDIFromFile(this->path_files.path_di_file, p_text_from_file);
  // Конвертиурем Текст в объект типо map
  output_err = Text2MapWithJSONObj(p_text_from_file, this->di_system);
  // Отчищаем память, выделенную под текст
  delete [] p_text_from_file;
  // Дата измерения альманаха
  Date date_rec_alm;
  // Считываем альманах системы c файла
  output_err = ReadDataAlmFromFile(this->path_files.path_alm_file, this->vec_alm, date_rec_alm);
  // Рассчитываем кол-во секунд от 1996 года для расчета определения координат КА
  double second_rec_alm = ConvertDateOfSeconds2000(date_rec_alm);
  this->time_start_calculation_coor = static_cast<uint32_t>(second_rec_alm);
  // Формируем необходимые словари для моделировния
  FormationAllDic();
  // Моделируем принятие альманаха
  ModelingReceivAlm();

  return output_err;
}

/* Сеттеры */

int ImitatorReceivAlm::SetMapCoordinatesLatitude(int8_t start, int8_t end, uint8_t step)
{
  int output_err = errors.succesful_completion;
  if (end < start)
    output_err = errors.error_set_not_correct_latitude;
  else if (step == 0)
    output_err = errors.error_null_step;
  else
  {
    this->settings.start_latitude = start;
    this->settings.end_latitude   = end;
    this->settings.step_latitude  = step;
  }
  return output_err;
}

int ImitatorReceivAlm::SetMapCoordinatesLongitude(int16_t start, int16_t end, uint8_t step)
{
  int output_err = errors.succesful_completion;
  if (end < start)
    output_err = errors.error_set_not_correct_longitude;
  else if (step == 0)
    output_err = errors.error_null_step;
  else
  {
    this->settings.start_longitude = start;
    this->settings.end_longitude   = end;
    this->settings.step_longitude  = step;
  }
  return output_err;
}

int ImitatorReceivAlm::SetMinAngleElev(double angle_elev)
{
  int output_err = errors.succesful_completion;
  if ((angle_elev < this->settings.min_correct_angle_elev) || (angle_elev > this->settings.max_correct_angle_elev))
    output_err = errors.error_set_not_correct_angle_elev;
  else
    this->settings.min_angle_elev = angle_elev;
  return output_err;
}

int ImitatorReceivAlm::SaveResultToJSONFile()
{
  int output_err = 0;
  // Преобразовываем результаты в текст
  json result_json_obj = this->dic_list_time_rec_alm;
  SaveJSONObjToFile(result_json_obj, this->path_files.path_result, this->settings.value_indent_json_result);
  return output_err;
}

/* Реализация private методов */

int ImitatorReceivAlm::ReadDataAlmFromFile(std::string path_alm_file, std::vector<Almanah>& vec_alm, Date& date_rec_alm)
{
  int output_err = errors.succesful_completion;
  // Предварительно отчищаем вектор с альманахом системы
  vec_alm.clear();
  // Считываем данные с файла
  std::ifstream file(path_alm_file);
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
    for (uint8_t ind_r = 0; ind_r < this->settings.count_var_to_str_in_file_alm; ind_r++)
    {
      if (ind_r == this->settings.ind_day_rec_file_alm)
        file >> day;
      else if (ind_r == this->settings.ind_mon_rec_file_alm)
        file >> mon;
       else if (ind_r == this->settings.ind_year_rec_file_alm)
        file >> year;
      else if (ind_r == this->settings.ind_NA_file_alm)
        file >> na;
      else if (ind_r == this->settings.ind_count_sat_file_alm)
        file >> count_sat;
       else
        file >> temp;
    }
    // Заполняем структуру с датой
    date_rec_alm[0] = day;
    date_rec_alm[1] = mon;
    date_rec_alm[2] = year;
    // Рассчитываем число четырехлетних циклов от 1996 г.
    uint8_t n4 = static_cast<uint8_t>((year-1996)/4);
    // Цикл по КА
    for (uint8_t num_sat = 1; num_sat <= count_sat; num_sat++)
    {
      Almanah alm;
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
      vec_alm.push_back(alm);
    }
  }
  else
    output_err = errors.error_miss_file;
  return output_err;
}

int ImitatorReceivAlm::ReadDIFromFile(std::string path_di_file, char*& text_in_file)
{
  int output_err = errors.succesful_completion;
  // Открываем файл для чтения
  std::ifstream file(path_di_file, std::ifstream::binary);
  if (file.is_open())
  {
    // Определяем размер (кол-во символов в файле) файла
    file.seekg (0, file.end);
    int size_file = file.tellg();
    file.seekg (0, file.beg);

    // Выделяем необходимое кол-во памяти
    text_in_file = new char[size_file];

    // Считываем текст с файла и закрываем его
    file.read (text_in_file, size_file);
    file.close();
  }
  else
  {
    output_err = errors.error_miss_file;
  }
  return output_err;
}

int ImitatorReceivAlm::Text2MapWithJSONObj(char* text, map_for_di& di)
{
  int output_err = errors.succesful_completion;
  try
  {
    // Парсим текст и конвертируем его в json объект
    json j_complete = json::parse(text);
    di = j_complete;
  }
  catch (json::parse_error& exp)
  {
    output_err = errors.error_convert_text_to_json;
  }
  catch (json::type_error& exp)
  {
    output_err = errors.error_convert_json_to_map;
  }
  return output_err;
}

double ImitatorReceivAlm::ConvertDateOfSeconds2000(Date date_rec_alm)
{
  double seconds = 0;
  // Переводим год в месяца
  seconds = (date_rec_alm[2] - 2000)*12;
  // Прибавляем текущий месяц
  seconds += date_rec_alm[1];
  // Переводим месяца в дни. Кол-во дней в месяце в среднем 30
  seconds *= 30;
  // Прибовляем тек. значение дня
  seconds += date_rec_alm[0];
  // Переводим кол-во дней в секунды
  seconds *= 86400;
  return seconds;
}

void ImitatorReceivAlm::FormationAllDic()
{
  for (int8_t latitude = this->settings.start_latitude
      ;latitude <= this->settings.end_latitude
      ;latitude += this->settings.step_latitude)
  {
    for (int16_t longitude = this->settings.start_longitude
        ;longitude <= this->settings.end_longitude
        ;longitude += this->settings.step_longitude)
    {
      bl_coor_point cur_point(latitude, longitude);
      FormationDicTimeRecAlm(cur_point);
      FormationDicListRecAlm(cur_point);
      FormationDicFlagRecAlm(cur_point);
    }
  }
}

void ImitatorReceivAlm::FormationDicTimeRecAlm(bl_coor_point cur_point)
{
  this->dic_time_rec_alm[cur_point] = 0;
}

void ImitatorReceivAlm::FormationDicListRecAlm(bl_coor_point cur_point)
{
  this->dic_list_time_rec_alm[cur_point] = std::list<int>();
}

void ImitatorReceivAlm::FormationDicFlagRecAlm(bl_coor_point cur_point)
{
  this->dic_flag_rec_alm[cur_point] = std::vector<bool>(this->vec_alm.size());
}

int ImitatorReceivAlm::ModelingReceivAlm()
{
  int output_err = errors.succesful_completion;
  // Вектор, который содержит координаты всех КА
  std::vector<Coordinates> vec_coor_all_sat;
  // Основной цикл по времени
  for (uint32_t time = 1; time <= this->settings.time_simulation; time++)
  {
    // Рассчитываем координаты всех КА
    CalculationCoordinatesAllSat(time+this->time_start_calculation_coor, this->vec_alm, vec_coor_all_sat);
    // Цикл по широте
    for (int8_t latitude = this->settings.start_latitude
        ;latitude <= this->settings.end_latitude
        ;latitude += this->settings.step_latitude)
    {
      for (int16_t longitude = this->settings.start_longitude
          ;longitude <= this->settings.end_longitude
          ;longitude += this->settings.step_longitude)
      {
        bl_coor_point cur_point(latitude, longitude);
        output_err = ModelingReceivAlmOnePoint(time, vec_coor_all_sat, cur_point);
      }
      if (output_err != errors.succesful_completion)
        break;
    }
  }
  return output_err;
}

int ImitatorReceivAlm::ModelingReceivAlmOnePoint(uint32_t time, std::vector<Coordinates> &vec_coor_all_sat
                                                ,bl_coor_point coor_bl_point)
{
  int output_err = errors.succesful_completion;
  // Определяем текущие координаты принимающей антенны
  Coordinates coor_point;
  coor_point[0] = coor_bl_point.first*M_PI/180.0;
  coor_point[1] = coor_bl_point.second*M_PI/180.0;
  coor_point[2] = this->settings.height_pos;
  coor_point = BLH2XYZ(coor_point);
  // Вычисляем список с видимыми КА
  std::list<uint8_t> list_vis_sat = DefinitionVisibleSat(vec_coor_all_sat, coor_point);
  // Заполняем вектор с принятыми альманахами КА для опред. точки
  PassingStr(time, list_vis_sat, coor_bl_point);
  // Определяем был ли передан весь альманах для данной точки
  auto& vec_rec_alm = this->dic_flag_rec_alm[coor_bl_point];
  bool f_full_alm = (std::find(vec_rec_alm.begin(), vec_rec_alm.end(), false) == vec_rec_alm.end());
  // Если альманах принят полностью, то добавляем полученное время в соот. список
  // из словаря, а также обнуляем это время и устанавливаем в False флаги принятия альманха
  if (f_full_alm)
  {
    this->dic_list_time_rec_alm[coor_bl_point].push_back(this->dic_time_rec_alm[coor_bl_point]);
    this->dic_time_rec_alm[coor_bl_point] = 0;
    std::fill(vec_rec_alm.begin(), vec_rec_alm.end(), false);
  }
  else
    this->dic_time_rec_alm[coor_bl_point] += 1;

  return output_err;
}

int ImitatorReceivAlm::CalculationCoordinatesAllSat(uint32_t curr_time, const std::vector<Almanah>& vec_alm
                                                   ,std::vector<Coordinates>& vec_sat_coor)
{
  int output_err = errors.succesful_completion;
  // Предварительно отчищаем вектор с координатами КА
  vec_sat_coor.clear();
  // Цикл перебора альманаха
  for (const auto& almanah : vec_alm)
  {
    Coordinates coor_sat; // Рассчитанные координаты КА
    // Рассчитываем координаты КА
    output_err = CalcultionCoordinatesSat(curr_time, almanah, coor_sat);
    if (output_err != errors.succesful_completion)
      break;
    vec_sat_coor.push_back(coor_sat);
  }
  return output_err;
}

int ImitatorReceivAlm::CalcultionCoordinatesSat(uint32_t curr_time, const Almanah& almanah, Coordinates& sat_coor)
{
  int output_err = errors.succesful_completion;
  double tmAlmVto = (almanah.n4 - 1); // число четырехлетних циклов от 2000г
  tmAlmVto *= 1461;                   // число дней от начала 2000г до конца предыдущего четырех.цикла
  tmAlmVto += (almanah.na - 1);       // число дней от начала 2000г до дня na
  tmAlmVto *= 86400;                  // число секунд от начала 2000г до дня na
  if( fabs((static_cast<double>(curr_time)) - tmAlmVto) > (90*24*3600) )
  {
    output_err = errors.error_old_almanac;
  }
  else
  {
    // Тест
    // i_cr = 64.8;
    // T_cr = 40544
//    almanah.na = 1452;
//    almanah.lambdaT = 33571.625;
//    almanah.dT = 0.01953124999975;
//    almanah.ddT = 6.103515625E-05;
//    almanah.lambda = -0.293967247009277;
//    almanah.omega = 0.57867431640625;
//    almanah.e = 0.000432968139648438;
//    almanah.dI = -0.00012947082519531;
//    curr_time = 51300+86400;

    // Константы
    const double i_cr = 64.8; //63.0;
    const double T_cr = 40544; //43200.0;
    const double GM   = 398600.4418;
    const double a_e  = 6378.136;
    const double om_z = 7.2921150e-5;
    const double J0_2 = 1082.62575e-6;

    //Исходные данные приведены в радианах. В алгоритме ИКД приведено в циклах.
    double dI = almanah.dI;
    double lambda = almanah.lambda;
    double omega = almanah.omega;

    //1.
//    double dt_pr = curr_time-almanah.lambdaT;
    double dt_pr = curr_time - (tmAlmVto+almanah.lambdaT);
    //2.
    double W = floor(dt_pr / (T_cr+almanah.dT));
    //3.
    double i = (i_cr/180.0+dI)*M_PI;
    //4.
    double T_dr = T_cr + almanah.dT + (2.0*W+1)*almanah.ddT;
    double n = 2.0*M_PI/T_dr;
    //5.
    double a = 0.0;
    double p;
    if (this->settings.prog_lvl_opt != 2)
    {
      double a0 = 1.0;
      double T_osk = T_dr;
      while (fabs(a-a0)>1e-6)
      { //в ИКД указано 1 см, но согласно примеру необходимо выполнить еще одну итерацию. Скорее всего в ИКД использовался do while
        a0 = a;
        a = pow(pow(T_osk/(2.0*M_PI),2.0) * GM,1.0/3.0);
        p = a * (1.0-pow(almanah.e,2.0));
        T_osk = T_dr / (1-1.5*J0_2*pow(a_e/p,2.0) *( (2.0-2.5*pow(sin(i),2.0)) * pow((1.0-pow(almanah.e,2.0)),1.5) / pow(1.0+almanah.e*cos(omega*M_PI),2.0) + pow(1.0+almanah.e*cos(omega*M_PI),3.0) / (1.0-pow(almanah.e,2.0))));
       }
    }
    else
    {
      a = pow(pow(T_dr/(2.0*M_PI),2.0) * GM,1.0/3.0);
      p = a * (1.0-pow(almanah.e,2.0));
    }
    //6.
    double lym = lambda * M_PI - (om_z + 1.5*J0_2*n*pow(a_e/p,2.0)*cos(i))*dt_pr;
    double om = omega*M_PI-0.75*J0_2*n*pow(a_e/p,2.0)* (1-5*pow(cos(i),2.0))*dt_pr;
    //7.
    double E0 = -2.0 * atan(sqrt((1.0-almanah.e)/(1.0+almanah.e))*tan(om/2.0));
    double L1 = om + E0 - almanah.e*sin(E0);
    //8.
    double L[2];
    L[1] = L1 + n*(dt_pr - (T_cr+almanah.dT)*W-almanah.ddT*W*W);
    L[0] = L1;

    double a_ = a;
    double i_ = i;
    double lym_ = lym;
    double L_ = L[1];
    double eps_ = almanah.e;
    double om_ = om;

    if (this->settings.prog_lvl_opt == 0)
    {
      //9.
      double h = almanah.e * sin(om);
      double l = almanah.e * cos(om);
      double B = 1.5*J0_2*(a_e/a)*(a_e/a);
      double dela[2], delh[2],dell[2],dellym[2],deli[2],delL[2];
      for (int k=0;k<2;k++)
      {
        dela[k] = (2.0*B*(1-1.5*pow(sin(i),2.0))*(l*cos(L[k])+h*sin(L[k]))+B*pow(sin(i),2.0)*(0.5*h*sin(L[k])-0.5*l*cos(L[k])+cos(2.0*L[k])+3.5*l*cos(3.0*L[k])+3.5*h*sin(3.0*L[k])))*a;
        delh[k] = B*(1-1.5*pow(sin(i),2.0))*(sin(L[k])+1.5*l*sin(2*L[k])-1.5*h*cos(2.0*L[k]))-0.25*B*pow(sin(i),2.0)*(sin(L[k])-7.0/3.0*sin(3.0*L[k])+5*l*sin(2*L[k])-8.5*l*sin(4*L[k])+8.5*h*cos(4*L[k])+h*cos(2.0*L[k])) +(-0.5*B*pow(cos(i),2.0)*l*sin(2.0*L[k]));
        dell[k] = B*(1-1.5*pow(sin(i),2.0))*(cos(L[k])+1.5*l*cos(2*L[k])+1.5*h*sin(2*L[k]))-0.25*B*pow(sin(i),2.0)*(-cos(L[k])-7.0/3.0*cos(3.0*L[k])-5.0*h*sin(2*L[k])-8.5*l*cos(4*L[k])-8.5*h*sin(4*L[k])+l*cos(2.0*L[k]))+  0.5*B*pow(cos(i),2.0)*h*sin(2.0*L[k]);
        dellym[k] = -B*cos(i)*(3.5*l*sin(L[k])-2.5*h*cos(L[k])-0.5*sin(2*L[k])-7.0/6.0*l*sin(3.0*L[k])+7.0/6.0*h*cos(3*L[k]));
        deli[k] = 0.5*B * sin(i)*cos(i)*(-l*cos(L[k])+h*sin(L[k])+cos(2*L[k])+7.0/3.0*l*cos(3.0*L[k])+7.0/3.0*h*sin(3*L[k]));
        delL[k] = 2.0*B*(1-1.5*pow(sin(i),2.0))*(7.0/4.0*l*sin(L[k])-7.0/4.0*h*cos(L[k]))+3.0*B*pow(sin(i),2.0)*(-7.0/24.0*h*cos(L[k])-7.0/24.0*l*sin(L[k])-49.0/72.0*h*cos(3*L[k])+49.0/72.0*l*sin(3.0*L[k])+0.25*sin(2*L[k]))+B*pow(cos(i),2.0) * (3.5*l*sin(L[k])-2.5*h*cos(L[k])-0.5*sin(2.0*L[k])+7.0/6.0*l*sin(3.0*L[k])+7.0/6.0*h*cos(3.0*L[k]));
      }

      a_ = a + dela[1] - dela[0];
      double h_ = h + delh[1] - delh[0];
      double l_ = l + dell[1] - dell[0];
      i_ = i + deli[1] - deli[0];
      lym_ = lym +dellym[1] - dellym[0];
      L_ = L[1] + delL[1] - delL[0];
      eps_ = sqrt(h_*h_+l_*l_);
      om_ = atan2(h_,l_);
    }

    //10.
    E0=L_-om_;
    double E = 0;
    while (fabs(E-E0)>10e-11){ //в Си использовать do while, тогда вставить условие abs(E-E0)>10e-9
      E0 = E;
      E = L_-om_+eps_*sin(E0);
    }
    //11.
    double v = 2.0 * atan(sqrt((1.0+eps_)/(1.0-eps_))*tan(E/2.0));
    double u = v + om_;
    //12.
    p = a_*(1.0-eps_*eps_);
    double r = p/(1+eps_*cos(v));
    // Кординаты сразу в м.
    sat_coor[0] = r * (cos(lym_)*cos(u)-sin(lym_)*sin(u)*cos(i_));
    sat_coor[1] = r * (sin(lym_)*cos(u)+cos(lym_)*sin(u)*cos(i_));
    sat_coor[2] = r * sin(u)*sin(i_);
  }

  return output_err;
}

std::list<uint8_t> ImitatorReceivAlm::DefinitionVisibleSat(std::vector<Coordinates>& vec_sat_coor, Coordinates coor_point)
{
  std::list<uint8_t> list_vis_sat;
  // Цикл перебора координат КА
  for (uint8_t ind_sat = 0; ind_sat < vec_sat_coor.size(); ind_sat++)
  {
    uint8_t num_sat = ind_sat+1;
    // Рассчитываем УМ
    double angle_elev = CalculationAngleElevation(vec_sat_coor[ind_sat], coor_point);
    // Определяем видимость КА
    if (angle_elev > this->settings.min_angle_elev)
      list_vis_sat.push_back(num_sat);
  }
  return list_vis_sat;
}

void ImitatorReceivAlm::PassingStr(uint32_t time, std::list<uint8_t>& list_vis_sat, bl_coor_point cur_point)
{
  // Цикл по видимым КА
  for (uint8_t num_sat : list_vis_sat)
  {
    auto signals_di_sat = this->di_system[std::to_string(num_sat)];
    // Цикл по передаваемым сигналам
    for (auto signal_di : signals_di_sat)
    {
      std::string cur_signal = signal_di.first;
      int num_cur_str = signal_di.second[(time-1)% this->settings.di_sett.time_di];
      uint8_t time_trans_sig = DIC_NAME_SIG_IN_TRANS_TIME.at(cur_signal);
      // Условие передачи строки с альманахом
      if (((time%time_trans_sig) == 0) && (num_cur_str >= this->settings.di_sett.num_con_aml))
      {
        // Определяем индекс КА в массиве и устанавливаем флаг передачи альманаха в true
        uint8_t ind_sat = num_cur_str - this->settings.di_sett.num_con_aml;
        this->dic_flag_rec_alm[cur_point][ind_sat] = true;
      }
    }
  }
}
