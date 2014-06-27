%define debug_package %{nil}
%define product_family Springdale Linux
%define variant_titlecase Server
%define variant_lowercase server
%define release_name Verona
%define base_release_version 7
%define full_release_version 7.0
%define dist_release_version 7
#define beta Beta
%define dist .el%{dist_release_version}

Name:           springdale-release
Version:        %{full_release_version}
Release:        1%{?dist}
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
Provides:       redhat-release = %{version}-%{release}
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{base_release_version}
Source0:        %{name}-%{base_release_version}-1.tar.gz
Source1:        85-display-manager.preset
Source2:        90-default.preset


%description
%{product_family} release files

%prep
%setup -q -n %{name}-%{base_release_version}

%build
echo OK

%install
rm -rf %{buildroot}

# create /etc
mkdir -p %{buildroot}/etc

# create /etc/system-release and /etc/redhat-release
echo "%{product_family} release %{full_release_version}%{?beta: %{beta}} (%{release_name})" > %{buildroot}/etc/springdale-release
ln -s springdale-release %{buildroot}/etc/system-release
ln -s springdale-release %{buildroot}/etc/redhat-release

# create /etc/os-release
cat << EOF >>%{buildroot}/etc/os-release
NAME="%{product_family}"
VERSION="%{full_release_version} (%{release_name})"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID="%{full_release_version}"
PRETTY_NAME="%{product_family} %{full_release_version} (%{release_name})"
ANSI_COLOR="0;32"
CPE_NAME="cpe:/o:springdale:linux:%{full_release_version}:%{?beta:beta}%{!?beta:GA}"
HOME_URL="http://springdale.princeton.edu/"
BUG_REPORT_URL="https://springdale.math.ias.edu/"

REDHAT_BUGZILLA_PRODUCT="%{product_family} %{base_release_version}"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{full_release_version}
REDHAT_SUPPORT_PRODUCT="%{product_family}"
REDHAT_SUPPORT_PRODUCT_VERSION=%{full_release_version}
EOF
# write cpe to /etc/system/release-cpe
echo "cpe:/o:springdale:linux:%{full_release_version}:%{?beta:beta}%{!?beta:GA}" | tr [A-Z] [a-z] > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file %{buildroot}/etc/pki/rpm-gpg
done

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%rhel %{base_release_version}
%%dist %dist
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/springdale-release
install -m 644 EULA %{buildroot}/%{_datadir}/springdale-release
ln -s %{_datadir}/springdale-release %{buildroot}/%{_datadir}/redhat-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/springdale-release
install -m 644 GPL %{buildroot}/%{_docdir}/springdale-release
ln -s %{_docdir}/springdale-release %{buildroot}/%{_docdir}/redhat-release

# copy systemd presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/systemd/system-preset/


%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/springdale-release
/etc/redhat-release
/etc/system-release
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/pki/rpm-gpg/
/etc/rpm/macros.dist
%{_docdir}/springdale-release/*
%{_datadir}/springdale-release/*
%{_docdir}/redhat-release
%{_datadir}/redhat-release
%{_prefix}/lib/systemd/system-preset/*

%changelog
* Wed Jun 25 2014 Josko Plazonic <plazonic@math.princeton.edu> - 7.0-1.sdl7
- springdale version

* Tue Apr  1 2014 Daniel Mach <dmach@redhat.com> - 7.0-1.el7
- Rebuild for GA

* Tue Feb 25 2014 Daniel Mach <dmach@redhat.com> - 7.0-0.12.el7
- Fix variant_titlecase macro usage

* Wed Feb 19 2014 Daniel Mach <dmach@redhat.com> - 7.0-0.11.el7
- Enable microcode.service by default

* Tue Feb 18 2014 Daniel Mach <dmach@redhat.com> - 7.0-0.10.el7
- Update EULA text

* Wed Feb 12 2014 Daniel Mach <dmach@redhat.com> - 7.0-0.9.el7
- Add systemd presets
- Resolves: #903690

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 7.0-0.8.el7
- Mass rebuild 2014-01-24

* Wed Jan 15 2014 Daniel Mach <dmach@redhat.com> - 7.0-0.7
- Add ID_LIKE, HOME_URL and BUG_REPORT_URL fields to /etc/os-release
- Make /etc/os-release a config file

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 7.0-0.6
- Mass rebuild 2013-12-27

* Fri Nov  8 2013 Daniel Mach <dmach@redhat.com> - 7.0-0.5
- Rebuild for Beta
