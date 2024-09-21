from coulomb_failure_stress_change.read_dynamic_cfs_results import *

if __name__ == "__main__":
    read_stress_results(
        path_output="/output_test_dynamic/cfs_S1_S2_d10/",
        path_obs_faults="/mypath/coulomb_failure_stress_change_example/path_faults_example",
        inds_obs=[1],
    )
