%define _legacy_common_support 1
%define debug_package %{nil}
%global _hardened_build 1

%global _commit gb382c62
%global _chromiumver 81.0.4044.113
%global _url_gver %{version}_%{_commit}_chromium-%{_chromiumver}

Name: cef-minimal
Summary: Chromium Embedded Framework minimal release
Version: 81.2.17
Release: 1%{?dist}
URL: https://bitbucket.org/chromiumembedded/cef/
Group: System Environment/Libraries
# Source from http://opensource.spotify.com/cefbuilds/index.html (renamed and uploaded in git repo for an easy download)
Source: https://github.com/UnitedRPMs/cef-minimal/releases/download/%{version}/cef_binary_%{_url_gver}_linux64_minimal.tar.bz2
License: BSD
BuildRequires: cmake
BuildRequires: gcc-c++
#BuildRequires: ninja-build

%description
Chromium Embedded Framework minimal release.

%prep
%autosetup -n cef_binary_%{version}+%{_commit}+chromium-%{_chromiumver}_linux64_minimal
cp -rf %{_builddir}/cef_binary_%{version}+%{_commit}+chromium-%{_chromiumver}_linux64_minimal %{_builddir}/cef_binary_static
%build
    sed -i 's/-Werror/#-Werror/g' cmake/cef_variables.cmake
# Static build
    #cmake -G "Ninja" -DPROJECT_ARCH="x86_64" -DCMAKE_BUILD_TYPE=Release -Wno-dev .
    %cmake -Wno-dev .
    make libcef_dll_wrapper
# static build
pushd %{_builddir}/cef_binary_static
    %cmake -DBUILD_SHARED_LIBS:BOOL=OFF -Wno-dev .
    make libcef_dll_wrapper
    cp -f libcef_dll_wrapper/*.a %{_builddir}/cef_binary_%{version}+%{_commit}+chromium-%{_chromiumver}_linux64_minimal/libcef_dll_wrapper/
    popd

%install
mkdir -p %{buildroot}/opt/cef/
mv -f * %{buildroot}/opt/cef/
pushd %{buildroot}/opt/cef/Release/
ln -sf /opt/cef/libcef_dll_wrapper/libcef_dll_wrapper.so  libcef_dll_wrapper.so
ln -sf /opt/cef/libcef_dll_wrapper/libcef_dll_wrapper.a libcef_dll_wrapper.a
popd

%files
/opt/cef/

%changelog

* Sat Apr 18 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 81.2.17-1 
- initial RPM
