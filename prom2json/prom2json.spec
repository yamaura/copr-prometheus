%define debug_package %{nil}

Name:             prom2json
Version:          1.3.0
Release:          1%{?dist}
Summary:          A tool to scrape a Prometheus client and dump the result as JSON.
License:          Apache License Version 2.0
URL:              https://github.com/prometheus/prom2json
Source0:          https://github.com/prometheus/prom2json/releases/download/v%{version}/prom2json-%{version}.linux-amd64.tar.gz

%description
%{summary}

%prep
ls
%setup -n prom2json-%{version}.linux-amd64

%build

%install
install -p -Dm 0755 prom2json %{buildroot}%{_bindir}/prom2json

%pre

%post

%preun

%postun

%files
%defattr(-,root,root,-)
/usr/bin/prom2json
%license LICENSE
