# TODO:
# - cgi-bin package - separate, because of suid-root
# - separate plugins into packages
# - use shared versions of lpc10, gsm,...
# - CFLAGS passing
# - fix bluetooth patch
# - package commandline tools (aelparse etc.)
# - system mxml
# - ~/.asterisk_history gets encoded with \xxx on exit, each time yet again
# - openh323 is missing regardless of BR, see http://pld.pastebin.com/f7f84c312
#
# Conditional build:
%bcond_with	rxfax		# without rx (also tx :-D) fax
%bcond_with	bluetooth	# without bluetooth support (NFT)
%bcond_with	zhone		# zhone hack
%bcond_with	zhone_hack	# huge hack workarounding broken zhone channel banks which start randomly
				# issuing pulse-dialled calls to weird numbers
%bcond_with	bristuff	# BRIstuff (Junghanns.NET BRI adapters) support
%bcond_with	verbose		# verbose build

%define		spandsp_version 0.0.2pre26
%define		rel	0.4
Summary:	Asterisk PBX
Summary(pl.UTF-8):	Centralka (PBX) Asterisk
Name:		asterisk
Version:	1.6.1.12
Release:	%{rel}%{?with_bristuff:.bristuff}
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.digium.com/pub/asterisk/releases/%{name}-%{version}.tar.gz
# Source0-md5:	d6bc1448b8fa274a2acaef1b15f4d485
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	http://downloads.digium.com/pub/telephony/sounds/releases/%{name}-core-sounds-en-gsm-1.4.13.tar.gz
# Source3-md5:	65add705003e9aebdb4cd03bd1a26f97
Source4:	http://downloads.digium.com/pub/telephony/sounds/%{name}-moh-freeplay-wav.tar.gz
# Source4-md5:	e523fc2b4ac524f45da7815e97780540
Source5:	%{name}.logrotate
Source10:	http://soft-switch.org/downloads/spandsp/spandsp-%{spandsp_version}/asterisk-1.2.x/app_txfax.c
# Source10-md5:	8c8fcb263b76897022b4c28052a7b439
Source11:	http://soft-switch.org/downloads/spandsp/spandsp-%{spandsp_version}/asterisk-1.2.x/app_rxfax.c
# Source11-md5:	ab6983b51c412883545b36993d704999
Patch2:		%{name}-no_k6_on_sparc.patch
Patch3:		%{name}-lib.patch
Patch4:		%{name}-ppc.patch
Patch5:		external-libedit.patch
Patch6:		pkg-config-gmime.patch
Patch7:		FHS-paths.patch
# http://soft-switch.org/downloads/spandsp/spandsp-%{spandsp_version}/asterisk-1.2.x/apps_Makefile.patch
Patch10:	%{name}-txfax-Makefile.patch
Patch12:	%{name}-chan_bluetooth.patch
Patch13:	%{name}-zhone.patch
# http://svn.debian.org/wsvn/pkg-voip/asterisk/trunk/debian/patches/bristuff
Patch14:	%{name}-bristuff.patch
Patch15:	%{name}-bristuff-build.patch
Patch16:	%{name}-bristuff-libpri.patch
URL:		http://www.asterisk.org/
BuildRequires:	OSPToolkit
BuildRequires:	SDL_image-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
%{?with_bluetooth:BuildRequires: bluez-devel}
BuildRequires:	curl-devel
BuildRequires:	dahdi-linux-devel
BuildRequires:	dahdi-tools-devel
BuildRequires:	freetds-devel >= 0.63
BuildRequires:	gawk
BuildRequires:	gcc >= 5:3.4
BuildRequires:	gmime22-devel
BuildRequires:	iksemel-devel
BuildRequires:	imap-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libcap-devel
BuildRequires:	libedit-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	mISDNuser-devel
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel
BuildRequires:	newt-devel
BuildRequires:	openais-devel
BuildRequires:	openh323-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	portaudio-devel
BuildRequires:	postgresql-devel
BuildRequires:	pwlib-devel
BuildRequires:	radiusclient-ng-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	spandsp-devel
%{?with_rxfax:BuildRequires:	spandsp-devel-%{spandsp_version}}
BuildRequires:	speex-devel
BuildRequires:	sqlite-devel
BuildRequires:	sqlite3-devel
BuildRequires:	unixODBC-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
%if %{with bristuff}
BuildRequires:	libgsmat-devel
BuildRequires:	libpri-bristuff-devel >= 1.2.4
%else
BuildRequires:	libpri-devel >= 1.2.4
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
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
%setup -q
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p0
%patch7 -p0

%if %{with zhone}
sed -i -e 's|.*#define.*ZHONE_HACK.*|#define ZHONE_HACK 1|g' channels/chan_zap.c
%endif

%if %{with rxfax}
cd apps
%patch10 -p0
cp %{SOURCE10} .
cp %{SOURCE11} .
%endif

%{?with_bluetooth:%patch12 -p1}
%{?with_zhonehack:%patch13 -p1}

%if %{with bristuff}
%patch14 -p1
%patch15 -p1
%patch16 -p1
%endif

# avoid using it
rm -rf imap

%build
rm -f pbx/.depend

%{__aclocal} -I autoconf
%{__autoheader}
%{__autoconf}

export CPPFLAGS="%{rpmcppflags} -I/usr/include/openh323"
export WGET="/bin/true"

# be sure to invoke ./configure with our flags
cd menuselect/mxml
%configure2_13
cd ../../

cd menuselect
%{__aclocal}
%{__autoheader}
%{__autoconf}
%configure
cd ..

cd main/editline
%configure2_13
cd ../..

%configure \
	%{?with_bristuff:--with-gsmat=%{_prefix}} \
	--with-imap=system \
	--with-gsm=/usr \
	--with-libedit=yes

# safe checks
%{?with_bristuff:grep '^#define HAVE_GSMAT 1' include/asterisk/autoconfig.h || exit 1}

cp -f .cleancount .lastclean

%{__make} -j1 -C menuselect \
	%{?with_verbose:NOISY_BUILD=yes} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{__make} -j1 \
	%{?with_verbose:NOISY_BUILD=yes} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}" \
	CHANNEL_LIBS+=chan_bluetooth.so || :

# rerun needed; asterisk wants that
%{__make} -j1 \
	%{?with_verbose:NOISY_BUILD=yes} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}" \
	CHANNEL_LIBS+=chan_bluetooth.so

# it requires doxygen - I don't know if we should do this...
#%{__make} progdocs

# safe checks
%{?with_bristuff:objdump -p channels/chan_zap.so | grep -qE 'NEEDED +libgsmat\.so' || exit 1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/{log/asterisk/cdr-csv,spool/asterisk/monitor},/etc/{rc.d/init.d,sysconfig,logrotate.d}}

install %{SOURCE3} sounds
install %{SOURCE4} sounds
install %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -j1 samples \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

# unpackaged at this point
rm $RPM_BUILD_ROOT/var/lib/asterisk/moh/.asterisk-moh-opsound-wav
rm $RPM_BUILD_ROOT/var/lib/asterisk/moh/CHANGES-asterisk-moh-opsound-wav
rm $RPM_BUILD_ROOT/var/lib/asterisk/moh/CREDITS-asterisk-moh-opsound-wav
rm $RPM_BUILD_ROOT/var/lib/asterisk/moh/LICENSE-asterisk-moh-opsound-wav
rm $RPM_BUILD_ROOT/var/lib/asterisk/sounds/.asterisk-core-sounds-en-gsm-1.4.16
rm $RPM_BUILD_ROOT/var/lib/asterisk/sounds/en/CHANGES-asterisk-core-en-1.4.16
rm $RPM_BUILD_ROOT/var/lib/asterisk/sounds/en/core-sounds-en.txt
rm $RPM_BUILD_ROOT/var/lib/asterisk/sounds/en/CREDITS-asterisk-core-en-1.4.16
rm $RPM_BUILD_ROOT/var/lib/asterisk/sounds/en/LICENSE-asterisk-core-en-1.4.16

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add asterisk
# this was insane; breaking all current calls
#%%service asterisk restart "Asterisk daemon"

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/*.adsi
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/*.lua
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions.ael
%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules
%attr(755,root,root) %{_libdir}/asterisk/modules/app_*.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_*.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_*.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_*.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_*.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_*.so
%attr(755,root,root) %{_libdir}/asterisk/modules/pbx_*.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_*.so

%dir /var/lib/asterisk
%dir /var/lib/asterisk/agi-bin
%dir /var/lib/asterisk/images
%dir /var/lib/asterisk/keys
%dir /var/lib/asterisk/moh
/var/lib/asterisk/moh/*.wav
%dir /var/lib/asterisk/sounds
%dir /var/lib/asterisk/sounds/en
%dir /var/lib/asterisk/sounds/en/digits
%dir /var/lib/asterisk/sounds/en/dictate
%dir /var/lib/asterisk/sounds/en/followme
%dir /var/lib/asterisk/sounds/en/letters
%dir /var/lib/asterisk/sounds/en/phonetic
%dir /var/lib/asterisk/sounds/en/silence
/var/lib/asterisk/images/*.jpg
/var/lib/asterisk/keys/*.pub
/var/lib/asterisk/phoneprov
/var/lib/asterisk/sounds/en/*.gsm
/var/lib/asterisk/sounds/en/digits/*.gsm
/var/lib/asterisk/sounds/en/dictate/*.gsm
/var/lib/asterisk/sounds/en/followme/*.gsm
/var/lib/asterisk/sounds/en/letters/*.gsm
/var/lib/asterisk/sounds/en/phonetic/*.gsm
/var/lib/asterisk/sounds/en/silence/*.gsm
/var/lib/asterisk/static-http
%dir /var/spool/asterisk
%dir /var/spool/asterisk/monitor
%dir /var/spool/asterisk/voicemail
%dir /var/spool/asterisk/voicemail/default
%dir /var/spool/asterisk/voicemail/default/1234
%dir /var/spool/asterisk/voicemail/default/1234/en
%dir /var/log/asterisk
%dir /var/log/asterisk/cdr-csv
%{_mandir}/man8/asterisk.8*
%{_mandir}/man8/astgenkey.8*
%{_mandir}/man8/autosupport.8*
%{_mandir}/man8/safe_asterisk.8*
%dir /var/lib/asterisk/firmware
%dir /var/lib/asterisk/firmware/iax
#/var/lib/asterisk/firmware/iax/iaxy.bin

%files examples
%defattr(644,root,root,755)
%attr(755,root,root) /var/lib/asterisk/agi-bin/agi-test.agi
%attr(755,root,root) /var/lib/asterisk/agi-bin/eagi-sphinx-test
%attr(755,root,root) /var/lib/asterisk/agi-bin/eagi-test
%attr(755,root,root) /var/lib/asterisk/agi-bin/jukebox.agi
/var/spool/asterisk/voicemail/default/1234/en/busy.gsm
/var/spool/asterisk/voicemail/default/1234/en/unavail.gsm

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/asterisk
%{_includedir}/asterisk/*.h
%{_includedir}/asterisk.h
