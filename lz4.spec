Summary:	Extremely Fast Compression algorithm
Name:		lz4
Version:	r104
Release:	4
License:	GPL v2 (cli), BSD (libs)
Group:		Applications
# svn checkout http://lz4.googlecode.com/svn/trunk/ lz4-rNUM
# tar --exclude-vcs -cvzf lz4-rNUM.tar.gz lz4-rNUM/
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	8a46dfcc102dce9c5fb94309c08a1718
Patch0:		%{name}-build.patch
URL:		http://fastcompression.blogspot.com/p/lz4.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LZ4 is a very fast lossless compression algorithm, providing
compression speed at 400 MB/s per core, scalable with multi-cores CPU.
It also features an extremely fast decoder, with speed in multiple
GB/s per core, typically reaching RAM speed limits on multi-core
systems.

%package devel
Summary:	Header files for lz4 library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for lz4 library.

%prep
%setup -q
%patch0 -p1

%{__sed} -i "s/-O3/%{rpmcflags} %{rpmldflags}/g" Makefile

%build
cd cmake
%cmake
%{__make}
cd ..
%{__make} lz4

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C cmake install \
	DESTDIR=$RPM_BUILD_ROOT

install -D cmake/lz4c?? $RPM_BUILD_ROOT%{_bindir}/lz4c

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc lz4_format_description.txt
%attr(755,root,root) %{_bindir}/lz4c
%attr(755,root,root) %{_libdir}/liblz4.so.0.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblz4.so
%{_includedir}/*.h

