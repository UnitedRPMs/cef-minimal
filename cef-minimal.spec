%define _legacy_common_support 1
%define debug_package %{nil}
%global _hardened_build 1

%global _commit ge484012
%global _chromiumver 88.0.4324.150
%global cdn_build_package_url https://cef-builds.spotifycdn.com
%global _url_pkgver %{version}%2B%{_commit}%2Bchromium-%{_chromiumver}

# Reduce compression level and build time
%define _source_payload w5.gzdio
%define _binary_payload w5.gzdio

%global _build_id_links none
%undefine __brp_check_rpaths
%global __brp_check_rpaths %{nil}


Name: cef-minimal
Summary: Chromium Embedded Framework minimal release
Version: 88.2.8
Release: 3%{?dist}
URL: https://bitbucket.org/chromiumembedded/cef/
Group: System Environment/Libraries
Source:	%{cdn_build_package_url}/cef_binary_%{_url_pkgver}_linux64_minimal.tar.bz2
License: BSD
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: chrpath
#BuildRequires: ninja-build
Requires:      expat

%description
Chromium Embedded Framework minimal release.

%prep
%autosetup -n cef_binary_%{version}+%{_commit}+chromium-%{_chromiumver}_linux64_minimal
cp -rf %{_builddir}/cef_binary_%{version}+%{_commit}+chromium-%{_chromiumver}_linux64_minimal %{_builddir}/cef_binary_static

%build
mkdir -p build
    sed -i 's/-Werror/#-Werror/g' cmake/cef_variables.cmake
# Static build
    #cmake -G "Ninja" -DPROJECT_ARCH="x86_64" -DCMAKE_BUILD_TYPE=Release -Wno-dev .
    %cmake -Wno-dev -B build
    pushd build
    make libcef_dll_wrapper
    popd
# static build
mkdir -p %{_builddir}/cef_binary_static/build
 pushd %{_builddir}/cef_binary_static/
    %cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DCMAKE_SKIP_RPATH=1 -Wno-dev -B build
    pushd build
    make libcef_dll_wrapper
    popd
      popd
    
   cp -f %{_builddir}/cef_binary_static/build/libcef_dll_wrapper/libcef_dll_wrapper.a %{_builddir}/cef_binary_%{version}+%{_commit}+chromium-%{_chromiumver}_linux64_minimal/build/libcef_dll_wrapper/

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

* Thu Aug 12 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 88.2.8-3
- Rebuilt

* Mon Apr 12 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 88.2.8-2
- Updated to 88.2.8

* Mon Sep 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 75.1.14-2
- Rebuilt 

* Sat Apr 18 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 75.1.14-1 
- initial RPM
