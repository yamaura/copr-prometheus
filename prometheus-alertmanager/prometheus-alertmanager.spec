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
%setup -a 1 -a 2 -n alertmanager-%{version}.linux-amd64

%build

%install
install -d -m 0774 /var/run/prometheus
install -d -m 0744 /var/log/prometheus
install -d -m 0755 /lib/log/prometheus

install -p -Dm 0755 alertmanager %{_bindir}/alertmanager
install -p -Dm 0755 amtool %{_bindir}/amtool
install -p -Dm 0644 alertmanager.yml %{_sysconfdir}/prometheus/alertmanager.yml

install -p -Dm 0644 prometheus-alertmanager.service %{buildroot}%{_unitdir}/prometheus-alertmanager.service
install -p -Dm 0644 prometheus-alertmanager.sysconfig %{_sysconfdir}/sysconfig/alert-manager

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
    -d ${buildroot}/var/lib/prometheus/ -c "Prometheus" prometheus
chgrp prometheus /var/run/prometheus
chmod 774 /var/run/prometheus
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
%config(noreplace) %{_sysconfdir}/prometheus/alertmanager.yaml
/usr/lib/systemd/system/alertmanager.service
%license LICENSE
