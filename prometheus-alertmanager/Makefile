.PHONY:all srpm

all: srpm

srpm:
	dnf install -y rpmdevtools
	spectool -g ./prometheus-alertmanager.spec
	rpmbuild -bs prometheus-alertmanager.spec --define "_sourcedir $(PWD)" --define "_srcrpmdir $(outdir)"
