#ifndef SETTINGSANDGLOBALCONSTANTS_HPP
#define SETTINGSANDGLOBALCONSTANTS_HPP

#include <map>
#include <vector>
#include <array>
#include <string>
#include <stdint.h>

/* Значения по умолчанию для имитатора */

// Путь до файлов с данными для имитатора, который указывается при создании имитатора (стандартный)
#define STD_PATH_DATA_IMITATOR "./../../Dropbox/Diplom/Model_Time_Collection_Alm_Python/"
#define STD_NAME_ALM_FILE "alm/alm_17_07_2018_10_30_11_00_929_KA_24.txt"
#define STD_NAME_DI_FILE "ci/ci_2021_10_22_08_11_02.json"
#define STD_PATH_RESULT_FILE "results/"

#define STD_TIME_SIMULATION 8*86400 // Стандартное время моделирования в сек.

// Значения по умолчанию карты моделирования
#define STD_START_LATITUDE 0//-60 // Начало широты для моделирования в град.
#define STD_END_LATITUDE    0//60 // Конец широты для моделирования в град.
#define STD_STEP_LATITUDE    2 // Шаг по широте для моделирования в град.
#define STD_START_LONGITUDE 0//-180 // Начало долготы для моделирования в град.
#define STD_END_LONGITUDE    0//180 // Конец долготы для моделирования в град.
#define STD_STEP_LONGITUDE     3 // Шаг по долготе для моделирования в град.
#define STD_MIN_ANGLE_ELEV 5 // Минимальный УМ, при котором КА считается видимым
#define HEIGHT_POS 0 //  Высота антенны, принимающая альманах

// Значение, с которого начинается условный номер КА
#define NUM_CON_ALM 700
// Время в сек. на формирование ЦИ
#define MAX_TIME_DI 3600

// Уровень оптимизации при расчете прогноза (рассчета координат КА)
// 0 - Оптимазация отсутствует, 1 - оптимизация первого уровня,
// 2 - Оптимизация второго уровня
#define PROG_LVL_OPT 0
// Количество параметров в строке с файлом альманаха
#define COUNT_VAR_TO_STR_IN_FILE_ALM 9
/* Индексы в файле с альманахом соот. параметрам в первой строке */
#define IND_TIME_BEG_FILE_ALM  0 // Время начала моделирования (не используемый параметр)
#define IND_TIME_END_FILE_ALM  1 // Время окончания моделирования (не используемый параметр)
#define IND_DAY_REC_FILE_ALM   2 // День в месяце, в котром был получен альманах
#define IND_MON_REC_FILE_ALM   3 // Месяц, в котором был получен альманах
#define IND_YEAR_REC_FILE_ALM  4 // Год, в котором был получен альманах
#define IND_NA_FILE_ALM        5 // День в четырехлетнем цикле
#define IND_COUNT_SAT_FILE_ALM 6 // Кол-во КА в альманахе
/* Индексы в файле с альманахом соот. параметрам альманаха */
#define IND_LITTER  0 // Номер литеры НКА
#define IND_TA_LYM  1 // Время восходящего узла НКА
#define IND_TAU_N  11
#define IND_LYMA   12 // Долгота восходящего узла НКА
#define IND_DIA    13 // Поправка к сред. значению наклонения орбиты НКА
#define IND_OMA    14 // Аргумент Перигея НКА
#define IND_EPSA   15 // Эксцентриситет орбиты НКА
#define IND_DTA    16 // Поправка к среднему значению драконического периода обращения
#define IND_DDTA   17 // Половинная скорость изменения драконического периода

// Диапозон корректных значений УМ
#define MIN_CORRECT_ANGLE_ELEV -60
#define MAX_COORECT_ANGLE_ELEV 60

// Значение оступа в JSON файле с результатами
#define VALUE_INDENT_JSON_RESULT 2

/* Ошибки */

#define SUCCESSFUL_COMPLETION 0 // Успешное завершение
#define ERROR_OLD_ALM -1 // Старый альманах (Альманах устарел больше чем на 90 дней)
// Файл c альманахом по заданному пути невозможно открыть/не существует
#define ERROR_MISS_ALM_FILE -2
// Файл c ЦИ по данному пути невозможно открыть/не существует
#define ERROR_MISS_DI_FILE -3
// Ошибка при конвертировании текста в JSON объект
#define ERROR_CONVERT_TEXT_TO_JSON -4
// Ошибка при конвертации JSON объекта в словарь
#define ERROR_CONVERT_JSON_TO_MAP -5
// Не правильно заданы координаты широты (end < start)
#define ERROR_SET_NOT_CORRERCT_LATITUDE -6
// Не правильно заданы координаты долготы (end < start)
#define ERROR_SET_NOT_CORRERCT_LONGITUDE -7
// Ошибка, характеризующая бесконечную карту (step == 0)
#define ERROR_NULL_STEP -8
// Не правильно задан УМ (вне диапозона)
#define ERROR_SET_NOT_CORRECT_ANGLE_ELEV -8
// Не удалось создать файл с результатами
#define ERROR_CREATE_RESULT_FILE -9

// Словарь для ЦИ
//               Номер КА,  map сигн,  дост. сигн,  перед. строки
typedef std::map<std::string, std::map<std::string, std::vector<int>>> map_for_di;
// Координаты точки типа BL (широта - долгота)
typedef std::pair<int8_t, int16_t> bl_coor_point;

static const uint8_t  UNDEFINE_UINT8  = 0xFF              ;
static const int16_t  UNDEFINE_INT16  = 0x7FFF            ;
static const uint16_t UNDEFINE_UINT16 = 0xFFFF            ;
static const int32_t  UNDEFINE_INT32  = 0x7FFFFFFF        ;
static const uint32_t UNDEFINE_UINT32 = 0xFFFFFFFF        ;
static const int64_t  UNDEFINE_INT64  = 0x7FFFFFFFFFFFFFFF;

// Константы Земли, которые необходимы для перевода координат
static const double R_EARHT = 6371.136; // Радиус Земли, [км]
static const double E_EARHT = 0.0818; // Эксцентриситет Земли

// Вектор, который содержит все имена сигналов
static const std::array<std::string, 4> VEC_ALLA_SIG = {"L1OC", "L1SC", "L2SC", "L3OC"};

// Словарь, который хранит в себе сопоставление имени сигнала и время передачи в сек.
static const std::map<std::string, uint8_t> DIC_NAME_SIG_IN_TRANS_TIME = {{"L3OC", 3}
                                                                         ,{"L1SC", 2}
                                                                         ,{"L2SC", 2}
                                                                         ,{"L1OC", 2}
                                                                         };

#endif // SETTINGSANDGLOBALCONSTANTS_HPP
