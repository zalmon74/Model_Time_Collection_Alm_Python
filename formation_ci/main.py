import functions as f
import get_conf_paramets as get_conf
import imitator_bink as ib


def main():
    conf_par_seq = get_conf.get_conf_par_seq_alg("./../conf/sequencing_algorithm.conf")
    mat_mi_n, arr_mi_epi = f.read_result_sequencing_alg_result_file("./../results/sequencing_algorithm.json", conf_par_seq)
    ci = ib.imitator_bink(mat_mi_n, arr_mi_epi)
    f.save_ci_in_file(ci)


if __name__ == "__main__":
    main()
