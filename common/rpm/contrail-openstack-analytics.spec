%define         _contrailetc /etc/contrail
%define         _contrailanalytics /opt/contrail/analytics
%define         _contrailutils /opt/contrail/utils
%define         _supervisordir /etc/contrail/supervisord_analytics_files
%define         _distropkgdir tools/packaging/common/control_files

%if 0%{?_buildTag:1}
%define         _relstr      %{_buildTag}
%else
%define         _relstr      %(date -u +%y%m%d%H%M)
%endif
%{echo: "Building release %{_relstr}\n"}
%if 0%{?_srcVer:1}
%define         _verstr      %{_srcVer}
%else
%define         _verstr      1
%endif
Release:	    %{_relstr}%{?dist}
Summary: Contrail Openstack Analytics %{?_gitVer}
Name: contrail-openstack-analytics
Version:	    %{_verstr}
Group:              Applications/System
License:            Commercial
URL:                http://www.juniper.net/
Vendor:             Juniper Networks Inc

BuildArch: noarch

Requires: contrail-analytics >= %{_verstr}-%{_relstr}
Requires: contrail-setup >= %{_verstr}-%{_relstr}
Requires: contrail-utils >= %{_verstr}-%{_relstr}
Requires: contrail-nodemgr >= %{_verstr}-%{_relstr}
Requires: python-contrail >= %{_verstr}-%{_relstr}
%if 0%{?rhel} <= 6
Requires: python-importlib
%endif

%description
Contrail Package Requirements for Analytics

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_contrailetc}
install -d -m 755 %{buildroot}%{_contrailanalytics}
install -d -m 755 %{buildroot}%{_supervisordir}
install -d -m 755 %{buildroot}%{_initddir}

#install wrapper scripts for supervisord
pushd %{_builddir}/..
install -p -m 755 %{_distropkgdir}/contrail-analytics.rules %{buildroot}%{_supervisordir}/contrail-analytics.rules

#install .ini files for supervisord
install -p -m 755 %{_distropkgdir}/supervisord_analytics.conf %{buildroot}%{_contrailetc}/supervisord_analytics.conf
install -p -m 755 %{_distropkgdir}/contrail-collector.ini %{buildroot}%{_supervisordir}/contrail-collector.ini
install -p -m 755 %{_distropkgdir}/contrail-analytics-api.ini %{buildroot}%{_supervisordir}/contrail-analytics-api.ini
install -p -m 755 %{_distropkgdir}/contrail-query-engine.ini %{buildroot}%{_supervisordir}/contrail-query-engine.ini

%if 0%{?rhel}
install -p -m 755 %{_distropkgdir}/supervisor-analytics.initd          %{buildroot}%{_initddir}/supervisor-analytics
%endif
install -p -m 755 %{_distropkgdir}/contrail-collector.initd.supervisord          %{buildroot}%{_initddir}/contrail-collector
install -p -m 755 %{_distropkgdir}/contrail-qe.initd.supervisord          %{buildroot}%{_initddir}/contrail-query-engine
install -p -m 755 %{_distropkgdir}/contrail-opserver.initd.supervisord          %{buildroot}%{_initddir}/contrail-analytics-api


for f in $(find %{buildroot} -type f -exec grep -l '^#!%{__python}' {} \; ); do
    sed 's/^#!.*python/#!\/usr\/bin\/python/g' $f > ${f}.b
    mv ${f}.b ${f}
done

%post

%files
%defattr(-, root, root)
%config(noreplace) %{_supervisordir}/contrail-collector.ini
%config(noreplace) %{_supervisordir}/contrail-analytics-api.ini
%config(noreplace) %{_supervisordir}/contrail-query-engine.ini
%{_supervisordir}/contrail-analytics.rules
%if 0%{?rhel}
%{_initddir}/supervisor-analytics
%endif
%{_initddir}/contrail-collector
%{_initddir}/contrail-query-engine
%{_initddir}/contrail-analytics-api
%config(noreplace) %{_contrailetc}/supervisord_analytics.conf

%changelog
* Tue Aug  6 2013 <ndramesh@juniper.net>
* Initial build.

