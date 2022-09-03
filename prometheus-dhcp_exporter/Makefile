.PHONY:all srpm

all: srpm

srpm:
	dnf install -y rpmdevtools
	spectool -g ./prometheus-dhcp_exporter.spec
	rpmbuild -bs prometheus-dhcp_exporter.spec --define "_sourcedir $(PWD)" --define "_srcrpmdir $(outdir)"
