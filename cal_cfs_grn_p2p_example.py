import matplotlib.pyplot as plt
import numpy as np
from scipy.io import savemat

from pygrnwang.create_qssp import create_points
from pygrnwang.focal_mechanism import mt2plane
from coulomb_failure_stress_change.coulomb_stress_dynamic import (
    cal_coulomb_stress_grn_point2point,
)

if __name__ == "__main__":
    sub_fm = list(mt2plane(
        [-0.98791947, -0.14147067, 0.05218096,
         0.98900693, 0.01424112, -0.00108746]
    )[0])

    sub_faults_2 = np.load(
        "./path_faults_example/sub_faults_plane2.npy"
    )
    sub_fms_2 = np.load(
        "./path_faults_example/sub_fms_plane2.npy"
    )
    ind_sub_fault = 30
    sub_fault_field = sub_faults_2[ind_sub_fault]
    sub_fm_field = sub_fms_2[ind_sub_fault]

    points = create_points(dist_range=[0, 320], delta_dist=5)

    savemat('/e/qb_d5/points_grn_geo.mat', mdict={'points_grn_geo': points})

    (
        stress_enz,
        sigma_vector,
        sigma,
        tau,
        mean_stress,
        coulomb_stress,
        coulomb_stress_pore
    ) = cal_coulomb_stress_grn_point2point(
        path_green="/e/qb_d5",
        fm_source=sub_fm,
        source_point=[37.2762992074037, 37.0745276572931, 9.96194698091746],
        fm_field=sub_fm_field,
        field_point=sub_fault_field,
        points_green_geo_flatten=points.flatten(),
        event_dep_list=[2 * h + 1 for h in range(15)],
        receiver_dep_list=[2 * h + 1 for h in range(15)],
        srate_cfs=1,
        time_reduction=10,
        N_T=256,

        max_slowness=0.4,
        mu_f=0.4,
        mu_f_pore=0.6,
        B_pore=0.75,
        interp=False,
    )
    print(stress_enz.shape)

    plt.figure()
    plt.plot(coulomb_stress)
    plt.show()
