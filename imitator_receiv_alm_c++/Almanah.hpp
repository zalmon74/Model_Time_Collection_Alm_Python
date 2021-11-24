#ifndef ALMANAH_HPP
#define ALMANAH_HPP

#include <stdint.h>
#include <iostream>
#include <iomanip>
#include <math.h>

#include "SettingsAndGlobalConstants.hpp"

#pragma pack(1)
struct Almanah
{
  uint8_t num;         // Номер системной точки НКА (255 --- недействительный номер)
  int8_t lit;         // Номер литерной частоты, от 0 до 32; 24 --- недействительная
  uint8_t  n4;         // Число четырехлетних циклов от 1996 г.
  uint16_t na;         // День в четырехлетнем цикле
  long double lambda;  // Гринвичская долгота восходящего узла орбиты в СК ПЗ-90, радианы
  long double lambdaT; // МДВ прохождения восходящего узла орбиты, секунды
  long double dI;      // Поправка к среднему значению наклонения орбиты радианы
  long double dT;      // Поправка к среднему значению драконического периода обращения секунды
  long double ddT;     // Скорость изменения поправки
  long double e;       // Эксцентриситет орбиты
  long double omega;   // Аргумент перигея, радианы
  long double tau;

  Almanah()
  {
    this->num = UNDEFINE_UINT8;
    this->lit = UNDEFINE_UINT8;
    this->n4  = UNDEFINE_UINT8;
    this->na  = UNDEFINE_UINT16;
    this->lambda  = NAN;
    this->lambdaT = NAN;
    this->dI      = NAN;
    this->dT      = NAN;
    this->ddT     = NAN;
    this->e       = NAN;
    this->omega   = NAN;
    this->tau     = NAN;
  }

  void PrintData()
  {
    std::cout << std::setw(5) << "  NUM = " << static_cast<uint16_t>(num) << '\t'
                              << "  LIT = " << static_cast<uint16_t>(lit) << '\t'
                              << "   N4 = " << static_cast<uint16_t>( n4) << '\t'
                              << "   Na = " <<                         na << '\t'
                              << "  LYM = " <<                     lambda << '\t'
                              << "LYM_T = " <<                    lambdaT << '\t'
                              << "   dT = " <<                         dT << '\t'
                              << "  ddT = " <<                        ddT << '\t'
                              << "  EXC = " <<                          e << '\t'
                              << "   OM = " <<                      omega << '\t'
                              << "  TAU = " <<                        tau << '\n';
  }
};
#pragma pack()

#endif // ALMANAH_HPP
