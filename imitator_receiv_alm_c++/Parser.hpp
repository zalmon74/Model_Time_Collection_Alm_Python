#ifndef PARSER_HPP
#define PARSER_HPP

#include <string>

#include "../sequencing_algorithm/include/my_analog_structs.hpp"
#include "SettingsAndGlobalConstants.hpp"

class Parser
{
protected:
  char comment_separator_symb = '#'; // Символ для определения комментариев в файле

  std::string path_to_file; // Путь до файла

public:

  /* Методы */

  /*! Метод установки символа для определения комментариев в файле
   *  Вх аргументы:
   *    \@param: symb - новый символ, с которого будет начинаться комментарий
  */
  void SetSymbolCommentSeparator(const char symb) { this->comment_separator_symb = symb; }

  /*! Метод установки пути до файла
   *  Вх аргументы:
   *    \@param: path_file - путь до файла
   *  Вых. аргументы:
   *    \@param: SUCCESFUL_COMPLETION - успешное выполнение
   *             ERROR_EMPTY - входная строка пустая;
   *             ERROR_MISS_FILE - в файла по данному пути не существует
  */
  int SetPathFile(std::string path_file);
};

class AlmanahParser : public Parser
{
private:
  Nf501StructList almanah;

  /*! Метод чтения файла с альманахом. В данном файле комментарии отсутствуют
   *
   *  Вых. параметры:
   *    \@param: SUCCESFUL_COMPLETION - успешное выполнение
   *             ERROR_EMPTY - файл пустой
   *             ERROR_MISS_FILE - в файла по данному пути не существует
  */
  int ReadFile();
public:

  /*! Метод получения считанных данных из файла в виде объекта "Nf501StructList" */
  Nf501StructList GetData() { ReadFile(); return this->almanah; }
};

#endif // PARSER_HPP
