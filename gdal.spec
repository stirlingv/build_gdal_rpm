# 
# spec file for package gdal
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%bcond_with ecw_support
# Soname should be bumped on API/ABI break
# http://trac.osgeo.org/gdal/ticket/4543
%define soversion 20
%define sourcename gdal

Name:           gdal
Version:        2.2.3
Release:        0
Summary:        GDAL/OGR - a translator library for raster and vector geospatial data formats
License:        MIT and BSD-3-Clause and SUSE-Public-Domain
Group:          Development/Libraries/C and C++
Url:            http://www.gdal.org/
Source0:        SOURCES/%{name}/%{version}/%{sourcename}-%{version}.tar.xz
Patch0:         gdal-perl.patch
# Fix occasional parallel build failure
Patch1:         GDALmake.opt.in.patch
# Fix hard coded name of libproj library
# But libproj.so is valid if libproj-devel is installed ?
Patch2:         gdal-libproj.patch
# PATCH-FIX-UPSTREAM gdal-json-c-0.13.patch dimstar@opensuse.org -- Fix build with json-c 0.13; copied from gentoo
Patch3:         gdal-json-c-0.13.patch
BuildRequires:  blas-devel
BuildRequires:  chrpath
BuildRequires:  curl-devel
BuildRequires:  dos2unix
BuildRequires:  doxygen >= 1.4.2
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  geos-devel >= 3
BuildRequires:  libgeotiff-devel >= 1.2.1
BuildRequires:  giflib-devel
BuildRequires:  lapack-devel
BuildRequires:  expat-devel >= 1.95.0
# No more please we have openjpeg2
# BuildRequires:  libjasper-devel
# Using jasper create build error on arm, powerpc, s390
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  proj-devel
BuildRequires:  libspatialite-devel
BuildRequires:  libtiff-devel >= 3.6.0
BuildRequires:  libtool
BuildRequires:  xerces-c-devel
BuildRequires:  libxml2-devel
BuildRequires:  mysql-devel
BuildRequires:  netcdf-devel
BuildRequires:  opencl-headers
BuildRequires:  openjpeg2-devel
#BuildRequires:  perl-macros
BuildRequires:  postgresql-devel
#BuildRequires:  python-numpy-devel #need added to yum repo
#BuildRequires:  python-setuptools
#BuildRequires:  python3-numpy-devel
#BuildRequires:  python3-setuptools
BuildRequires:  sqlite-devel >= 3
BuildRequires:  swig
#BuildRequires:  unixODBC-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel >= 1.1.4
#BuildRequires:  pkgconfig(poppler)
BuildRequires:  pkgconfig
%if %{with ecw_support}
BuildRequires:  libecwj2-devel
%endif
%if 0%{?suse_version} >= 1310
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  freexl-devel
BuildRequires:  hdf5-devel
BuildRequires:  libwebp-devel
%endif
%if 0%{?suse_version} > 1320
BuildRequires:  json-c-devel
BuildRequires:  ocl-icd-devel
BuildRequires:  opencl-headers
BuildRequires:  perl-ExtUtils-MakeMaker
%else
BuildRequires:  hdf-devel >= 4.0
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
GDAL is a translator library for raster geospatial data formats that
is released under an Open Source license. As a library, it presents a
single abstract data model to the calling application for all
supported formats. The related OGR library (which lives within the
GDAL source tree) provides a similar capability for simple features
vector data.

%package devel
Summary:        GDAL library header files
Group:          Development/Languages/C and C++
Requires:       lib%{name}%{soversion} = %{version}
Provides:       lib%{name}%{soversion}-devel
Provides:       lib%{name}-devel

%description devel
Development Libraries for the GDAL file format library

%package -n lib%{name}%{soversion}
Summary:        GDAL static libraries
Group:          System/Libraries

%description -n lib%{name}%{soversion}
GDAL and OGR are translator libraries for raster and vector geospatial data
formats. As a library, it presents a single abstract data model to the calling
application for all supported formats.

%package -n perl-%{name}
Summary:        Perl bindings for GDAL
Group:          Development/Languages/Perl
Requires:       %{name} = %{version}-%{release}
%if 0%{?suse_version} < 1140
Requires:       perl = %{perl_version}
%else
%{perl_requires}
%endif

%description -n perl-%{name}
Perl bindings for GDAL - Geo::GDAL, Geo::OGR and Geo::OSR modules.

%package -n python-%{name}
Summary:        GDAL Python module
Group:          Development/Languages/Python
Requires:       %{name} = %{version}-%{release}
Provides:       python2-%{name} = %{version}
#%py_requires

%description -n python-%{name}
The GDAL python modules provide support to handle multiple GIS file formats.

%package -n python3-%{name}
Summary:        GDAL Python3 module
Group:          Development/Languages/Python
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{name}
The GDAL python modules provide support to handle multiple GIS file formats.

%prep
%setup -q -n %{sourcename}-%{version}
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1

# Fix mandir
sed -i "s|^mandir=.*|mandir='\${prefix}/share/man'|" configure

# Fix wrong encoding EOL
for F in frmt_twms_srtm.xml frmt_wms_bluemarble_s3_tms.xml frmt_wms_virtualearth.xml frmt_twms_Clementine.xml;do
  find . -name "${F}" -exec dos2unix {} \;
done

#Fix wrong /usr/bin/env phyton
#Create the move to python3
find . -iname "*.py" -exec sed -i 's,^#!/usr/bin/env python$,#!/usr/bin/python3,' {} \;

%build
# need to regenerate (old one does not accept CFLAGS)
#autoreconf -fi

%configure \
        --prefix=%{_prefix}     \
        --includedir=%{_includedir}/gdal \
        --datadir=%{_datadir}/gdal \
        --with-threads          \
        --disable-static        \
        --with-geotiff          \
        --with-libtiff          \
        --with-rename-internal-libtiff-symbols=yes \
        --with-rename-internal-libgeotiff-symbols=yes \
        --with-libz             \
        --with-liblzma          \
        --with-cfitsio=no       \
        --with-netcdf           \
        --with-openjpeg         \
        --with-curl             \
        --with-pg               \
        --with-ogdi             \
        --without-pcraster      \
        --with-jpeg12=no        \
        --without-libgrass      \
        --without-grass         \
        --enable-shared         \
        --with-geos             \
        --with-expat            \
        --without-jasper        \
        --with-png              \
        --with-gif              \
        --with-jpeg             \
        --with-spatialite       \
        --with-poppler          \
        --with-mysql            \
        --with-freexl           \
        --with-xerces=yes       \
        --with-xerces-lib="-lxerces-c" \
        --with-xerces-inc=%{_includedir}/xercesc \
        --without-python        \
%if %{with ecw_support}
        --with-ecw              \
        CFLAGS="$CFLAGS -pthread" \
%endif
%if 0%{?suse_version} > 1320
        --with-opencl           \
%endif
%if 0%{?suse_version} > 1310
        --without-hdf4          \
        --with-hdf5             \
        --with-webp             \
%else
        --with-hdf4             \
%endif
        --disable-rpath

# regenerate where needed
for M in perl python;
do
  make %{?_smp_mflags} -C swig/${M} veryclean
  make %{?_smp_mflags} -C swig/${M} generate
done

make %{?_smp_mflags} VERBOSE=1 all docs man

# Make Python 3 module
pushd swig/python
#  python3 setup.py build
popd

%install

# Install Python 3 module
# Must be done first so executables are env python
pushd swig/python
#  python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

make %{?_smp_mflags} install install-man \
  DESTDIR=%{buildroot} INST_MAN=%{_mandir}

# Not on buildroot : broke everything with python3
# If done got python3 needing python2 package heretic ..
# Futhermore duplicates are only existing in src html dir
%fdupes -s html
# Empty file
rm -f html/do-not-remove

# chrpath must be removed here
#chmod 644 %{buildroot}%{perl_vendorarch}/auto/Geo/GDAL/Const/Const.so
#chmod 644 %{buildroot}%{perl_vendorarch}/auto/Geo/GDAL/GDAL.so
#chmod 644 %{buildroot}%{perl_vendorarch}/auto/Geo/GNM/GNM.so
#chmod 644 %{buildroot}%{perl_vendorarch}/auto/Geo/OGR/OGR.so
#chmod 644 %{buildroot}%{perl_vendorarch}/auto/Geo/OSR/OSR.so

#chrpath --delete %{buildroot}%{perl_vendorarch}/auto/Geo/GDAL/Const/Const.so
#chrpath --delete %{buildroot}%{p
