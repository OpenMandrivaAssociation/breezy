%define debug_package %{nil}
# TODO
# split the tools from main package ?
# split the doc ?
%define short_ver %(echo %{version}|cut -d. -f1,2)
Name:           breezy
Epoch:          0
Version:        3.3.5
Release:        1
Summary:        Next-generation distributed version control
Group:          Development/Other
License:        GPLv2+
URL:            http://www.breezy-vcs.org/
Source0:        https://launchpad.net/brz/%{short_ver}/%{version}/+download/%{name}-%{version}.tar.gz
Source1:	https://launchpad.net/brz/%{short_ver}/%{version}/+download/%{name}-%{version}.tar.gz.asc
BuildRequires:  pkgconfig(python)
BuildRequires:	python-setuptools-gettext
BuildRequires:	rust
Provides:	bzr
Obsoletes:	bzr < 3

%description
Bazaar is a distributed revision control system. It allows team members to
branch and merge upstream code very easily.

Distributed revision control systems allow multiple people to have their
own branch of a project, and merge code efficiently between them. This
enables new contributors to immediately have access to the full tools that
previously have been limited to just the committers to a project.

%prep
%setup -q
	
find . -name '*_pyx.c' -exec rm \{\} \;

%check
# run test in /tmp to avoid lock problems with nfs on build cluster
# sadely, it's not enough: bzr tests are trying to rebuild bzr, and
# so must be run in the bzr build dir
# cd /tmp
# $OLDPWD/bzr selftest

# (misc) broken by diff binary test, will investigate later
# still broken with 0.11
# still broken with 0.12
# still broken with 0.13, maybe du to a local server listening , as pycurl test fail
# still broken with 0.15
export TMPDIR=/tmp
#./brz selftest

%build
%py_build
%make_build man1/brz.1

%install
%py_install

find %{buildroot}/%py_platsitedir -name '*.pyc' | xargs rm -f

# install bash completion
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d/
cp contrib/bash/brz %{buildroot}/%{_sysconfdir}/bash_completion.d/

# backwards compatible symbolic links
ln -s brz %{buildroot}%{_bindir}/bzr

%find_lang %{name}

# man pages
install -Dpm644 man1/brz.1 %{buildroot}%{_mandir}/man1/brz.1
install -Dpm644 breezy/git/git-remote-bzr.1 %{buildroot}%{_mandir}/man1/git-remote-bzr.1
echo ".so man1/brz.1" > %{buildroot}%{_mandir}/man1/bzr.1
echo ".so man1/git-remote-bzr.1" > %{buildroot}%{_mandir}/man1/git-remote-brz.1

 
%files -f %{name}.lang
%doc  doc contrib NEWS TODO
%_bindir/brz
%_bindir/bzr
%_bindir/bzr-receive-pack
%_bindir/bzr-upload-pack
%_bindir/git-remote-bzr

%py_platsitedir/%{name}
%py_platsitedir/*.dist-info
%config(noreplace) %{_sysconfdir}/bash_completion.d/brz

%{_mandir}/man1/*

