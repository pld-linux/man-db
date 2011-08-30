Summary:	Tools for searching and reading man pages
Name:		man-db
Version:	2.6.0.2
Release:	0.1
# project man-db  GPLv2+
# Gnulib part     GPLv3+
License:	GPL v2+ and GPL v3+
Group:		Base
URL:		http://www.nongnu.org/man-db/
Source0:	http://download.savannah.gnu.org/releases/man-db/%{name}-%{version}.tar.gz
# Source0-md5:	2b41c96efec032d2b74ccbf2e401f93e
Source1:	%{name}.daily
Source2:	%{name}.sysconfig
# Resolves: #655385 - use old format of nroff output
Patch1:		sgr.patch
BuildRequires:	gdbm-devel
BuildRequires:	gettext
BuildRequires:	groff
BuildRequires:	less
BuildRequires:	libpipeline-devel
BuildRequires:	zlib-devel
Requires:	coreutils
Requires:	crontabs
Requires:	grep
Requires:	groff
Requires:	gzip
Requires:	less
Provides:	man = %{version}
Provides:	man-pages-reader = %{version}
Obsoletes:	man < 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cache	/var/cache/man

%description
The man-db package includes five tools for browsing man-pages: man,
whatis, apropos, manpath and lexgrog. man preformats and displays
manual pages. whatis searches the manual page names. apropos searches
the manual page names and descriptions. manpath determines search path
for manual pages. lexgrog directly reads header information in manual
pages.

%prep
%setup -q
%patch1 -p1

%build
%configure\
	--with-sections="1 1p 8 2 3 3p 4 5 6 7 9 0p n l p o 1x 2x 3x 4x 5x 6x 7x 8x" \
	--disable-setuid \
	--with-browser=elinks

%{__make} \
	V=1 \
	CC="%{__cc} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL='install -p' \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

# move the documentation to relevant place
mv $RPM_BUILD_ROOT%{_datadir}/doc/man-db/* ./

# remove zsoelim - part of groff package
rm $RPM_BUILD_ROOT%{_bindir}/zsoelim
rm $RPM_BUILD_ROOT%{_mandir}/man1/zsoelim.1

# remove pages which are also in  man-pages-de
rm $RPM_BUILD_ROOT%{_mandir}/de/man1/zsoelim.1
rm $RPM_BUILD_ROOT%{_mandir}/de/man1/manpath.1
rm $RPM_BUILD_ROOT%{_mandir}/de/man5/manpath.5
rm $RPM_BUILD_ROOT%{_mandir}/de/man8/catman.8
rm $RPM_BUILD_ROOT%{_mandir}/de/man8/mandb.8

# remove libtool archives
rm $RPM_BUILD_ROOT%{_libdir}/man-db/*.la

# install cache directory
install -d $RPM_BUILD_ROOT%{cache}

# install cron script for man-db creation/update
install -D -p %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/man-db.cron

# config for cron script
install -D -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/man-db

%find_lang %{name}
%find_lang %{name}-gnulib
cat %{name}-gnulib.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README man-db-manual.txt man-db-manual.ps docs/COPYING ChangeLog NEWS
%config(noreplace) %{_sysconfdir}/man_db.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/man-db
/etc/cron.daily/man-db.cron
%attr(755,root,root) %{_sbindir}/accessdb
%attr(755,root,root) %{_bindir}/man
%attr(755,root,root) %{_bindir}/whatis
%attr(755,root,root) %{_bindir}/apropos
%attr(755,root,root) %{_bindir}/manpath
%attr(755,root,root) %{_bindir}/lexgrog
%attr(755,root,root) %{_bindir}/catman
%attr(755,root,root) %{_bindir}/mandb
%dir %{_libdir}/man-db
%{_libdir}/man-db/*.so
%{_libdir}/man-db/globbing
%{_libdir}/man-db/manconv
%dir %{cache}
# documentation and translation
%{_mandir}/man1/apropos.1*
%{_mandir}/man1/lexgrog.1*
%{_mandir}/man1/man.1*
%{_mandir}/man1/manconv.1*
%{_mandir}/man1/manpath.1*
%{_mandir}/man1/whatis.1*
%{_mandir}/man5/manpath.5*
%{_mandir}/man8/accessdb.8*
%{_mandir}/man8/catman.8*
%{_mandir}/man8/mandb.8*
%lang(de) %{_mandir}/de/man*/*
%lang(es) %{_mandir}/es/man*/*
%lang(fr) %{_mandir}/fr/man*/*
%lang(id) %{_mandir}/id/man*/*
%lang(it) %{_mandir}/it/man*/*
%lang(ja) %{_mandir}/ja/man*/*
%lang(nl) %{_mandir}/nl/man*/*
%lang(pl) %{_mandir}/pl/man*/*
%lang(ru) %{_mandir}/ru/man*/*
