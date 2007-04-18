# TODO:
# - cgi-bin package - separate, because of suid-root
# - separate plugins into packages
# - use shared versions of lpc10, gsm,...
# - CFLAGS passing
# - fix bluetooth patch
# - package commandline tools (aelparse etc.)
#
# Conditional build:
%bcond_with	rxfax		# without rx (also tx :-D) fax
%bcond_with	bluetooth		# without bluetooth support (NFT)

%define _spandsp_version 0.0.2pre26
#
Summary:	Asterisk PBX
Summary(pl.UTF-8):	Centralka (PBX) Asterisk
Name:		asterisk
Version:	1.4.2
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://ftp.digium.com/pub/asterisk/releases/%{name}-%{version}.tar.gz
# Source0-md5:	343e2d7b145a30b23d7d814dac2f704c
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	http://ftp.digium.com/pub/telephony/sounds/releases/asterisk-core-sounds-en-gsm-1.4.6.tar.gz
# Source3-md5:	02e582b6c7de58e5eaba220229c0a71a
Source4: 	http://ftp.digium.com/pub/telephony/sounds/asterisk-moh-freeplay-wav.tar.gz
# Source4-md5:	e523fc2b4ac524f45da7815e97780540
Patch1:		%{name}-configure.patch
Patch2:		%{name}-no_k6_on_sparc.patch
Patch3:		%{name}-lib.patch
Patch8:		%{name}-awk.patch
Source10:	http://soft-switch.org/downloads/spandsp/spandsp-%{_spandsp_version}/asterisk-1.2.x/app_txfax.c
# Source10-md5:	8c8fcb263b76897022b4c28052a7b439
Source11:	http://soft-switch.org/downloads/spandsp/spandsp-%{_spandsp_version}/asterisk-1.2.x/app_rxfax.c
# Source11-md5:	ab6983b51c412883545b36993d704999
# http://soft-switch.org/downloads/spandsp/spandsp-%{_spandsp_version}/asterisk-1.2.x/apps_Makefile.patch
Patch10:	%{name}-txfax-Makefile.patch
Patch11:	%{name}-fix-ptlib.patch
Patch12:	%{name}-chan_bluetooth.patch
URL:		http://www.asterisk.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
%{?with_bluetooth:BuildRequires: bluez-devel}
BuildRequires:	freetds >= 0.63
BuildRequires:	gawk
BuildRequires:	gcc >= 5:3.4
BuildRequires:	iksemel-devel
BuildRequires:	libpri-devel >= 1.2.4
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	spandsp-devel < 1:0.0.3
BuildRequires:	spandsp-devel >= 1:0.0.2-0.pre20.1
%{?with_rxfax:BuildRequires:	spandsp-devel-%{_spandsp_version}}
BuildRequires:	speex-devel
BuildRequires:	unixODBC-devel
BuildRequires:	zaptel-devel >= 1.2.10
BuildRequires:	zlib-devel
BuildRequires:	openh323-devel
BuildRequires:	pwlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
%requires_eq	openh323
%requires_eq	pwlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Asterisk is an Open Source PBX and telephony development platform that
can both replace a conventional PBX and act as a platform for
developing custom telephony applications for delivering dynamic
content over a telephone similarly to how one can deliver dynamic
content through a web browser using CGI and a web server.

Asterisk talks to a variety of telephony hardware including BRI, PRI,
POTS, and IP telephony clients using the Inter-Asterisk eXchange
protocol (e.g. gnophone or miniphone). For more information and a
current list of supported hardware, see http://www.asterisk.org/.

%description -l pl.UTF-8
Asterisk to wolnodostępna centralka (PBX) i platforma programistyczna
dla telefonii, mogąca zastąpić konwencjonalne PBX-y oraz służyć jako
platforma do rozwijania własnych aplikacji telefonicznych do
przekazywania dynamicznej treści przez telefon, podobnie jak można
przekazywać dynamiczną treść przez przeglądarkę WWW przy użyciu CGI i
serwera WWW.

Asterisk współpracuje z wielorakim sprzętem telefonicznym, w tym BRI,
PRI, POTS oraz klienty telefonii IP używające protokołu Inter-Asterisk
eXchange (np. gnophone lub miniphone). Więcej informacji i listę
obsługiwanego sprzętu można znaleźć pod http://www.asterisk.org/.

%package devel
Summary:	Header files for Asterisk platform
Summary(pl.UTF-8):	Pliki nagłówkowe platformy Asterisk
Group:		Development

%description devel
Header files for Asterisk development platform.

%description devel -l pl.UTF-8
Pliki nagłówkowe platformy programistycznej Asterisk.

%package examples
Summary:	Example files for the Asterisk PBX
Summary(pl.UTF-8):	Pliki przykładowe dla centralki Asterisk
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description examples
Example files for the Asterisk PBX.

%description examples -l pl.UTF-8
Pliki przykładowe dla centralki Asterisk.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1
#%patch5 -p1
#%patch6 -p1
#%patch7 -p1
%patch8 -p1
#%patch9 -p1

%if %{with rxfax}
cd apps
%patch10 -p0
cp %{SOURCE10} .
cp %{SOURCE11} .
%endif

%patch11 -p1

%if %{with bluetooth}
%patch12 -p1
%endif

sed -i -e "s#/usr/lib/#/usr/%{_lib}/#g#" Makefile

%build
rm -f pbx/.depend

%{__aclocal}
%{__autoconf}

%configure

cp -f .cleancount .lastclean

%{__make} -C menuselect 
%{__make} \
     CC="%{__cc}" \
     OPTIMIZE="%{rpmcflags}" \
		 CHANNEL_LIBS+=chan_bluetooth.so

# it requires doxygen - I don't know if we should do this...
#%{__make} progdocs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/{log/asterisk/cdr-csv,spool/asterisk/monitor},/etc/{rc.d/init.d,sysconfig}}

install %{SOURCE3} sounds
install %{SOURCE4} sounds

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -j1 samples \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add asterisk
%service asterisk restart "Asterisk daemon"

%preun
if [ "$1" = "0" ]; then
	%service asterisk stop
	/sbin/chkconfig --del asterisk
fi

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog CHANGES CREDITS README* UPGRADE.txt configs doc/*.txt
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/asterisk
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/*.adsi
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions.ael
%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules
%attr(755,root,root) %{_libdir}/asterisk/modules/*.so
%dir /var/lib/asterisk
%dir /var/lib/asterisk/agi-bin
%dir /var/lib/asterisk/images
%dir /var/lib/asterisk/keys
%dir /var/lib/asterisk/moh
/var/lib/asterisk/moh/fpm-calm-river.wav
/var/lib/asterisk/moh/fpm-sunshine.wav
/var/lib/asterisk/moh/fpm-world-mix.wav
%dir /var/lib/asterisk/sounds
%dir /var/lib/asterisk/sounds/digits
%dir /var/lib/asterisk/sounds/dictate
%dir /var/lib/asterisk/sounds/followme
%dir /var/lib/asterisk/sounds/letters
%dir /var/lib/asterisk/sounds/phonetic
%dir /var/lib/asterisk/sounds/silence
/var/lib/asterisk/images/*.jpg
/var/lib/asterisk/keys/*.pub
/var/lib/asterisk/sounds/*.gsm
/var/lib/asterisk/sounds/digits/*.gsm
/var/lib/asterisk/sounds/dictate/*.gsm
/var/lib/asterisk/sounds/followme/*.gsm
/var/lib/asterisk/sounds/letters/*.gsm
/var/lib/asterisk/sounds/phonetic/*.gsm
/var/lib/asterisk/sounds/silence/*.gsm
%dir /var/spool/asterisk
%dir /var/spool/asterisk/monitor
#%%dir /var/spool/asterisk/vm
%dir /var/spool/asterisk/voicemail
%dir /var/spool/asterisk/voicemail/default
%dir /var/spool/asterisk/voicemail/default/1234
%dir /var/log/asterisk
%dir /var/log/asterisk/cdr-csv
%{_mandir}/man8/asterisk.8*
%{_mandir}/man8/astgenkey.8*
%{_mandir}/man8/autosupport.8*
%{_mandir}/man8/safe_asterisk.8*
%dir /var/lib/asterisk/firmware
%dir /var/lib/asterisk/firmware/iax
/var/lib/asterisk/firmware/iax/iaxy.bin

%files examples
%defattr(644,root,root,755)
%attr(755,root,root) /var/lib/asterisk/agi-bin/agi-test.agi
%attr(755,root,root) /var/lib/asterisk/agi-bin/eagi-sphinx-test
%attr(755,root,root) /var/lib/asterisk/agi-bin/eagi-test
%attr(755,root,root) /var/lib/asterisk/agi-bin/jukebox.agi
/var/spool/asterisk/voicemail/default/1234/busy.gsm
/var/spool/asterisk/voicemail/default/1234/unavail.gsm

#%dir /var/lib/asterisk/agi-bin/*

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/asterisk
%{_includedir}/asterisk/*.h
%{_includedir}/asterisk.h
