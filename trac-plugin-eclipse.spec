# TODO
# - how to package eclipse ext?

%define		subver	r3719
%define		rel		0.1
Summary:	Eclipse Trac Integration
Name:		trac-plugin-eclipse
Version:	0.1
Release:	0.%{subver}.%{rel}
License:	BSD-like
Group:		Applications/WWW
Source0:	trac-plugin-tracrpcext-r3719.tar.bz2
# Source0-md5:	8fb5e84a2fede6710aa082c95810e151
Source1:	http://trac-hacks.org/attachment/wiki/EclipseTracPlugin/EclipseTrac.zip?format=raw
# Source1-md5:	ab5c9b5d196272a261cd2d799702847d
URL:		http://trac-hacks.org/wiki/EclipseTracPlugin
BuildRequires:	python-devel
BuildRequires:	python-setuptools >= 0.6
Requires:	python-ldap
Requires:	trac >= 0.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_eclipsedir		%{_prefix}/lib/eclipse

%description
This is a plugin that provides a complete Trac interface usable from
the Eclipse environment.

%package -n eclipse-plugin-trac
Summary:	Eclipse plugin for trac
Group:		Development/Languages

%description -n eclipse-plugin-trac
Eclipse Trac Integration

%prep
%setup -qc -a1
mv trac-plugin-tracrpcext-%{subver} tracrpcext

%build
cd tracrpcext
%{__python} setup.py build
%{__python} setup.py egg_info
cd ..

%install
rm -rf $RPM_BUILD_ROOT
cd tracrpcext
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT
cd ..

install -d $RPM_BUILD_ROOT%{_eclipsedir}/plugins
cp -a features plugins web index.html site.xml $RPM_BUILD_ROOT%{_eclipsedir}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	Don't forget to enable both the TracRpcExt-Plugin and the XmlRpcPlugin:

	[components]
	tracrpc.* = enabled
	tracrpcext.* = enabled
	EOF
#'
fi

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/TracExtendedXmlRpc-*.egg-info
%dir %{py_sitescriptdir}/tracrpcext
%{py_sitescriptdir}/tracrpcext/*.py[co]

%files -n eclipse-plugin-trac
%defattr(644,root,root,755)
%{_eclipsedir}/features/EclipseTrac_*.jar
%{_eclipsedir}/plugins/mm.eclipse.trac_*.jar
%{_eclipsedir}/plugins/org.apache.xmlrpc_*.jar
%{_eclipsedir}/index.html
%{_eclipsedir}/site.xml
%{_eclipsedir}/web
