# 简介

此项目作为Python前端，基于汪荣江老师的Fortran程序计算和建立动态和静态应力格林函数库，并计算给定有限断层模型时的动态和静态库仑破裂应力变化。

参考文献：

Wang, Rongjiang. (1999). A simple orthonormalization method for stable and efficient computation of Green’s functions.  *Bulletin of the Seismological Society of America* ,  *89* (3), 733–741. [https://doi.org/10.1785/BSSA0890030733](https://doi.org/10.1785/BSSA0890030733)

Wang, R. (2003). Computation of deformation induced by earthquakes in a multi-layered elastic crust—FORTRAN programs EDGRN/EDCMP.  *Computers & Geosciences* ,  *29* (2), 195–207. [https://doi.org/10.1016/S0098-3004(02)00111-5](https://doi.org/10.1016/S0098-3004(02)00111-5)

Wang, Rongjiang, Heimann, S., Zhang, Y., Wang, H., & Dahm, T. (2017). Complete synthetic seismograms based on a spherical self-gravitating Earth model with an atmosphere–ocean–mantle–core structure.  *Geophysical Journal International* ,  *210* (3), 1739–1764.

# 安装

克隆这个项目

```
git clone --recurse-submodules https://github.com/Zhou-Jiangcheng/coulomb_failure_stress_change_example
```

在Debian系Linux上，使用

```
sudo apt install gfortran
```

安装gfortran编译器。

在 qssp2020_src文件夹使用命令

```
gfortran ./*.f -O3 -o qssp2020.bin
```

编译生成可执行文件。

同理在 edgrn2.0-f77code和 edcmp2.0-f77code文件夹使用

```
gfortran ./*.f -O3 -o edgrn2.0
```

```
gfortran ./*.f -O3 -o edcmp2.0
```

编译生成可执行文件。

之后安装Anaconda3或者Miniforge，并使用命令

```
conda create -n cfs python=3.11 # 建立虚拟环境 cfs
conda activate cfs # 激活虚拟环境
conda install numpy scipy pandas tqdm mpi4py -c conda-forge # 安装依赖项
```

添加文件夹路径。例如，你clone的项目在 /home/mydir/coulomb_failure_stress_change_example，那么在创建文件/path_anaconda/envs/cfs/lib/python3.11/site-packages/custom.pth，并在其中添加一行/home/mydir/coulomb_failure_stress_change_example。

# 使用 (静态cfs)

根据需求修改cal_cfs_static_example.py中的各项参数，其中各参数意义如下：

processes_num 并行时的核心数

path_output 输出路径

path_bin_edgrn 名称为edgrn2.0的可执行文件的路径

path_bin_edgrn 名称为edcmp2.0的可执行文件的路径

ref_point 将断层坐标从地理坐标系（lat,lon,dep)转换到直角坐标系时的参考点，推荐使用接近源和观测断层构成的整体区域的几何中心点以减少计算量

path_faults_source 作为源的断层文件存储路径（注意，Python中序号从0开始，名称为sub_faults_plane%d.npy % ind)

source_plane_inds 源断层序号列表

path_faults_obs 作为观测断层的断层文件存储路径

obs_plane_inds 观测断层的序号列表

sub_length_source 源断层上的子断层尺度

sub_length_obs 观测断层上的子断层尺度

source_dep_list 源断层的深度列表

obs_dep_list 观测断层的深度列表

lat_range 观测断层的纬度范围

lon_range 观测断层的经度范围

rmax_grn 使用edgrn计算格林函数库时的最大半径

hs_flag=1/0为是/否使用无限半空间模型，如果选择1，表示使用分层地球模型，可以不填写lam和mu；如果选择0，表示使用使用无限半空间模型，将不会运行edgrn，直接使用edcmp计算位移

path_nd 使用edgrn时的地球模型

earth_model_layer_num 地球模型中需要使用的层数，从地表起

lam 使用无限半空间模型时的弹性参数

mu 使用无限半空间模型时的弹性参数

单位均为国际标准单位。

保证cfs虚拟环境已经激活，之后运行如下命令：

```
python cal_cfs_static_example.py # 计算并建立格林函数库，之后计算静态库仑破裂应力
```

# 使用 (动态cfs)

## 建立格林函数库

根据需求修改prepare_qssp_bulk_exmaple.py文件中的各项参数：

processes_num 并行核心数目

event_depth_list 源断层的深度列表

receiver_depth_list 观测断层的深度列表

path_green 格林函数库的路径

path_bin 编译好的qssp2020.bin可执行文件的路径

spec_time_window 格林函数的窗长

time_window 波形的窗长

time_reduction 时间窗口的开始时间

dist_range 震中距（deg)

delta_dist_range 格林函数震中距间隔（km)

sampling_interval 采样间隔（s)

max_frequency 最大频率（Hz)

max_slowness 最大慢度（s/km)

anti_alias 抗假频因子

turning_point_filter 参考qssp2020.inp

turning_point_d1 参考qssp2020.inp

turning_point_d2 参考qssp2020.inp

free_surface_filter 是否计算自由表面反射

gravity_fc 计算重力的频率上限

gravity_harmonic 计算重力的球谐函数阶数上限

cal_sph 是否计算球形模态

cal_tor 是否计算环形模态

min_harmonic 最小球谐函数阶数

max_harmonic 最大球谐函数阶数

output_observables 输出的观测值，与qssp2020.inp中顺序相同，其中第6个为应力，必须为1，其余可根据需要选择0或1

path_nd 地球模型

earth_model_layer_num 地球模型中需要使用的层数，从地表起


注意：1.近场情况下，可能需要较大的球谐函数阶数min_harmonic和max_harmonic；2. path_green参数不能太长，越短越好。

修改create_qssp_bulk_exmaple.py中的path_green参数，保证与prepare_qssp_bulk_exmaple.py中相同。

确保已经激活cfs虚拟环境，使用

```
python prepare_qssp_bulk_exmaple.py # 生成子目录和inp文件
python create_qssp_bulk_exmaple.py # 使用单节点多核心计算格林函数库

```

或者

```
python prepare_qssp_bulk_exmaple.py # 生成子目录和inp文件
mpirun -n 8 python create_qssp_bulk_mpi_exmaple.py # 使用多节点多核心计算格林函数库，其中8为核心数，需要与之前设置的processes_num相同
```

等待程序执行完毕。

## 计算动态库仑破裂应力变化

在prepare_cfs_dynamic_example.py中修改各项参数：

processes_num 并行核心数目

path_output 结果输出目录，与prepare_cfs_dynamic_example.py中相同

path_green 已经计算好的格林函数库的路径

path_faults_source 作为源的断层文件存储路径（注意，Python中序号从0开始，名称为sub_faults_plane%d.npy % ind)

source_inds 源断层序号

field_points 场点坐标(lat,lon,dep)

field_fms 场点子断层机制(strike,dip,rake)，具体numpy数组形状可参考path_faults_example目录中的npy文件

points_geo 格林函数库中的点，使用create_points(dist_range, delta_dist)函数生成，dist_range和delta_dist需要与建立格林函数库时相同

event_depth_list 源断层的深度列表，需要与建立格林函数库时相同

receiver_depth_list 观测断层的深度列表，需要与建立格林函数库时相同

srate_stf 子断层震源时间函数的采样率

srate_cfs 动态应力库的采样率

N_T 时间点数，如果之前建立格林函数库时的时窗长度为255，采样间隔为1，此处需要填256

time_reduction 建立格林函数库时time_reduction的相反数，例如建立格林函数库时为-10，则此处需要填10

mu_f 摩擦系数

mu_f_pore 存在孔隙时的摩擦系数

B_pore Skempton's 系数

interp 是否做时空插值

修改cal_cfs_dynamic_example.py中的path_output，确保与prepare_cfs_dynamic_example.py中相同。

运行

```
python prepare_cfs_dynamic_example.py # 生成对应pkl文件
mpirun -n 8 python cal_cfs_dynamic_example.py # mpi并行运行，8为processes_num
```

## 读取动态库仑破裂应力结果

在read_cfs_dynamic_example.py中设置对应参数：

path_output 与prepare_cfs_dynamic_example.py中相同

path_obs_faults 作为观测断层的断层文件存储路径（注意，Python中序号从0开始，path_obs_faults目录下的场点断层文件名称为sub_faults_plane_exp%d.npy % ind）

inds_obs 观测断层序号列表

之后可使用plot_cfs_dynamic_example.py画图，其中各参数意义如下：

n_t_list 时间点列表，无单位

nrows 子图行数

ncols 子图列数

srate 采样率（Hz)

path_output 与prepare_cfs_dynamic_example.py中相同

path_obs_faults_list 观测断层npy文件路径构成的列表

obs_plane_inds 观测断层序号

num_dip 沿倾向子断层数目

sub_length_km 子断层长度

file_name 输出文件的名称，不包含后缀

```
python read_cfs_dynamic_example.py # 读取结果
python plot_cfs_dynamic_example.py # 画图
```

即可在当前目录下生成file_name.png, file_name.svg, file_name.pdf图形文件。
