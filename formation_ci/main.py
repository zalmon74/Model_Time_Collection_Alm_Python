import numpy as np

import global_constants as gc
import support_function as sf
import functions as f
import imitator_bink as ib


def main():
    mat_mi_n, arr_mi_epi = f.read_result_sequencing_alg_result_file("./../results/sequencing_algorithm.json")
    ci = ib.imitator_bink(mat_mi_n, arr_mi_epi)
    f.save_ci_in_file(ci)


if __name__ == "__main__":
    main()
