%define debug_package %{nil}

Name:             prometheus-alertmanager
Version:          0.19.0
Release:          1%{?dist}
Summary:          Prometheus Alertmanager
License:          Apache License Version 2.0
URL:              https://prometheus.io/
Source0:          https://github.com/prometheus/alertmanager/releases/download/v%{version}/alertmanager-%{version}.linux-amd64.tar.gz
Source1:          prometheus-alertmanager.service
Source2:          prometheus-alertmanager.sysconfig
Requires(pre):    /usr/sbin/useradd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
%{summary}

%prep
ls
%setup -n alertmanager-%{version}.linux-amd64

%build

%install
install -d -m 0774 %{buildroot}/var/run/prometheus
install -d -m 0744 %{buildroot}/var/log/prometheus
install -d -m 0755 %{buildroot}/lib/log/prometheus

install -p -Dm 0755 alertmanager %{buildroot}%{_bindir}/alertmanager
install -p -Dm 0755 amtool %{buildroot}%{_bindir}/amtool
install -p -Dm 0644 alertmanager.yml %{buildroot}%{_sysconfdir}/prometheus/alertmanager.yml

install -p -Dm 0644 %{_sourcedir}/prometheus-alertmanager.service %{buildroot}%{_unitdir}/prometheus-alertmanager.service
install -p -Dm 0644 %{_sourcedir}/prometheus-alertmanager.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/prometheus-alertmanager

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
    -d ${buildroot}/var/lib/prometheus/ -c "Prometheus" prometheus
chgrp prometheus /var/run/prometheus
mkdir -p /var/run/prometheus
chmod 774 /var/run/prometheus
mkdir -p /var/log/prometheus
chown prometheus:prometheus /var/log/prometheus
chmod 744 /var/log/prometheus

%post
%systemd_post prometheus-alertmanager.service

%preun
%systemd_preun prometheus-alertmanager.service

%postun
%systemd_postun prometheus-alertmanager.service

%files
%defattr(-,root,root,-)
/usr/bin/alertmanager
/usr/bin/amtool
%config(noreplace) %{_sysconfdir}/prometheus/alertmanager.yml
%config(noreplace) /etc/sysconfig/prometheus-alertmanager
/usr/lib/systemd/system/prometheus-alertmanager.service
%license LICENSE
