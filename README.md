# Introduction

This project serves as a Python frontend, based on Professor Wang‘s Fortran programs, to compute and build the stress Green’s function library, and to calculate the dynamic and static Coulomb failure stress changes for a given finite-fault model. (Chinese README: https://github.com/Zhou-Jiangcheng/coulomb_failure_stress_change_example/blob/main/README_zh.md)

References:

Wang, Rongjiang. (1999). A simple orthonormalization method for stable and efficient computation of Green’s functions.  *Bulletin of the Seismological Society of America* ,  *89* (3), 733–741. [https://doi.org/10.1785/BSSA0890030733](https://doi.org/10.1785/BSSA0890030733)

Wang, R. (2003). Computation of deformation induced by earthquakes in a multi-layered elastic crust—FORTRAN programs EDGRN/EDCMP.  *Computers & Geosciences* ,  *29* (2), 195–207. [https://doi.org/10.1016/S0098-3004(02)00111-5](https://doi.org/10.1016/S0098-3004(02)00111-5)

Wang, Rongjiang, Heimann, S., Zhang, Y., Wang, H., & Dahm, T. (2017). Complete synthetic seismograms based on a spherical self-gravitating Earth model with an atmosphere–ocean–mantle–core structure.  *Geophysical Journal International* ,  *210* (3), 1739–1764.

# Installation

Clone this repo with

```
git clone --recurse-submodules https://github.com/Zhou-Jiangcheng/coulomb_failure_stress_change_example
```

On Debian-based Linux, use the following command to install the `gfortran` compiler:

```
sudo apt install gfortran
```

In the `qssp2020_src` folder, use the command:

```
gfortran ./*.f -O3 -o qssp2020.bin
```

to compile and generate the executable file.

Similarly, in the `edgrn2.0-f77code` and `edcmp2.0-f77code` folders, use the following commands to compile and generate the executables:

```
gfortran ./*.f -O3 -o edgrn2.0
```

```
gfortran ./*.f -O3 -o edcmp2.0
```

Next, install Anaconda3 or Miniforge, and use the following commands:

```
conda create -n cfs python=3.11 # Create a virtual environment named cfs
conda activate cfs # Activate the virtual environment
conda install numpy scipy pandas tqdm mpi4py -c conda-forge # Install dependencies
```

Add the folder path containing this Python library to the environment.

For example, if the project folder path is `/home/mydir/coulomb_failure_stress_change_example`, create and add `/home/mydir`/`coulomb_failure_stress_change_example` to the `/path_anaconda/envs/cfs/lib/python3.11/site-packages/custom.pth` file.

# Usage (static)

Modify the various parameters in `cal_cfs_static_example.py` according to your requirements. The meaning of each parameter is as follows:

- `processes_num`: Number of cores used for parallel processing.
- `path_output`: Output path.
- `path_bin_edgrn`: Path of the executable file named `edgrn2.0`.
- `path_bin_edcmp`: Path of the executable file named `edcmp2.0`.
- `ref_point`: Reference point used when converting fault coordinates from the geographic coordinate system (lat, lon, dep) to the Cartesian coordinate system. It is recommended to use the geometric center of the entire region formed by the source and observation faults to reduce computational cost.
- `path_faults_source`: Path where the source fault file is stored (Note: in Python, indexing starts from 0; the name is `sub_faults_plane%d.npy % ind`).
- `source_inds`: Index of the source fault.
- `path_faults_obs`: Path of the observation fault.
- `obs_plane_inds`: Index of the observation fault.
- `sub_length_source`: Size of sub-faults on the source fault.
- `sub_length_obs`: Size of sub-faults on the observation fault.
- `source_dep_list`: Depth list of the source fault.
- `obs_dep_list`: Depth list of the observation fault.
- `lat_range`: Latitude range of the observation fault.
- `lon_range`: Longitude range of the observation fault.
- `rmax_grn`: Maximum radius when calculating the Green's function library using `edgrn`.
- `hs_flag=1/0`: Indicates whether to use the infinite half-space model. If set to 1, the layered Earth model is used, and you don't need to provide `lam` and `mu`. If set to 0, the infinite half-space model is used, `edgrn` will not run, and `edcmp` will directly calculate the displacement.
- `path_nd`: Path to the Earth model when using `edgrn`.
- `earth_model_layer_num`: Number of layers in the Earth model, starting from the surface.
- `lam`: Elastic parameter when using the infinite half-space model.
- `mu`: Elastic parameter when using the infinite half-space model.

All units are in international standard units.

Ensure that the `cfs` virtual environment is activated, then run the following command:

```
python cal_cfs_static_example.py # Calculate and establish the Green's function library, then compute the static Coulomb failure stress
```

# Usage (dynamic)

## Building the Green’s Function Library

Modify the parameters in the `prepare_qssp_bulk_exmaple.py` file according to your requirements. The `processes_num` represents the number of parallel cores, `path_green` should be set to the path of the Green’s function library, and `path_bin` should point to the path of the compiled `qssp2020.bin` executable file. Other parameters are the same as in the `qssp2020.inp` file.

In the `create_qssp_bulk_exmaple.py`, adjust the `path_green` parameter to ensure it matches the one in `prepare_qssp_bulk_exmaple.py`.

Note:

1. In the near-field cases, it may be necessary to increase the spherical harmonic order `min_harmonic` and `max_harmonic`.
2. The `path_green` parameter should not be too long, the shorter, the better.

Ensure that the `cfs` virtual environment is activated, then use the following commands:

```
python prepare_qssp_bulk_exmaple.py # Generate subdirectories and inp files
python create_qssp_bulk_exmaple.py # Use a single node with multiple cores to compute the Green's function library
```

or

```
python prepare_qssp_bulk_exmaple.py # Generate subdirectories and inp files
mpirun -n 8 python create_qssp_bulk_mpi_exmaple.py # Use multi-node multi-core computation of the Green's function library, where 8 is the number of cores, which should match the `processes_num` set earlier
```

Wait for the program to finish.

## Calculating Dynamic Coulomb Failure Stress Changes

In the `prepare_cfs_dynamic_example.py`, set the file storage path for the source fault `path_faults_source` and the index `source_inds` (Note: in Python, the index starts from 0, and the name is `sub_faults_plane%d.npy % ind`). Read the coordinates of the observation points `(lat, lon, dep)` and the fault mechanism at those points `(strike, dip, rake)`. Refer to the `npy` files in `path_faults_example` for the specific numpy array format.

The `path_output` is the directory for dynamic stress outputs, and `processes_num` still refers to the number of parallel cores. Other parameters such as `dist_range`, `delta_dist`, `path_green`, etc., should be the same as those used when creating the Green's function library.

Run the following commands:

```
python prepare_cfs_dynamic_example.py # Prepare the corresponding pkl file
mpirun -n 8 python cal_cfs_dynamic_example.py # Use mpi for parallel execution, where 8 is the `processes_num`
```

## Reading Dynamic Coulomb Failure Stress Results

In `read_cfs_dynamic_example.py`, set `path_output` to match the one in `prepare_cfs_dynamic_example.py`, and set `path_obs_faults` and `inds_obs` (Note: the index in Python starts from 0, and the fault files for observation points in `path_obs_faults` are named `sub_faults_plane_exp%d.npy % ind`).

Afterward, you can use `plot_cfs_dynamic_example.py` to plot the results. The parameter `n_t_list` is a list of time points (without units), `num_dip` is the number of sub-faults along the dip direction, `sub_length_km` is the length of the sub-faults, and `file_name` is the name of the output file.

```
python read_cfs_dynamic_example.py # Read the results
python plot_cfs_dynamic_example.py # Generate plots
```

This will generate image files `file_name.png`, `file_name.svg`, and `file_name.pdf` in the current directory.
