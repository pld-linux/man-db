# TODO: use man cache owner?
#
# Conditional build:
%bcond_without	tests	# "make check" call
#
Summary:	Tools for searching and reading man pages
Summary(pl.UTF-8):	Narzędzia do przeszukiwania i czytania stron podręcznika man
Name:		man-db
Version:	2.13.1
Release:	1
# project man-db  GPLv2+
# Gnulib part     GPLv3+
License:	GPL v2+ and GPL v3+
Group:		Base
Source0:	http://download.savannah.gnu.org/releases/man-db/%{name}-%{version}.tar.xz
# Source0-md5:	b6335533cbeac3b24cd7be31fdee8c83
Source1:	%{name}.daily
Source2:	%{name}.sysconfig
# Resolves: #655385 - use old format of nroff output
Patch0:		sgr.patch
# recent nroff uses times()
Patch1:		%{name}-sandbox.patch
URL:		https://man-db.gitlab.io/man-db/
BuildRequires:	gdbm-devel
BuildRequires:	gettext-tools >= 0.18.3
BuildRequires:	groff >= 1:1.21
BuildRequires:	less
BuildRequires:	libpipeline-devel >= 1.5.0
BuildRequires:	libseccomp-devel
BuildRequires:	pkgconfig
BuildRequires:	po4a >= 0.41
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	coreutils
Requires:	grep
Requires:	groff >= 1:1.21
Requires:	gzip
Requires:	less
Requires:	libpipeline >= 1.5.0
Suggests:	cronjobs
Suggests:	zstd
Provides:	man-pages-reader = %{version}
Obsoletes:	man < 1.7
Obsoletes:	man-config < 1.7
Obsoletes:	man-whatis < 1.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pkgcachedir	/var/cache/man

%description
The man-db package includes five tools for browsing man-pages: man,
whatis, apropos, manpath and lexgrog:
- man preformats and displays manual pages.
- whatis searches the manual page names.
- apropos searches the manual page names and descriptions.
- manpath determines search path for manual pages.
- lexgrog directly reads header information in manual pages.

%description -l pl.UTF-8
Pakiet man-db zawiera pięć narzędzi do przeglądania stron podręcznika
man (nazywanych man-pages): man, whatis, apropos, manpath i lexgrog:
- man wstępnie formatuje i wyświetla strony podręcznika.
- whatis przeszukuje nazwy stron podręcznika.
- apropos przeszukuje nazwy stron podręcznika oraz opisy.
- manpath określa ścieżkę przeszukiwania dla stron podręcznika.
- lexgrog bezpośrednio odczytuje informacje z nagłówka stron
  podręcznika.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%configure \
	--disable-cache-owner \
	--disable-setuid \
	--disable-silent-rules \
	--with-browser=elinks \
	--with-sections="1 1p 8 2 3 3p 4 5 6 7 9 0p n l p o 1x 2x 3x 4x 5x 6x 7x 8x" \
	--with-systemdtmpfilesdir=%{systemdtmpfilesdir} \
	--with-zstd=/usr/bin/zstd

%{__make} \
	CC="%{__cc} %{rpmcflags} %{rpmcppflags}"

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL='install -p' \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

# move the documentation to relevant place
%{__mv} $RPM_BUILD_ROOT%{_docdir}/man-db/* ./

# remove libtool archives
%{__rm} $RPM_BUILD_ROOT%{_libdir}/man-db/*.la

# install cache directory
install -d $RPM_BUILD_ROOT%{pkgcachedir}

# install cron script for man-db creation/update
install -D -p %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/man-db.cron

# config for cron script
install -D -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/man-db

cat <<EOF > $RPM_BUILD_ROOT%{systemdtmpfilesdir}/man-db.conf
d %{pkgcachedir} 2755 root root 1w
EOF

%find_lang %{name}
%find_lang %{name}-gnulib
cat %{name}-gnulib.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog FAQ NEWS.md README.md man-db-manual.txt man-db-manual.ps
%config(noreplace) %{_sysconfdir}/man_db.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/man-db
%attr(750,root,root) /etc/cron.daily/man-db.cron
%attr(755,root,root) %{_sbindir}/accessdb
%attr(755,root,root) %{_bindir}/apropos
%attr(755,root,root) %{_bindir}/catman
%attr(755,root,root) %{_bindir}/lexgrog
%attr(755,root,root) %{_bindir}/man
%attr(755,root,root) %{_bindir}/man-recode
%attr(755,root,root) %{_bindir}/mandb
%attr(755,root,root) %{_bindir}/manpath
%attr(755,root,root) %{_bindir}/whatis
%dir %{_libdir}/man-db
%attr(755,root,root) %{_libdir}/man-db/*.so
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/man-db
%endif
%attr(755,root,root) %{_libexecdir}/man-db/zsoelim
%{_libexecdir}/man-db/globbing
%{_libexecdir}/man-db/manconv
%{systemdunitdir}/man-db.service
# TODO: as cron.daily replacement
#%{systemdunitdir}/man-db.timer
%{systemdtmpfilesdir}/man-db.conf
%dir %{pkgcachedir}
# documentation and translation
%{_mandir}/man1/apropos.1*
%{_mandir}/man1/lexgrog.1*
%{_mandir}/man1/man.1*
%{_mandir}/man1/man-recode.1*
%{_mandir}/man1/manconv.1*
%{_mandir}/man1/manpath.1*
%{_mandir}/man1/whatis.1*
%{_mandir}/man1/zsoelim.1*
%{_mandir}/man5/manpath.5*
%{_mandir}/man8/accessdb.8*
%{_mandir}/man8/catman.8*
%{_mandir}/man8/mandb.8*
%lang(da) %{_mandir}/da/man*/*
%lang(de) %{_mandir}/de/man*/*
%lang(es) %{_mandir}/es/man*/*
%lang(fr) %{_mandir}/fr/man*/*
%lang(id) %{_mandir}/id/man*/*
%lang(it) %{_mandir}/it/man*/*
%lang(ja) %{_mandir}/ja/man*/*
%lang(ko) %{_mandir}/ko/man*/*
%lang(nl) %{_mandir}/nl/man*/*
%lang(pl) %{_mandir}/pl/man*/*
%lang(pt) %{_mandir}/pt/man*/*
%lang(pt_BR) %{_mandir}/pt_BR/man*/*
%lang(ro) %{_mandir}/ro/man*/*
%lang(ru) %{_mandir}/ru/man*/*
%lang(sr) %{_mandir}/sr/man*/*
%lang(sv) %{_mandir}/sv/man*/*
%lang(tr) %{_mandir}/tr/man*/*
%lang(uk) %{_mandir}/uk/man*/*
%lang(zh_CN) %{_mandir}/zh_CN/man*/*
