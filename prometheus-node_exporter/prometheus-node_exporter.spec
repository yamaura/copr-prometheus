%define debug_package %{nil}

Name:             prometheus-node_exporter
Version:          0.18.1
Release:          1%{?dist}
Summary:          Prometheus NodeExporter
License:          Apache License Version 2.0
URL:              https://prometheus.io/
Source0:          https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-amd64.tar.gz
Source1:          prometheus-node_exporter.service
Source2:          prometheus-node_exporter.sysconfig
Requires(pre):    /usr/sbin/useradd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
%{summary}

%prep
ls
%setup -n node_exporter-%{version}.linux-amd64

%build

%install
install -d -p %{buildroot}%{_sysconfdir}/sysconfig \
              %{buildroot}%{_sysconfdir}/prometheus/node_exporter/text_collectors

install -p -Dm 0755 node_exporter %{buildroot}%{_bindir}/node_exporter

install -p -Dm 0644 %{_sourcedir}/prometheus-node_exporter.service %{buildroot}%{_unitdir}/prometheus-node_exporter.service
install -p -Dm 0644 %{_sourcedir}/prometheus-node_exporter.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/prometheus-node_exporter

%pre
getent group node_exporter >/dev/null || groupadd -r node_exporter
getent passwd node_exporter >/dev/null || \
  useradd -r -g node_exporter -s /sbin/nologin \
    -d ${buildroot}/var/lib/node_exporter/ -c "Prometheus node exporter" node_exporter
mkdir -p /var/lib/node_exporter/textfile_collector
chgrp node_exporter /var/lib/node_exporter/textfile_collector
chmod 771 /var/lib/node_exporter/textfile_collector

%post
%systemd_post prometheus-node_exporter.service

%preun
%systemd_preun prometheus-node_exporter.service

%postun
%systemd_postun prometheus-node_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/node_exporter
%config(noreplace) /etc/sysconfig/prometheus-node_exporter
/usr/lib/systemd/system/prometheus-node_exporter.service
%license LICENSE
