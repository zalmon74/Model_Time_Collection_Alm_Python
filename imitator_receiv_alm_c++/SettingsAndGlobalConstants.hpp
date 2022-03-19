#ifndef SETTINGSANDGLOBALCONSTANTS_HPP
#define SETTINGSANDGLOBALCONSTANTS_HPP

#include <map>
#include <vector>
#include <array>
#include <string>
#include <stdint.h>

#include "Structs.hpp"

/* Значения по умолчанию для имитатора */

// Путь до файлов с данными для имитатора, который указывается при создании имитатора (стандартный)
#define STD_PATH_PATHS "./../conf/paths.conf"

// Словарь для ЦИ
//               Номер КА,  map сигн,  дост. сигн,  перед. строки
typedef std::map<std::string, std::map<std::string, std::vector<int>>> map_for_di;
// Координаты точки типа BL (широта - долгота)
typedef std::pair<int8_t, int16_t> bl_coor_point;

#define UNDEFINE_UINT8  0xFF
#define UNDEFINE_INT16  0x7FFF
#define UNDEFINE_UINT16 0xFFFF
#define UNDEFINE_INT32  0x7FFFFFFF
#define UNDEFINE_UINT32 0xFFFFFFFF
#define UNDEFINE_INT64  0x7FFFFFFFFFFFFFFF

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

static const PathsFiles paths_files(STD_PATH_PATHS);

#endif // SETTINGSANDGLOBALCONSTANTS_HPP
