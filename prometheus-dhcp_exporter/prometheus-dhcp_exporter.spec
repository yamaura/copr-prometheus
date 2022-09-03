%define debug_package %{nil}
%define _build_id_links none

%global commit 228c4923a8e70a7845bf08da609caff082316934
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:             prometheus-dhcp_exporter
Version:          0.1.0_1_g228c492
Release:          2%{?dist}
Summary:          Prometheus DHCP Exporter
License:          MIT License
URL:              https://github.com/MindFlavor/prometheus_dhcp_exporter
Source0:          https://github.com/MindFlavor/prometheus_dhcp_exporter/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:          prometheus-dhcp_exporter.service
Source2:          prometheus-dhcp_exporter.sysconfig
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires:         dhcpd-pools
BuildRequires:    cargo

%description
%{summary}

%prep
%autosetup -n prometheus_dhcp_exporter-%{commit}

%build
cargo build --release

%install
install -d -p %{buildroot}%{_sysconfdir}/sysconfig \

install -p -Dm 0755 target/release/prometheus_dhcp_exporter %{buildroot}%{_sbindir}/prometheus-dhcp_exporter

install -p -Dm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/prometheus-dhcp_exporter.service
install -p -Dm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/prometheus-dhcp_exporter

%pre

%post
%systemd_post prometheus-dhcp_exporter.service

%preun
%systemd_preun prometheus-dhcp_exporter.service

%postun
%systemd_postun prometheus-dhcp_exporter.service

%files
%defattr(-,root,root,-)
/usr/sbin/prometheus-dhcp_exporter
%config(noreplace) /etc/sysconfig/prometheus-dhcp_exporter
/usr/lib/systemd/system/prometheus-dhcp_exporter.service
%license LICENSE
