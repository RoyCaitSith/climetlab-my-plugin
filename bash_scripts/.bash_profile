# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin
export PATH

unset USERNAME

alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"
alias cdcfeng="cd /uufs/chpc.utah.edu/common/home/zpu-group30/cfeng"
alias cdhome="cd /uufs/chpc.utah.edu/common/home/u1237353"
alias cdscratch="cd /scratch/general/nfs1/u1237353"
alias cdgoes="cd /uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance"
alias cdcpex="cd /uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX"
alias cdtropics="cd /uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/TROPICS"
alias cdsoftware="cd /uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software"
alias cdgsi="cd /uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/comGSIv3.7_EnKFv1.3"

module purge
module load ncl
module load perl
module load grib
module load ncview
module load aws-cli/2.2.29
module load cmake/3.13.3
#module load cmake/3.21.4
module load intel-oneapi-compilers/2021.4.0
module load openmpi/4.1.1
module load netcdf-c/4.8.1 netcdf-fortran/4.5.3
module load parallel-netcdf/1.12.2
module load hdf5/1.10.7

# GSI V3.7
#module load intel-oneapi-compilers/2021.4.0 intel-oneapi-mpi/2021.4.0 intel-oneapi-mkl/2022.0.2 hdf5/1.10.7
#module load netcdf-c/4.9.0 netcdf-cxx netcdf-fortran

#export NETCDF="/uufs/chpc.utah.edu/sys/spack/linux-rocky8-nehalem/intel-2021.4.0/netcdf-impi"
#export PATH="$NETCDF:$PATH"
#export LD_LIBRARY_PATH="$NETCDF/lib:$LD_LIBRARY_PATH"
#export HDF5="$HDF5_ROOT"
#export PATH="$HDF5:$PATH"
#export LD_LIBRARY_PATH="$HDF5/lib:$LD_LIBRARY_PATH"

# Environment for WRF and WPS
export NETCDF="/uufs/chpc.utah.edu/sys/spack/linux-rocky8-nehalem/intel-2021.4.0/netcdf-ompi"
export PATH="$NETCDF:$PATH"
export LD_LIBRARY_PATH="$NETCDF/lib:$LD_LIBRARY_PATH"
export HDF5="$HDF5_ROOT"
export PATH="$HDF5:$PATH"
export LD_LIBRARY_PATH="$HDF5/lib:$LD_LIBRARY_PATH"

export J="-j 8"
export WRF_EM_CORE="1"
export WRFIO_NCD_LARGE_FILE_SUPPORT="1"
export DIR="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software"
export JASPERLIB="$DIR/grib2/lib"
export JASPERINC="$DIR/grib2/include" 

# Environment for WRFPLUS, RTTOV, WRFDA, and DART
#export NETCDF="/uufs/chpc.utah.edu/sys/spack/linux-rocky8-nehalem/intel-2021.4.0/netcdf-ompi"
#export PATH="$NETCDF:$PATH"
#export LD_LIBRARY_PATH="$NETCDF/lib:$LD_LIBRARY_PATH"
#export HDF5="$HDF5_ROOT"
#export PATH="$HDF5:$PATH"
#export LD_LIBRARY_PATH="$HDF5/lib:$LD_LIBRARY_PATH"

#export WRFPLUS_DIR="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/DART/WRFPLUS"
#export RTTOV="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/DART/rttov_12.1"

# NCEPlibs
#export DIR="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software"
#export JASPER_INC="$DIR/grib2/include" 
#export PNG_INC="$JASPER_INC"

# UPP
#export NCEPLIBS_DIR="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/NCEPlibs"

# Environment for GFDL Vortex Tracker
#export PNETCDF=$PARALLEL_NETCDF_ROOT
#export PATH="$PNETCDF:$PATH"
#export LD_LIBRARY_PATH="$PNETCDF/lib:$LD_LIBRARY_PATH"
#export DIR="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software"
#export JASPERLIB="$DIR/grib2/lib"
#export JASPERINC="$DIR/grib2/include" 
#export LIB_Z_PATH="$JASPERLIB"
#export LIB_PNG_PATH="$JASPERLIB"
#export LIB_JASPER_PATH="$JASPERLIB"

# GSI Github
#module use /uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/hpc-stack/modulefiles/stack
#module load hpc/1.2.0
#module load hpc-intel/18.0.5
#module load hpc-impi/2018.4.274
#module load nemsio/2.5.4
#module load sfcio/1.4.1
#module load sigio/2.3.2
#module load sp/2.3.3
#module load w3nco/2.4.1
#module load wrf_io/1.2.0
#module load bacio/2.4.1
#module load crtm/2.3.0
#module load g2/3.4.1
#module load g2tmpl/1.9.1
#module load w3emc/2.9.2
#module load gfsio/1.4.1
#module load bufr/11.5.0
#module load ip/3.3.3

# Environment for CRTM
#export libroot="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/crtm_v2.3.0"
#export FCFLAGS="-I$libroot/include $FCFLAGS"
#export LDFLAGS="-L$libroot/lib $LDFLAGS"
#export LIBS="-lcrtm"

# Create BUFR File
#export GSI_DIR="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/comGSIv3.7_EnKFv1.3"
#export GSI_DIR_LIB="$GSI_DIR/build/lib" 
#export HDF5="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/hdf5"
#export HDF5_LIB="$HDF5/lib"
#export LD_LIBRARY_PATH="$NETCDF/lib:$LD_LIBRARY_PATH"
#export LD_LIBRARY_PATH="$GSI_DIR_LIB:$LD_LIBRARY_PATH"
#export LD_LIBRARY_PATH="$HDF5_LIB:$LD_LIBRARY_PATH"
#export FCFLAGS="-I$NETCDF/include $FCFLAGS"
#export FCFLAGS="-I$GSI_DIR/build/include $FCFLAGS"
#export FCFLAGS="-I$HDF5/include $FCFLAGS"

# Environment for installing HWRF
#export DIR="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software"
#export SCRATCH="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/HWRF"
#export HOMEhwrf="${SCRATCH}/hwrfrun"
#export HWRF=1
#export WRF_NMM_CORE=1
#export WRF_NMM_NEST=1
#export WRFIO_NCD_LARGE_FILE_SUPPORT=1
#export PNETCDF_QUILT=1
#export JASPERLIB="${DIR}/grib2/lib/"
#export JASPERINC="${DIR}/grib2/include/"
#export WRF_DIR="${SCRATCH}/hwrfrun/sorc/WRF/"
#export LAPACK_PATH="${MKLROOT}"
#export LIB_W3_PATH="${SCRATCH}/hwrfrun/sorc/hwrf-utilities/libs/"
#export LIB_SP_PATH="${SCRATCH}/hwrfrun/sorc/hwrf-utilities/libs/"
#export LIB_SFCIO_PATH="${SCRATCH}/hwrfrun/sorc/hwrf-utilities/libs/"
#export LIB_BACIO_PATH="${SCRATCH}/hwrfrun/sorc/hwrf-utilities/libs/"
#export LIB_NEMSIO_PATH="${SCRATCH}/hwrfrun/sorc/hwrf-utilities/libs/"
#export LIB_G2_PATH="${SCRATCH}/hwrfrun/sorc/hwrf-utilities/libs/"
#export PNETCDF="$DIR/PnetCDF"
#export LIB_BLAS_PATH="${SCRATCH}/hwrfrun/sorc/hwrf-utilities/libs/"
#export LIB_Z_PATH="${JASPERLIB}"
#export LIB_PNG_PATH="${JASPERLIB}"
#export LIB_JASPER_PATH="${JASPERLIB}"

# ECMWF
#export ECMWF_API_URL="https://api.ecmwf.int/v1"
#export ECMWF_API_KEY="f0e9e36bd2c4ce37ff7b84c9ae29aa5b"
#export ECMWF_API_EMAIL="mg1528002@smail.nju.edu.cn"

# DART
#export DART_DIR="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/DART"
#export BASE_DIR="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/TROPICS/06_20220203/work"

# Miniconda3
export PATH="/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/mymini3/bin:$PATH"
export PYTHONPATH="$HOME/climetlab-my-plugin/functions:$PYTHONPATH"
