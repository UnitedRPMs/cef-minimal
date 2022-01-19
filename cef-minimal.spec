%define _legacy_common_support 1
%define debug_package %{nil}
%global _hardened_build 1

%global _commit 95e19b8
%global _chromiumver 95.0.%{_cefbranch}.69
%global cdn_build_package_url https://cdn-fastly.obsproject.com
%global _cefbranch 4638

# Reduce compression level and build time
%define _source_payload w5.gzdio
%define _binary_payload w5.gzdio

%global _build_id_links none
%undefine __brp_check_rpaths
%global __brp_check_rpaths %{nil}


Name: cef-minimal
Summary: Chromium Embedded Framework minimal release
Version: 95.0.4638.69
Release: 3%{?dist}
URL: https://bitbucket.org/chromiumembedded/cef/
Group: System Environment/Libraries
Source:	%{cdn_build_package_url}/downloads/cef_binary_%{_cefbranch}_linux64.tar.bz2
License: BSD
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: chrpath
#BuildRequires: ninja-build
Requires:      expat

%description
Chromium Embedded Framework minimal release.

%prep
%autosetup -n cef_binary_%{_cefbranch}_linux64
cp -rf %{_builddir}/cef_binary_%{_cefbranch}_linux64 %{_builddir}/cef_binary_static

%build
rm -rf build
mkdir -p build
    sed -i 's/-Werror/#-Werror/g' cmake/cef_variables.cmake
# Static build
    #cmake -G "Ninja" -DPROJECT_ARCH="x86_64" -DCMAKE_BUILD_TYPE=Release -Wno-dev .
    %cmake -Wno-dev -B build
    pushd build
    make libcef_dll_wrapper
    popd
# static build
rm -rf %{_builddir}/cef_binary_static/build
mkdir -p %{_builddir}/cef_binary_static/build
 pushd %{_builddir}/cef_binary_static/
    %cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DCMAKE_SKIP_RPATH=1 -Wno-dev -B build
    pushd build
    make libcef_dll_wrapper
    popd
      popd
    
   cp -f %{_builddir}/cef_binary_static/build/libcef_dll_wrapper/libcef_dll_wrapper.a %{_builddir}/cef_binary_%{_cefbranch}_linux64/build/libcef_dll_wrapper/
   
   
%install
mkdir -p %{buildroot}/opt/cef/
mv -f * %{buildroot}/opt/cef/
pushd %{buildroot}/opt/cef/Release/
ln -sf /opt/cef/libcef_dll_wrapper/libcef_dll_wrapper.so  libcef_dll_wrapper.so
ln -sf /opt/cef/libcef_dll_wrapper/libcef_dll_wrapper.a libcef_dll_wrapper.a
popd
 mv -f %{buildroot}/opt/cef/build/libcef_dll_wrapper %{buildroot}/opt/cef/libcef_dll_wrapper && rm -rf %{buildroot}/opt/cef/build
 
 rm -rf %{buildroot}/opt/cef/libcef_dll_wrapper/CMakeFiles/
  rm -f %{buildroot}/opt/cef/libcef_dll_wrapper/MakeFile
  
chrpath --delete %{buildroot}/opt/cef/libcef_dll_wrapper/libcef_dll_wrapper.so

%files
/opt/cef/

%changelog

* Fri Dec 31 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 95.0.4638.69-3
- Updated to 95.0.4638.69

* Thu Aug 12 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 88.2.8-3
- Rebuilt

* Mon Apr 12 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 88.2.8-2
- Updated to 88.2.8

* Mon Sep 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 75.1.14-2
- Rebuilt 

* Sat Apr 18 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 75.1.14-1 
- initial RPM
