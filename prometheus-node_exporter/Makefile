.PHONY:all srpm

all: srpm

srpm:
	dnf install -y rpmdevtools
	spectool -g -R. ./prometheus-node_exporter.spec
	rpmbuild -bs prometheus-node_exporter.spec --define "_sourcedir $(PWD)" --define "_srcrpmdir $(outdir)"
