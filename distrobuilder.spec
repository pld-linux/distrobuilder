Summary:	System container image builder for LXC and LXD
Name:		distrobuilder
Version:	1.0
Release:	1
License:	Apache v2.0
Group:		Applications/System
Source0:	https://linuxcontainers.org/downloads/distrobuilder/%{name}-%{version}.tar.gz
# Source0-md5:	24e2202ce18dbe16e8f653b39389d1be
URL:		http://linuxcontainers.org/distrobuilder/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires:	rsync
Requires:	squashfs
ExclusiveArch:	%{ix86} %{x8664} %{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		goinstall go install -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x

%description
Distrobuilder builds images based on image definition is a YAML document which describes the source of the image, its package manager, what packages to install/remove for specific image variants, os releases and architectures, as well as additional files to generate and arbitrary actions to execute as part of the image build process.

The output is either a plain root filesystem, a LXD image or a LXC image.

%prep
%setup -q

%build
export GOPATH=$(pwd)/_dist
export GOBIN=$GOPATH/bin

%goinstall ./...

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install _dist/bin/distrobuilder $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md doc/*
%attr(755,root,root) %{_bindir}/%{name}
