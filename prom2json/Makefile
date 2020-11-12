.PHONY:all srpm

all: srpm

srpm:
	dnf install -y rpmdevtools
	spectool -g -R. ./prom2json.spec
	rpmbuild -bs prom2json.spec --define "_sourcedir $(PWD)" --define "_srcrpmdir $(outdir)"
