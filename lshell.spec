Summary:	Limited Shell (lshell)
Summary(pl.UTF-8):	Limitowana Powłoka (lshell)
Name:		lshell
Version:	0.9.10
Release:	1
License:	GPL v3
Group:		Applications/Shells
Source0:	http://downloads.sourceforge.net/lshell/%{name}-%{version}.tar.gz
# Source0-md5:	af9c86e1be9d61adaa175988604cbeae
URL:		http://lshell.ghantoos.org
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.462
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lshell is a configurable limited shell coded in Python, that lets you
restrict users to limited sets of commands, choose to enable/disable
any command over SSH (e.g. SCP, SFTP, rsync, etc.), log user's
commands, implement timing restriction, and more.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p <lua>
%lua_add_etc_shells %{_bindir}/lshell
os.execute("/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1")

%preun	-p <lua>
if arg[2] == 0 then
	%lua_remove_etc_shells %{_bindir}/lshell
end

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc CHANGES README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lshell.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/lshell
%attr(755,root,root) %{_bindir}/lshell
%{_mandir}/man1/lshell.1*
%{py_sitescriptdir}/lshell.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{name}-*.egg-info
%endif
