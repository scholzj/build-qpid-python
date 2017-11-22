# Define pkgdocdir for releases that don't define it already
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:          qpid-python
Version:       1.37.0
Release:       RC1%{?dist}
Summary:       Libraries for Qpid Python
License:       ASL 2.0
URL:           http://qpid.apache.org

Source0:       qpid-python-%{version}.tar.gz

BuildRequires: python
BuildRequires: python-devel
BuildRequires: python-setuptools


%description

Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.

%package -n python-qpid-common
Summary: Shared code for Qpid Python language bindings

%description -n python-qpid-common
%{summary}.

%files -n python-qpid-common
%doc LICENSE.txt
%doc examples
%{python_sitelib}/mllib
%{python_sitelib}/qpid/*.py*
%{python_sitelib}/qpid/specs



%package -n python-qpid
Summary: Python client library for AMQP written in pure Python

Requires: python-qpid-common = %{version}-%{release}

%description -n python-qpid
%{summary}.

%files -n python-qpid
%doc LICENSE.txt
%{_bindir}/qpid-python-test
%{python_sitelib}/qpid
%if "%{python_version}" >= "2.6"
%{python_sitelib}/qpid_python-*.egg-info
%endif



%prep
%setup -D -q -a 0

%build
pushd qpid-python-%{version}
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
popd

%install
mkdir -p -m0755 %{buildroot}/%{_bindir}
mkdir -p -m0755 %{buildroot}/%{_unitdir}

pushd qpid-python-%{version}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

chmod +x %{buildroot}/%{python_sitelib}/qpid/codec.py
chmod +x %{buildroot}/%{python_sitelib}/qpid/tests/codec.py
chmod +x %{buildroot}/%{python_sitelib}/qpid/reference.py
chmod +x %{buildroot}/%{python_sitelib}/qpid/managementdata.py
chmod +x %{buildroot}/%{python_sitelib}/qpid/disp.py
popd

# clean up items we're not installing
rm -rf %{buildroot}/%{python2_sitearch}/*qpid_tests*
rm -rf %{buildroot}/%{python2_sitelib}/*qpid_tests*


%changelog
* Wed Aug 17 2016 Created based on the C++ spec file
- Separating C++ and Python stuff
