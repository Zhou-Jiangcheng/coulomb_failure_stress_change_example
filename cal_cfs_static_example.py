from coulomb_failure_stress_change.coulomb_stress_static import *

if __name__ == "__main__":
    processes_num = 6
    path_output = "/mypath/output_test_static"
    path_bin_edgrn = "/mypath/coulomb_failure_stress_change/edgrn2.0-f77code/edgrn2.0.bin"
    path_bin_edcmp = "/mypath/coulomb_failure_stress_change/edcmp2.0-f77code/edcmp2.0.bin"
    ref_point = [37.2762992074037, 37.0745276572931, 9961.94698091746]
    path_faults_sources = "./path_faults_example"
    path_faults_obs = "./path_faults_example"
    source_plane_inds = [0]
    obs_plane_inds = [1]
    sub_length_source = 2000
    sub_length_obs = 2000
    source_dep_list = [d * 1e3 for d in range(0, 31, 1)]
    obs_dep_list = [d * 1e3 for d in range(0, 31, 1)]
    lat_range = [36, 39]
    lon_range = [36, 39]
    rmax_grn = 300e3
    hs_flag = 1
    path_nd = "/mypath/pygrnwang/turkey.nd"
    earth_model_layer_num = 6
    lam = 30516224000
    mu = 33701888000

    prepare_cfs_static(
        path_output,
        path_bin_edgrn,
        path_bin_edcmp,
        path_faults_sources,
        source_plane_inds,
        sub_length_source,
        source_dep_list,
        path_faults_obs,
        sub_length_obs,
        obs_dep_list,
        lat_range,
        lon_range,
        rmax_grn,
        ref_point,
        hs_flag,
        path_nd,
        earth_model_layer_num,
        lam,
        mu,
    )
    create_static_cfs_lib(
        processes_num,
        path_output,
        path_faults_obs,
        obs_plane_inds,
        sub_length_obs,
        obs_dep_list,
        ref_point,
        hs_flag,
    )
    cal_static_coulomb_stress(path_output, obs_plane_inds, mu_f=0.4, B=0.75)
