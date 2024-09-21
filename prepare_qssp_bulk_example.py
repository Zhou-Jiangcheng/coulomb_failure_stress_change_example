from pygrnwang.create_qssp_bulk import *

if __name__ == "__main__":
    # Only for example, the parameter must be modified!
    processes_num = 6
    event_depth_list = [h * 2 + 1 for h in range(15)]
    receiver_depth_list = [h * 2 + 1 for h in range(15)]
    path_green = "/mypath/output_test_dynamic/grnlib"
    path_bin = "/mypath/coulomb_failure_stress_change_example/pygrnwang/qssp2020.bin"
    spec_time_window = 255
    time_window = 255
    time_reduction = -10
    dist_range = [0, 100]
    delta_dist_range = 10
    sampling_interval = 1
    max_frequency = 0.01
    max_slowness = 0.4
    anti_alias = 0.01
    turning_point_filter = 0
    turning_point_d1 = 0
    turning_point_d2 = 0
    free_surface_filter = 1
    gravity_fc = 0
    gravity_harmonic = 0
    cal_sph = 1
    cal_tor = 1
    min_harmonic = 6000
    max_harmonic = 6000
    output_observables = [0 for _ in range(11)]
    output_observables[5] = 1
    path_nd = "/mypath/pygrnwang/turkey.nd"
    earth_model_layer_num = 7
    pre_process(
        processes_num=processes_num,
        event_depth_list=event_depth_list,
        receiver_depth_list=receiver_depth_list,
        path_green=path_green,
        path_bin=path_bin,
        spec_time_window=spec_time_window,
        time_window=time_window,
        time_reduction=time_reduction,
        dist_range=dist_range,
        delta_dist_range=delta_dist_range,
        sampling_interval=sampling_interval,
        max_frequency=max_frequency,
        max_slowness=max_slowness,
        anti_alias=anti_alias,
        turning_point_filter=turning_point_filter,
        turning_point_d1=turning_point_d1,
        turning_point_d2=turning_point_d2,
        free_surface_filter=free_surface_filter,
        gravity_fc=gravity_fc,
        gravity_harmonic=gravity_harmonic,
        cal_sph=cal_sph,
        cal_tor=cal_tor,
        min_harmonic=min_harmonic,
        max_harmonic=max_harmonic,
        output_observables=output_observables,
        path_nd=path_nd,
        earth_model_layer_num=earth_model_layer_num,
    )
