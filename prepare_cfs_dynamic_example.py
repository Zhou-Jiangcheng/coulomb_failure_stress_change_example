import numpy as np

from coulomb_failure_stress_change.coulomb_stress_dynamic import *
from pygrnwang.create_qssp import create_points

if __name__ == "__main__":
    processes_num = 6
    path_output = "/mypath/output_test_dynamic/cfs_S1_S2_d10"
    path_green = "/mypath/output_test_dynamic/grnlib"
    path_faults_source = "/mypath/coulomb_failure_stress_change_example/path_faults_example"
    source_inds = [0]
    field_points = np.load(
        "/mypath/coulomb_failure_stress_change_example/path_faults_example/sub_faults_plane_exp1.npy"
    )
    field_fms = np.load(
        "/mypath/coulomb_failure_stress_change_example/path_faults_example/sub_fms_plane_exp1.npy"
    )
    points_geo = create_points(dist_range=[0, 100], delta_dist=10)
    event_depth_list = [h * 2 + 1 for h in range(15)]
    receiver_depth_list = [h * 2 + 1 for h in range(15)]
    srate_stf = 2
    srate_cfs = 1
    N_T = 256
    time_reduction = 10
    mu_f = 0.4
    mu_f_pore = 0.6
    B_pore = 0.75
    interp = False
    prepare_multi_points(
        processes_num=processes_num,
        path_output=path_output,
        path_faults_source=path_faults_source,
        path_green=path_green,
        source_inds=source_inds,
        field_points=field_points,
        field_fms=field_fms,
        points_green_geo=points_geo,
        event_dep_list=event_depth_list,
        receiver_dep_list=receiver_depth_list,
        srate_stf=srate_stf,
        srate_cfs=srate_cfs,
        N_T=N_T,
        time_reduction=time_reduction,
        mu_f=mu_f,
        mu_f_pore=mu_f_pore,
        B_pore=B_pore,
        interp=interp,
    )
