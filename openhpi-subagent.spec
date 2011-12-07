Name:           openhpi-subagent
Version:        2.3.4
Release:        10%{?dist}
Summary:        NetSNMP subagent for OpenHPI

Group:          System Environment/Base
License:        BSD
URL:            http://www.openhpi.org
Source0:        http://downloads.sourceforge.net/openhpi/%{name}-%{version}.tar.gz
Source1:        %{name}.initd
Source2:        %{name}.sysconfig
# https://sourceforge.net/tracker/?func=detail&aid=2849869&group_id=71730&atid=532251
Patch1:         %{name}-2.3.4-format.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openhpi-devel >= 2.10, net-snmp-devel, openssl-devel
BuildRequires:  docbook-utils
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

%description
The openhpi-subagent package contains the Service Availability Forum's
Hardware Platform Interface SNMP sub-agent.

%prep
%setup -q
%patch1 -p1 -b .format


%build
%configure
make %{?_smp_mflags}
make -C docs subagent-manual/book1.html


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{name}
mkdir -p $RPM_BUILD_ROOT%{_initddir}
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initddir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1
fi
            

%files
%defattr(-,root,root,-)
%doc COPYING README docs/subagent-manual
%{_initddir}/%{name}
%config(noreplace) %{_sysconfdir}/snmp/*.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/hpiSubagent
%{_datadir}/snmp/mibs/*.mib

%changelog
* Tue Mar  9 2010 Dan Horák <dhorak@redhat.com> - 2.3.4-10
- switched to new initscript
- Related: #543948

* Tue Jan 12 2010 Dan Horák <dhorak@redhat.com> - 2.3.4-9
- added patch for net-snmp 5.5
- Related: #543948

* Tue Jan 12 2010 Dan Horák <dhorak@redhat.com> - 2.3.4-8
- rebuild with net-snmp 5.5
- Related: #543948

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.3.4-7
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2.3.4-4
- rebuild with new openssl

* Fri Nov 21 2008 Dan Horak <dan[at]danny.cz> - 2.3.4-3
- fix Source0 URL

* Fri Apr 25 2008 Dan Horak <dan[at]danny.cz> - 2.3.4-2
- initscript is not a config file
- added missing R(postun)
- update the initd script

* Thu Apr 17 2008 Dan Horak <dan[at]danny.cz> - 2.3.4-1
- initial version 2.3.4
