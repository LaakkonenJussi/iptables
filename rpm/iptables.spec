Name:       iptables
Summary:    Tools for managing Linux kernel packet filtering capabilities
Version:    1.8.2
Release:    1
Group:      System/Base
License:    GPLv2
URL:        http://www.netfilter.org/
Source0:    http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
Source1:    iptables-config
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  kernel-headers
BuildRequires:  autoconf, automake, libtool

%description
The iptables utility controls the network packet filtering code in the
Linux kernel. If you need to set up firewalls and/or IP masquerading,
you should install this package.


%package devel
Summary:    Development package for iptables
Group:      System/Base
Requires:   %{name} = %{version}-%{release}

%description devel
iptables development headers and libraries.

The iptc interface is upstream marked as not public. The interface is not 
stable and may change with every new version. It is therefore unsupported.


%package ipv6
Summary:    IPv6 support for iptables
Group:      System/Base
Requires:   %{name} = %{version}-%{release}

%description ipv6
The iptables package contains IPv6 (the next version of the IP
protocol) support for iptables. Iptables controls the Linux kernel
network packet filtering code, allowing you to set up firewalls and IP
masquerading. 

Install iptables-ipv6 if you need to set up firewalling for your
network and you are using ipv6.


%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.


%prep
%setup -q -n %{name}-%{version}/%{name}

%build
./autogen.sh
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" ./configure --enable-devel --prefix=%{_prefix} --bindir=/bin --sbindir=/sbin --with-kernel=/usr --with-kbuild=/usr --with-ksource=/usr --disable-nftables --libdir=%{_libdir} --with-xtlibdir=%{_libdir}/xtables
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

# remove la file(s)
rm -f %{buildroot}/%{_lib}/*.la

# install ip*tables.h header files
install -m 644 include/ip*tables.h %{buildroot}%{_includedir}/
install -d -m 755 %{buildroot}%{_includedir}/iptables
install -m 644 include/iptables/internal.h %{buildroot}%{_includedir}/iptables/

# install ipulog header file
install -d -m 755 %{buildroot}%{_includedir}/libipulog/
install -m 644 include/libipulog/*.h %{buildroot}%{_includedir}/libipulog/

# install init scripts and configuration files
install -d -m 755 %{buildroot}/etc/sysconfig
install -c -m 755 %{SOURCE1} %{buildroot}/etc/sysconfig/iptables-config
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE1} > ip6tables-config
install -c -m 755 ip6tables-config %{buildroot}/etc/sysconfig/ip6tables-config

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} INCOMPATIBILITIES


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%config %attr(0600,root,root) /etc/sysconfig/iptables-config
/sbin/iptables*
/sbin/xtables-legacy-multi
/bin/iptables-xml
%dir %{_libdir}/xtables
%{_libdir}/xtables/libipt*
%{_libdir}/xtables/libxt*
%{_libdir}/libip*tc.so.*
%{_libdir}/libxtables.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/iptables
%{_includedir}/iptables/*.h
%{_includedir}/*.h
%dir %{_includedir}/libiptc
%{_includedir}/libiptc/*.h
%dir %{_includedir}/libipulog
%{_includedir}/libipulog/*.h
%{_libdir}/libip*tc.so
%{_libdir}/libxtables.so
%{_libdir}/pkgconfig/libiptc.pc
%{_libdir}/pkgconfig/libip4tc.pc
%{_libdir}/pkgconfig/libip6tc.pc
%{_libdir}/pkgconfig/xtables.pc

%files ipv6
%defattr(-,root,root,-)
%config %attr(0600,root,root) /etc/sysconfig/ip6tables-config
/sbin/ip6tables*
%{_libdir}/xtables/libip6t*

%files doc
%defattr(-,root,root,-)
%{_mandir}/man*/%{name}*
%{_mandir}/man8/ip6tables*
%{_mandir}/man8/xtables-legacy.*
%exclude %{_mandir}/man8/xtables-monitor.*
%exclude %{_mandir}/man8/xtables-nft.*
%exclude %{_mandir}/man8/xtables-translate.*
%{_docdir}/%{name}-%{version}
