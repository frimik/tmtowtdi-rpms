%define logmsg logger -t %{name}/rpm

%define __os_install_post /usr/lib/rpm/brp-compress

Name:           jsvc
Version:        1.0.12
Release:        1%{?dist}
Summary:        Apache Commons Daemon
Vendor:         Fulhack Industries

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://commons.apache.org/daemon/jsvc.html
Source0:        http://apache.mirrors.spacedump.net/commons/daemon/source/commons-daemon-%{version}-src.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  jdk, docbook2x, ant
Requires:       jdk

%description
Jsvc is a set of libraries and applications for making Java
applications run on UNIX more easily.
Jsvc allows the application (e.g. Tomcat) to perform some privileged
operations as root (e.g. bind to a port < 1024), and then switch
identity to a non-privileged user. 

%prep
%setup -q -n commons-daemon-%{version}-src

%build
ant

cd $RPM_BUILD_DIR/commons-daemon-%{version}-src/src/native/unix
%ifarch x86_64
export CFLAGS=-m64
export LDFLAGS=-m64
%endif
%configure --with-java=/usr/java/default
make %{?_smp_mflags}

cd $RPM_BUILD_DIR/commons-daemon-%{version}-src/src/native/unix/man
db2x_docbook2man jsvc.1.xml
gzip JSVC.1


%install
rm -rf "${RPM_BUILD_ROOT}"
%{__install} -D -m0755 src/native/unix/jsvc ${RPM_BUILD_ROOT}%{_bindir}/jsvc
%{__install} -D -m0644 src/native/unix/man/JSVC.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/jsvc.1.gz
%{__install} -D -m0644 dist/commons-daemon-%{version}.jar ${RPM_BUILD_ROOT}/opt/jsvc/commons-daemon-%{version}.jar
ln -s commons-daemon-%{version}.jar ${RPM_BUILD_ROOT}/opt/jsvc/commons-daemon.jar

%clean
rm -rf "${RPM_BUILD_ROOT}"

%files
%defattr(-,root,root,-)
%doc README dist/LICENSE.txt dist/RELEASE-NOTES.txt
%{_bindir}/jsvc
/opt/jsvc
%{_mandir}/man1/*

%changelog
* Fri Feb 8 2013 Mikael Fridh <frimik@gmail.com> - 1.0.12-1
- New upstream version 1.0.12

* Wed Nov 28 2012 Mikael Fridh <frimik@gmail.com> - 1.0.11-1
- New upstream version 1.0.11

* Mon Jul 18 2011 Mikael Fridh <frimik@gmail.com> - 1.0.5-2
- export FLAGS for 64-bit build

* Wed Jul 06 2011 Mikael Fridh <frimik@gmail.com> - 1.0.5-1
- initial package
