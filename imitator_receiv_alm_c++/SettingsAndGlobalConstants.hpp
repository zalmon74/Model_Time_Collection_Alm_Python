#ifndef SETTINGSANDGLOBALCONSTANTS_HPP
#define SETTINGSANDGLOBALCONSTANTS_HPP

#include <map>
#include <vector>
#include <string>
#include <stdint.h>

// Путь до файлов с данными для имитатора, который указывается при создании имитатора (стандартный)
#define STD_PATH_DATA_IMITATOR "./"
#define STD_NAME_ALM_FILE "alm_17_07_2018_10_30_11_00_929_KA_24.txt"
#define STD_NAME_DI_FILE "ci_2021_10_22_08_11_02.json"

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

// Словарь для ЦИ
//               Номер КА,  map сигн,  дост. сигн,  перед. строки
typedef std::map<std::string, std::map<std::string, std::vector<int>>> map_for_di;

static const uint8_t  UNDEFINE_UINT8  = 0xFF              ;
static const int16_t  UNDEFINE_INT16  = 0x7FFF            ;
static const uint16_t UNDEFINE_UINT16 = 0xFFFF            ;
static const int32_t  UNDEFINE_INT32  = 0x7FFFFFFF        ;
static const uint32_t UNDEFINE_UINT32 = 0xFFFFFFFF        ;
static const int64_t  UNDEFINE_INT64  = 0x7FFFFFFFFFFFFFFF;

#endif // SETTINGSANDGLOBALCONSTANTS_HPP
