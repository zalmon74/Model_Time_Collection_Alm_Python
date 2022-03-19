#!/bin/bash

# Путь по которому лежит программа формирования посследовательностей
PATH_PROGRAM_SEQ_ALGORITHM="./build-opt-Desktop_Qt_6_2_2_GCC_64bit-Release"
# Путь по которму лежит программа формирования ЦИ
PATH_PROGRAM_FORMATION_DI="./formation_ci"
# Путь по которому лежит программа моделирования приема альманаха
PATH_PROGRAM_IMITATOR_RECEIV_ALM="./imit_receiv_alm_c++"
# Файл запуска программы формирования последовательностей
NAME_FILE_START_SEQ_ALGORITHM="opt"
# Файл запуска программы формирования ЦИ
NAME_FILE_START_FORMATION_DI="main.py"
# Файл запуска программы моделирования приема альманаха
NAME_FILE_START_IMITATOR_RECEIV_ALM="untitled"
# Путь по которому лежат результаты выполнения алгоритма формирования последовательностей
PATH_RESULT_SEQ_FILES="./result_sequncing_algorithm/"
# Путь по которому лежат результаты формирования ЦИ
PATH_RESULT_DI_FILES="./ci/"
# Путь по которому располагаются конфигурационные файлы
PATH_CONFS_FILES="./conf/"
# Имя файла, который содержит пути до всех файлов
NAME_PATHS_PATHS="paths.conf"
# Имя, которое воспринимает программа формирования ЦИ, с результатами работы
# алгоритма формирования последовательностей
NAME_RESULT_SEQ_ALGORITHM="sequencing_algorithm.json"
# Имя временного файла
NAME_TMP_FILE="tmp_file"
# Имя переменной, которая отвечает за используемый файл ЦИ
NAME_VALUE_RESULT_DI="RESULT_CI_FORMATION_FILE = "

echo "Запускается программа формирования последовательностей"
# Запускаем программу формирования последовательностей
cd "$PATH_PROGRAM_SEQ_ALGORITHM"
"./$NAME_FILE_START_SEQ_ALGORITHM" > /dev/null 2>&1
cd ..
# Имя последнего сформированного файла с последовательностями
name_result_seq_file=$(ls -t1 "$PATH_RESULT_SEQ_FILES" | head -n1)
mv "$PATH_RESULT_SEQ_FILES$name_result_seq_file" "$PATH_RESULT_SEQ_FILES$NAME_TMP_FILE"
mv "$PATH_RESULT_SEQ_FILES$NAME_RESULT_SEQ_ALGORITHM" "$PATH_RESULT_SEQ_FILES$name_result_seq_file"
mv "$PATH_RESULT_SEQ_FILES$NAME_TMP_FILE" "$PATH_RESULT_SEQ_FILES$NAME_RESULT_SEQ_ALGORITHM"

echo "Запускается программа формирования ЦИ"
# Запускаем программу формирования ЦИ
cd "$PATH_PROGRAM_FORMATION_DI"
python3 "./$NAME_FILE_START_FORMATION_DI" > /dev/null 2>&1
cd ..
# Имя последнего сформированного файла с ЦИ
name_result_di_file=$(ls -t1 "$PATH_RESULT_DI_FILES" | head -n1)
# Записываем имя последнего ЦИ в конфигурационный файл
name_value=$(cat "$PATH_CONFS_FILES$NAME_PATHS_PATHS" | grep "$NAME_VALUE_RESULT_DI")
need_name_value="${NAME_VALUE_RESULT_DI}../ci/${name_result_di_file}"
test="$(sed -e "s@${name_value}@${need_name_value}@" ${PATH_CONFS_FILES}${NAME_PATHS_PATHS})"
echo "$test" > "$PATH_CONFS_FILES$NAME_PATHS_PATHS"

echo "Запускается программа имитации моделирования приема альманаха"
# Запускаем моделирование
cd "$PATH_PROGRAM_IMITATOR_RECEIV_ALM"
"./$NAME_FILE_START_IMITATOR_RECEIV_ALM" > /dev/null 2>&1
cd ..
