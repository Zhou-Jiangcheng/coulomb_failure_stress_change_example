# Introduction

This project serves as a Python frontend, based on Professor Wang Rongjiang's Fortran programs, to compute and establish dynamic and static stress Green's function libraries, and to calculate dynamic and static Coulomb failure stress changes for a given finite-fault model.

References:

Wang, Rongjiang. (1999). A simple orthonormalization method for stable and efficient computation of Green’s functions. *Bulletin of the Seismological Society of America*, *89* (3), 733–741. [https://doi.org/10.1785/BSSA0890030733](https://doi.org/10.1785/BSSA0890030733)

Wang, R. (2003). Computation of deformation induced by earthquakes in a multi-layered elastic crust—FORTRAN programs EDGRN/EDCMP. *Computers & Geosciences*, *29* (2), 195–207. [https://doi.org/10.1016/S0098-3004(02)00111-5](https://doi.org/10.1016/S0098-3004(02)00111-5)

Wang, Rongjiang, Heimann, S., Zhang, Y., Wang, H., & Dahm, T. (2017). Complete synthetic seismograms based on a spherical self-gravitating Earth model with an atmosphere–ocean–mantle–core structure. *Geophysical Journal International*, *210* (3), 1739–1764.

# Installation

Clone the project with:

```
git clone --recurse-submodules https://github.com/Zhou-Jiangcheng/coulomb_failure_stress_change_example
```

On Debian-based Linux, install the `gfortran` compiler with:

```
sudo apt install gfortran
```

In the `qssp2020_src` folder, compile the executable with:

```
gfortran ./*.f -O3 -o qssp2020.bin
```

Similarly, in the `edgrn2.0-f77code` and `edcmp2.0-f77code` folders, compile the executables with:

```
gfortran ./*.f -O3 -o edgrn2.0
```

```
gfortran ./*.f -O3 -o edcmp2.0
```

Next, install Anaconda3 or Miniforge and run the following commands:

```
conda create -n cfs python=3.11 # Create a virtual environment named cfs
conda activate cfs # Activate the virtual environment
conda install numpy scipy pandas tqdm mpi4py -c conda-forge # Install dependencies
```

Add the folder path. For example, if your project is located at `/home/mydir/coulomb_failure_stress_change_example`, create and add `/home/mydir/coulomb_failure_stress_change_example` to the `/path_anaconda/envs/cfs/lib/python3.11/site-packages/custom.pth` file.

# Usage (Static CFS)

Modify the parameters in `cal_cfs_static_example.py` as needed. The meaning of each parameter is as follows:

- `processes_num`: Number of cores for parallel processing.
- `path_output`: Output path.
- `path_bin_edgrn`: Path to the executable file named `edgrn2.0`.
- `path_bin_edcmp`: Path to the executable file named `edcmp2.0`.
- `ref_point`: Reference point for converting fault coordinates from the geographic coordinate system (lat, lon, dep) to the Cartesian coordinate system. It is recommended to use the geometric center of the entire region formed by the source and observation faults to reduce computational load.
- `path_faults_source`: Path where the source fault files are stored (Note: In Python, indexing starts at 0, and the file is named `sub_faults_plane%d.npy % ind`).
- `source_plane_inds`: List of source fault indices.
- `path_faults_obs`: Path where the observation fault files are stored.
- `obs_plane_inds`: List of observation fault indices.
- `sub_length_source`: Sub-fault size on the source fault.
- `sub_length_obs`: Sub-fault size on the observation fault.
- `source_dep_list`: Depth list of the source fault.
- `obs_dep_list`: Depth list of the observation fault.
- `lat_range`: Latitude range of the observation fault.
- `lon_range`: Longitude range of the observation fault.
- `rmax_grn`: Maximum radius for calculating the Green's function library using `edgrn`.
- `hs_flag=1/0`: Whether or not to use the infinite half-space model. If set to 1, the layered Earth model is used and `lam` and `mu` do not need to be provided; if set to 0, the infinite half-space model is used, and `edgrn` will not run—`edcmp` will directly calculate the displacement.
- `path_nd`: Path to the Earth model when using `edgrn`.
- `earth_model_layer_num`: Number of layers in the Earth model, starting from the surface.
- `lam`: Elastic parameter when using the infinite half-space model.
- `mu`: Elastic parameter when using the infinite half-space model.

All units are in international standard units.

Ensure that the `cfs` virtual environment is activated, and then run the following command:

```
python cal_cfs_static_example.py # Calculate and build the Green's function library, then compute the static Coulomb failure stress.
```

# Usage (Dynamic CFS)

## Building the Green’s Function Library

Modify the parameters in `prepare_qssp_bulk_exmaple.py` as needed:

- `processes_num`: Number of parallel cores.
- `event_depth_list`: Depth list of the source fault.
- `receiver_depth_list`: Depth list of the observation fault.
- `path_green`: Path to the Green’s function library.
- `path_bin`: Path to the compiled `qssp2020.bin` executable file.
- `spec_time_window`: Length of the Green's function time window.
- `time_window`: Length of the waveform time window.
- `time_reduction`: Start time of the time window.
- `dist_range`: Epicentral distance (degrees).
- `delta_dist_range`: Epicentral distance interval for the Green's function (km).
- `sampling_interval`: Sampling interval (seconds).
- `max_frequency`: Maximum frequency (Hz).
- `max_slowness`: Maximum slowness (s/km).
- `anti_alias`: Anti-aliasing factor.
- `turning_point_filter`: Refer to `qssp2020.inp`.
- `turning_point_d1`: Refer to `qssp2020.inp`.
- `turning_point_d2`: Refer to `qssp2020.inp`.
- `free_surface_filter`: Whether or not to compute free surface reflections.
- `gravity_fc`: Upper frequency limit for gravity calculations.
- `gravity_harmonic`: Upper harmonic order for gravity calculations.
- `cal_sph`: Whether or not to compute spherical modes.
- `cal_tor`: Whether or not to compute toroidal modes.
- `min_harmonic`: Minimum harmonic order.
- `max_harmonic`: Maximum harmonic order.
- `output_observables`: List of observables to output. The order should match the one in `qssp2020.inp`, where the 6th is stress (must be 1), and others can be set to 0 or 1 as needed.
- `path_nd`: Path to the Earth model.
- `earth_model_layer_num`: Number of layers in the Earth model, starting from the surface.

**Note:** 1. In near-field cases, you may need larger spherical harmonic orders for `min_harmonic` and `max_harmonic`; 2. The `path_green` parameter should be as short as possible.

Modify the `path_green` parameter in `create_qssp_bulk_exmaple.py` to ensure it matches the one in `prepare_qssp_bulk_exmaple.py`.

Ensure that the `cfs` virtual environment is activated, and use the following commands:

```
python prepare_qssp_bulk_exmaple.py # Generate subdirectories and inp files
python create_qssp_bulk_exmaple.py # Use a single node with multiple cores to compute the Green's function library.
```

or

```
mpirun -n 8 python create_qssp_bulk_mpi_exmaple.py # Use multi-node multi-core computation for the Green's function library, where 8 is the number of cores and should match `processes_num`.
```

Wait for the program to finish.

## Calculating Dynamic Coulomb Failure Stress Changes

In `prepare_cfs_dynamic_example.py`, modify the following parameters:

- `processes_num`: Number of parallel cores.
- `path_output`: Output directory, same as in `prepare_cfs_dynamic_example.py`.
- `path_green`: Path to the precomputed Green's function library.
- `path_faults_source`: Path to the source fault file (Note: In Python, indexing starts at 0, and the file name is `sub_faults_plane%d.npy % ind`).
- `source_inds`: Index of the source fault.
- `field_points`: Coordinates of field points (lat, lon, dep).
- `field_fms`: Fault mechanisms of the field points (strike, dip, rake). The specific numpy array format can be referenced from the `npy` files in the `path_faults_example` directory.
- `points_geo`: Points in the Green’s function library, generated using the `create_points(dist_range, delta_dist)` function.

 `dist_range` and `delta_dist` should match the ones used when building the Green’s function library.

- `event_depth_list`: Depth list of the source fault, which must match the one used when building the Green’s function library.
- `receiver_depth_list`: Depth list of the observation fault, which must match the one used when building the Green’s function library.
- `srate_stf`: Sampling rate of the sub-fault source time function.
- `srate_cfs`: Sampling rate of the dynamic stress library.
- `N_T`: Number of time points. If the time window length was 255 and the sampling interval was 1 when building the Green's function library, set this value to 256.
- `time_reduction`: The inverse of `time_reduction` used when building the Green’s function library. For example, if `time_reduction` was set to -10 when building the library, this value should be set to 10.
- `mu_f`: Friction coefficient.
- `mu_f_pore`: Friction coefficient in the presence of pore pressure.
- `B_pore`: Skempton's coefficient.
- `interp`: Whether to perform spatiotemporal interpolation.

Modify `path_output` in `cal_cfs_dynamic_example.py` to ensure it is the same as in `prepare_cfs_dynamic_example.py`.

Run:

```
python prepare_cfs_dynamic_example.py # Generate the corresponding pkl file
mpirun -n 8 python cal_cfs_dynamic_example.py # Run in parallel using mpi, where 8 is `processes_num`.
```

## Reading Dynamic Coulomb Failure Stress Results

In `read_cfs_dynamic_example.py`, set the following parameters:

- `path_output`: Same as in `prepare_cfs_dynamic_example.py`.
- `path_obs_faults`: Path where the observation fault files are stored (Note: In Python, indexing starts at 0, and the fault files in `path_obs_faults` are named `sub_faults_plane_exp%d.npy % ind`).
- `inds_obs`: List of observation fault indices.

You can then use `plot_cfs_dynamic_example.py` to generate plots. The meaning of each parameter is as follows:

- `n_t_list`: List of time points, without units.
- `nrows`: Number of rows in the subplot.
- `ncols`: Number of columns in the subplot.
- `srate`: Sampling rate (Hz).
- `path_output`: Same as in `prepare_cfs_dynamic_example.py`.
- `path_obs_faults_list`: List of paths to the observation fault `.npy` files.
- `obs_plane_inds`: Index of the observation fault.
- `num_dip`: Number of sub-faults along the dip direction.
- `sub_length_km`: Length of the sub-faults (in kilometers).
- `file_name`: Name of the output file, without the extension.

```
python read_cfs_dynamic_example.py # Read the results
python plot_cfs_dynamic_example.py # Generate plots.
```

This will generate the files `file_name.png`, `file_name.svg`, and `file_name.pdf` in the current directory.
