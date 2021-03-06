LIST_SOURCES        := list
PWD                 := ${CURDIR}
CPLANE_GIT_ROOT     := $(PWD:/tools/packaging/common/rpm=/controller)
PKGING_GIT_ROOT     := $(CPLANE_GIT_ROOT)/../tools
PKGING_DISTDIR      := $(PKGING_GIT_ROOT)/packaging/common/rpm
CPLANE_SRC_VER      := $(shell cat $(CPLANE_GIT_ROOT)/src/base/version.info)
BUILD_BASE          := $(CPLANE_GIT_ROOT)/build/package-build
BUILD_SRC           := $(BUILD_BASE)/SOURCES
PKGBLDDIR           := $(BUILD_BASE)/BUILD
LOCAL_PY_PTH        := $(BUILD_BASE)/BUILD/python2.7
LOCAL_PY            := $(LOCAL_PY_PTH)/bin/python
LOCAL_PY_BLD        := $(BUILD_BASE)/BUILDROOT/Python-2.7.5
LOCAL_PY_DEF        := --define "_python_path $(LOCAL_PY_PTH)"
DISTRO_PACKAGING    := $(CPLANE_GIT_ROOT)/../distro/python-venv-packaging
RPM_PY              := --define "__python $(LOCAL_PY)"
DISTRO              := $(shell egrep -o "Fedora|CentOS|Ubuntu" /etc/issue)
RPMBLDOPTS          := --define '_topdir $(BUILD_BASE)' --define '_builddir $(CPLANE_GIT_ROOT)' -bb
SB_TOP              := $(CPLANE_GIT_ROOT)/..
SB_TOPDIR	    := --define '_sbtop $(SB_TOP)'
PREP = prep
PPREP = pprep

# Skip unit-tests for building packages
export BUILD_ONLY := TRUE

G_TAG :=
ifdef GIT_VER
 G_TAG := --define "_gitVer $(GIT_VER)"
endif 
ifdef TAG
 G_TAG += --define "_buildTag $(TAG)"
endif
ifdef FILE_LIST
 G_TAG += --define "_fileList $(FILE_LIST)"
endif
G_TAG += --define "_srcVer $(CPLANE_SRC_VER)"

ifdef CONTRAIL_SKU
else
  CONTRAIL_SKU := "grizzly"
endif
G_TAG += --define "_skuTag $(CONTRAIL_SKU)"


$(PPREP):
	@echo some $(PPREP) work ...
	mkdir -p $(BUILD_BASE)/{BUILD,RPMS,SOURCES,SPECS,SRPMS,TOOLS}

$(PREP): $(PPREP)
	@echo some $(PREP) work ...
	@echo CPLANE_GIT_ROOT = $(CPLANE_GIT_ROOT)
	mkdir -p $(BUILD_BASE)/{BUILD,RPMS,SOURCES,SPECS,SRPMS,TOOLS}

localpy: $(LOCAL_PY)
$(LOCAL_PY): $(PPREP)
	@echo Compiling python
	if [ ! -d $(PKGBLDDIR)/packaging ]; then mkdir $(PKGBLDDIR)/packaging && \
		cd $(PKGBLDDIR)/packaging && cp -ar $(DISTRO_PACKAGING)/archives .; \
	fi 
	if [ ! -f $(LOCAL_PY) ]; then mkdir  -p $$( dirname $(LOCAL_PY_BLD) ) && \
		tar xjvf $(DISTRO_PACKAGING)/archives/Python-2.7.5.tar.bz2 \
		-C $$( dirname $(LOCAL_PY_BLD) ) && cd $(LOCAL_PY_BLD) && \
		./configure --prefix=$(LOCAL_PY_PTH) && make install &&  \
		$(LOCAL_PY) $(PKGBLDDIR)/packaging/archives/ez_setup.py; \
	fi

contrail: $(PREP)
	@echo making rpm for contrail
	rpmbuild $(RPMBLDOPTS) $(SB_TOP)/tools/packages/rpm/contrail/contrail.spec $(G_TAG) $(SB_TOPDIR)

contrail-api-extension: $(PREP) $(LOCAL_PY)
	@echo making rpm for contrail-api-extension
	rpmbuild $(RPMBLDOPTS) contrail-api-extension.spec $(G_TAG) $(RPM_PY)

contrail-api-lib: $(PREP)
	@echo making rpm for contrail-api-lib
	rpmbuild $(RPMBLDOPTS) contrail-api-lib.spec $(G_TAG)

contrail-nodemgr: $(PREP)
	@echo making rpm for contrail-nodemgr
	rpmbuild $(RPMBLDOPTS) contrail-nodemgr.spec  $(G_TAG)

contrail-interface-name: $(PREP)
	@echo making rpm for contrail-interface-name
	rpmbuild $(RPMBLDOPTS) contrail-interface-name.spec  $(G_TAG)

contrail-libs: $(PREP) $(LOCAL_PY)
	@echo making rpm for contrail-libs
	rpmbuild $(RPMBLDOPTS) contrail-libs.spec $(G_TAG) $(RPM_PY)

contrail-nova-vif: $(PREP) $(LOCAL_PY)
	@echo making rpm for contrail-nova-vif
	rpmbuild $(RPMBLDOPTS) contrail-nova-vif.spec $(G_TAG)

neutron-plugin-contrail: $(PREP) $(LOCAL_PY)
	@echo making rpm for neutron-plugin-plugin
	rpmbuild $(RPMBLDOPTS) neutron-plugin-contrail.spec $(G_TAG)

contrail-setup: $(PREP)
	@echo making rpm for contrail-setup
	rpmbuild $(RPMBLDOPTS) contrail-setup.spec $(G_TAG)

contrail-setup-with-guest: $(PREP)
	@echo making rpm for contrail-setup-with-guest
	rpmbuild $(RPMBLDOPTS) contrail-setup-with-guest.spec $(G_TAG)

# Contrail Cloudstack stuff
contrail-cloudstack-utils: $(PREP)
	@echo making rpm for contrail-cloudstack-utils
	rpmbuild $(RPMBLDOPTS) contrail-cloudstack-utils.spec $(G_TAG)

# Contrail Openstack stuff
ifeq ($(CONTRAIL_SKU), icehouse)
contrail-openstack: $(PREP)
	@echo making rpm for contrail-openstack
	rpmbuild $(RPMBLDOPTS) contrail-openstack-icehouse.spec $(G_TAG)
else
contrail-openstack: $(PREP)
	@echo making rpm for contrail-openstack
	rpmbuild $(RPMBLDOPTS) contrail-openstack.spec $(G_TAG)
endif

contrail-openstack-ha: $(PREP)
	@echo making rpm for contrail-openstack-ha
	rpmbuild $(RPMBLDOPTS) contrail-openstack-ha.spec $(G_TAG)

contrail-openstack-analytics: $(PREP)
	@echo making rpm for contrail-openstack-analytics
	rpmbuild $(RPMBLDOPTS) contrail-openstack-analytics.spec $(G_TAG)

ifeq ($(CONTRAIL_SKU), grizzly)
contrail-openstack-config: $(PREP)
	@echo making rpm for contrail-openstack-config
	rpmbuild $(RPMBLDOPTS) contrail-openstack-config.spec $(G_TAG)
else
contrail-openstack-config: $(PREP)
	@echo making rpm for contrail-openstack-config
	rpmbuild $(RPMBLDOPTS) contrail-openstack-havana-config.spec $(G_TAG)
endif

contrail-openstack-control: $(PREP)
	@echo making rpm for contrail-openstack-control
	rpmbuild $(RPMBLDOPTS) contrail-openstack-control.spec $(G_TAG)

contrail-openstack-database: $(PREP)
	@echo making rpm for contrail-openstack-database
	rpmbuild $(RPMBLDOPTS) contrail-openstack-database.spec $(G_TAG)

contrail-openstack-vrouter: $(PREP)
	@echo making rpm for contrail-openstack-vrouter
	rpmbuild $(RPMBLDOPTS) contrail-openstack-vrouter.spec  $(G_TAG)

contrail-openstack-webui: $(PREP)
	@echo making rpm for contrail-openstack-webui
	rpmbuild $(RPMBLDOPTS) contrail-openstack-webui.spec $(G_TAG)

contrail-openstack-storage: $(PREP) $(LOCAL_PY)
	@echo making rpm for contrail-openstack-storage
	if [ "$(DISTRO)" == "CentOS" ]; then \
		rpmbuild $(RPMBLDOPTS) contrail-openstack-storage.spec $(G_TAG) $(RPM_PY); \
	fi

contrail-openstack-all: contrail-openstack contrail-openstack-analytics contrail-openstack-config \
	contrail-openstack-control contrail-openstack-database contrail-openstack-vrouter \
	contrail-openstack-webui contrail-openstack-storage contrail-openstack-ha

contrail-web-core:
	@echo making rpm for contrail-web-core
	cd $(CPLANE_GIT_ROOT)/../contrail-webui-third-party && python fetch_packages.py
	cd $(CPLANE_GIT_ROOT)/../contrail-web-core && make package REPO=$(CPLANE_GIT_ROOT)/../contrail-web-core
	cp contrail-web-core.spec $(BUILD_BASE)/SPECS/
	cp ../control_files/contrailWebServer.sh $(BUILD_SRC)/
	cp ../control_files/contrailWebMiddleware.sh $(BUILD_SRC)/
	cp ../control_files/contrail-webui-middleware.service $(BUILD_SRC)/
	cp ../control_files/contrail-webui.service $(BUILD_SRC)/
	cp ../control_files/supervisord_webui.conf $(BUILD_SRC)/
	cp ../control_files/supervisor-webui.initd $(BUILD_SRC)/
	cp ../control_files/supervisor-webui.service $(BUILD_SRC)/
	cp ../control_files/contrail-webui.initd.supervisord $(BUILD_SRC)/
	cp ../control_files/contrail-webui-middleware.initd.supervisord $(BUILD_SRC)/
	cp ../control_files/contrail-webui.ini $(BUILD_SRC)/
	cp ../control_files/contrail-webui-middleware.ini $(BUILD_SRC)/
	cp ../control_files/supervisord_wrapper_scripts/contrail-webui.kill $(BUILD_SRC)/
	cp ../control_files/supervisord_wrapper_scripts/contrail-webui-middleware.kill $(BUILD_SRC)/
	cp ../control_files/redis-webui.conf $(BUILD_SRC)/
	cp ../control_files/redis-webui.ini $(BUILD_SRC)/
	cp ../control_files/redis-webui.initd.supervisord $(BUILD_SRC)/
	rpmbuild $(RPMBLDOPTS) $(BUILD_BASE)/SPECS/contrail-web-core.spec $(G_TAG)

contrail-web-controller:
	@echo making rpm for contrail-web-controller
	cd $(CPLANE_GIT_ROOT)/../contrail-web-core && make package REPO=$(CPLANE_GIT_ROOT)/../contrail-web-controller,webController
	cp contrail-web-controller.spec $(BUILD_BASE)/SPECS/
	rpmbuild $(RPMBLDOPTS) $(BUILD_BASE)/SPECS/contrail-web-controller.spec $(G_TAG)

contrail-web-server-manager: $(PREP)
	@echo making rpm for contrail-web-server-manager
	cd $(CPLANE_GIT_ROOT)/../contrail-web-core && make package REPO=$(CPLANE_GIT_ROOT)/../contrail-web-server-manager,serverManager
	cp contrail-web-server-manager.spec $(BUILD_BASE)/SPECS/
	rpmbuild $(RPMBLDOPTS) $(BUILD_BASE)/SPECS/contrail-web-server-manager.spec $(G_TAG)

contrail-install-packages: $(PREP)
	@echo making rpm for contrail-install-packages
	rpmbuild $(RPMBLDOPTS) contrail-install-packages.spec  $(G_TAG)

contrail-database: $(PREP) $(LOCAL_PY)
	@echo making rpm for contrail-database
	cp contrail-database.spec $(BUILD_BASE)/SPECS/
	cp ../control_files/contrail-database.initd $(BUILD_SRC)/
	cp ../control_files/supervisord_database.conf $(BUILD_SRC)/
	cp ../control_files/supervisord_contrail_database.initd $(BUILD_SRC)/
	rpmbuild $(RPMBLDOPTS) $(BUILD_BASE)/SPECS/contrail-database.spec $(G_TAG) $(RPM_PY)

contrail-server-manager: $(PREP) $(LOCAL_PY)
	@echo making rpm for contrail-server-manager
	cp contrail-server-manager.spec $(BUILD_BASE)/SPECS/
	rpmbuild $(RPMBLDOPTS) $(BUILD_BASE)/SPECS/contrail-server-manager.spec $(G_TAG)

contrail-server-manager-client: $(PREP) $(LOCAL_PY)
	@echo making rom for contrail-server-manager-client
	cp contrail-server-manager-client.spec $(BUILD_BASE)/SPECS/
	rpmbuild $(RPMBLDOPTS) $(BUILD_BASE)/SPECS/contrail-server-manager-client.spec $(G_TAG)

contrail-vrouter-init: $(PREP)
	@echo making rpm for contrail-vrouter-init
	rpmbuild $(RPMBLDOPTS) contrail-vrouter-init.spec $(G_TAG)

ifeq ($(CONTRAIL_SKU), grizzly)
NEUTRON_PLUGIN = 
else
NEUTRON_PLUGIN = neutron-plugin-contrail
endif

all: $(PREP) contrail contrail-api-extension \
       contrail-interface-name ifmap-python-client \
       contrail-nodemgr contrail-setup contrail-openstack-all \
       contrail-web-core contrail-web-controller contrail-database \
       ${NEUTRON_PLUGIN} contrail-server-manager contrail-server-manager-client \
       contrail-vrouter-init contrail-web-server-manager

clean:
	@echo clean

