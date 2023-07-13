module purge
module load ncl
module load ncview
module load cmake/3.21.4
module load perl

# GSI V3.7
#module load intel-oneapi-compilers/2021.4.0 intel-oneapi-mpi/2021.4.0 intel-oneapi-mkl/2022.0.2 hdf5
#module load netcdf-c netcdf-cxx netcdf-fortran
module load intel-oneapi-compilers/2021.4.0 intel-oneapi-mpi/2021.4.0 intel-oneapi-mkl/2022.0.2 hdf5/1.12.2
module load netcdf-c/4.9.0 netcdf-cxx netcdf-fortran

export NETCDF="/uufs/chpc.utah.edu/sys/spack/linux-rocky8-nehalem/intel-2021.4.0/netcdf-impi"
export PATH="$NETCDF:$PATH"
export LD_LIBRARY_PATH="$NETCDF/lib:$LD_LIBRARY_PATH"
export HDF5="$HDF5_ROOT"
export PATH="$HDF5:$PATH"
export LD_LIBRARY_PATH="$HDF5/lib:$LD_LIBRARY_PATH"
