# TODO:
# - cgi-bin package - separate, because of suid-root
# - use shared versions of LIBILBC:=ilbc/libilbc.a (ilbc not enabled currently)
# - CFLAGS passing
# - fix bluetooth patch
# - make package for moh sound files
# - likely odbc and imap broken (identical code, some #define not working, etc):
#   *** WARNING: identical binaries are copied, not linked:
#     %attr(755,root,root) %{_libdir}/asterisk/modules/app_directory_odbc.so
#   and  /usr/lib64/asterisk/modules/app_directory_imap.so
#   *** WARNING: identical binaries are copied, not linked:
#     %attr(755,root,root) %{_libdir}/asterisk/modules/app_directory_plain.so
#   and  /usr/lib64/asterisk/modules/app_directory_imap.so
# - ncurses dep gone for good (replaced by libedit)?
# - missing/failed features:
# $ grep =0 build_tools/menuselect-deps
#   NBS=0 AST_EXT_LIB_SETUP([NBS], [Network Broadcast Sound], [nbs])
#   SS7=0 AST_EXT_LIB_SETUP([SS7], [ISDN SS7], [ss7])
#   VPBAPI=0 AST_EXT_LIB_SETUP([VPB], [Voicetronix API], [vpb])
# - app_{rx,tx}fax seems to b replaced by app_fax alongside latest spanddsp
#   See: http://sourceforge.net/projects/agx-ast-addons/
#        https://agx-ast-addons.svn.sourceforge.net/svnroot/agx-ast-addons/trunk/attic/
#
# Conditional build:
%bcond_with	rxfax		# without rx (also tx:-D) fax
%bcond_with	bluetooth	# without bluetooth support (NFT)
%bcond_with	zhone		# zhone hack
%bcond_with	zhone_hack	# huge hack workarounding broken zhone channel banks which start randomly
				# issuing pulse-dialled calls to weird numbers
%bcond_with	bristuff	# BRIstuff (Junghanns.NET BRI adapters) support
%bcond_with	misdn		# chan_misdn
%bcond_with	openais		# openais is dead project
%bcond_with	h323		# without h323 support
%bcond_without	apidocs		# disable apidocs building
%bcond_without	verbose		# verbose build

%define		spandsp_version 0.0.2pre26
%define		rel	1	
Summary:	Asterisk PBX
Summary(pl.UTF-8):	Centralka (PBX) Asterisk
Name:		asterisk
Version:	1.8.29.0
Release:	%{rel}%{?with_bristuff:.bristuff}
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.digium.com/pub/asterisk/releases/%{name}-%{version}.tar.gz
# Source0-md5:	23778d7ebefdecd4c742d5de39f5e2c1
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
Source5:	%{name}.logrotate
Source10:	app_txfax.c
Source11:	app_rxfax.c
Patch0:		mxml-system.patch
Patch1:		lua51-path.patch
Patch3:		%{name}-lib.patch
Patch4:		%{name}-ppc.patch
Patch5:		external-libedit.patch
Patch6:		pkg-config-gmime.patch
Patch7:		FHS-paths.patch
Patch8:		libedit-history.patch
Patch9:		pld-banner.patch
# http://soft-switch.org/downloads/spandsp/spandsp-%{spandsp_version}/asterisk-1.2.x/apps_Makefile.patch
Patch10:	%{name}-txfax-Makefile.patch
Patch11:	%{name}-chan_bluetooth.patch
Patch12:	%{name}-zhone.patch
# http://svn.debian.org/wsvn/pkg-voip/asterisk/trunk/debian/patches/bristuff
Patch13:	%{name}-bristuff.patch
Patch14:	%{name}-bristuff-build.patch
Patch15:	%{name}-bristuff-libpri.patch
Patch16:	lpc10-system.patch
Patch17:	gsm-libpoison.patch
Patch18:	Fix-history-loading-when-using-external-libedit.patch
URL:		http://www.asterisk.org/
BuildRequires:	OSPToolkit-devel >= 3.6.1
BuildRequires:	SDL_image-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
%{?with_bluetooth:BuildRequires: bluez-devel}
BuildRequires:	curl-devel
BuildRequires:	dahdi-linux-devel
BuildRequires:	dahdi-tools-devel >= 2.0.0
BuildRequires:	doxygen
BuildRequires:	freetds-devel >= 0.63
BuildRequires:	gawk
BuildRequires:	gcc >= 5:3.4
BuildRequires:	gmime22-devel
BuildRequires:	gtk+2-devel
BuildRequires:	iksemel-devel
BuildRequires:	imap-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libcap-devel
BuildRequires:	libedit-devel
BuildRequires:	libgsm-devel
BuildRequires:	libical-devel
BuildRequires:	pkgconfig(libilbc)
BuildRequires:	libogg-devel
BuildRequires:	libresample-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
BuildRequires:	lpc10-devel
BuildRequires:	lua51-devel
%if %{with misdn}
BuildRequires:	mISDNuser-devel >= 1.1
BuildConflicts:	mISDNuser-devel >= 2.0
%endif
BuildRequires:	mxml-devel
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	neon-devel
BuildRequires:	net-snmp-devel
BuildRequires:	newt-devel
%{?with_openais:BuildRequires:	openais-devel}
%if %{with h323}
BuildRequires:	openh323-devel >= 1.19.0
%endif
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	portaudio-devel >= 19
BuildRequires:	postgresql-devel
%if %{with h323}
BuildRequires:	pwlib-devel
%endif
BuildRequires:	radiusclient-ng-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	spandsp-devel >= 0.0.5
BuildRequires:	speex-devel
BuildRequires:	sqlite-devel
BuildRequires:	sqlite3-devel
BuildRequires:	srtp-devel
BuildRequires:	unixODBC-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(asterisk)
Provides:	user(asterisk)
%if %{with bristuff}
BuildRequires:	libgsmat-devel
BuildRequires:	libpri-bristuff-devel >= 1.2.4
%else
BuildRequires:	libpri-devel >= 1.4.6
%endif
Requires(post,preun):	/sbin/chkconfig
%if %{with fc}
BuildRequires:	libss7-devel >= 1.0.1
BuildRequires:	libtool-ltdl-devel
BuildRequires:	libusb-devel
BuildRequires:	lm_sensors-devel
%endif
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

%package ais
Summary:	Modules for Asterisk that use OpenAIS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description ais
Modules for Asterisk that use OpenAIS.

%package alsa
Summary:	Modules for Asterisk that use Alsa sound drivers
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description alsa
Modules for Asterisk that use Alsa sound drivers.

%package astman
Summary:	Astman is a text mode Manager for Asterisk
Group:		Applications/Networking

%description astman
Astman is a text mode Manager for Asterisk.

Astman connects to Asterisk by TCP, so you can run Astman on a
completely different computer than your Asterisk computer.

%package curl
Summary:	Modules for Asterisk that use cURL
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description curl
Modules for Asterisk that use cURL.

%package dahdi
Summary:	Modules for Asterisk that use DAHDI
Group:		Applications/Networking
Requires(pre):	/usr/sbin/usermod
Requires:	%{name} = %{version}-%{release}
Requires:	dahdi-tools >= 2.0.0

%description dahdi
Modules for Asterisk that use DAHDI.

%package fax
Summary:	FAX applications for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description fax
FAX applications for Asterisk

%package festival
Summary:	Festival application for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	festival

%description festival
Application for the Asterisk PBX that uses Festival to convert text to
speech.

%package gsm
Summary:	Support GSM audio encoding/decoding
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description gsm
Support GSM audio encoding/decoding.

%package h323
Summary:	H.323 protocol support for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description h323
This channel driver (chan_h323) provides support for the H.323
protocol for Asterisk. This is an implementation originally
contributed by NuFone and nowdays maintained and distributed by
Digium, Inc. Hence, it is considered the official H.323 chanel driver.

%package http
Summary:	HTTP Server Support
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description http
HTTP Server Support.

%package ices
Summary:	Stream audio from Asterisk to an IceCast server
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	ices
Obsoletes:	asterisk < 1.4.18-1
Conflicts:	asterisk < 1.4.18-1

%description ices
Stream audio from Asterisk to an IceCast server.

%package jabber
Summary:	Jabber/XMPP resources for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description jabber
Jabber/XMPP resources for Asterisk.

%package jack
Summary:	JACK resources for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description jack
JACK resources for Asterisk.

%package lua
Summary:	Lua resources for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description lua
Lua resources for Asterisk.

%package ldap
Summary:	LDAP resources for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description ldap
LDAP resources for Asterisk.

%package ldap-fds
Summary:	LDAP resources for Asterisk and the Fedora Directory Server
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-ldap = %{version}-%{release}
Requires:	fedora-ds-base

%description ldap-fds
LDAP resources for Asterisk and the Fedora Directory Server.

%package lpc10
Summary:	LPC-10 2400 bps Voice Codec support
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description lpc10
LPC-10 2400 bps Voice Codec support

%package misdn
Summary:	mISDN channel for Asterisk
Group:		Applications/Networking
Requires(pre):	/usr/sbin/usermod
Requires:	%{name} = %{version}-%{release}

%description misdn
mISDN channel for Asterisk.

%package minivm
Summary:	MiniVM applicaton for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description minivm
MiniVM application for Asterisk.

%package odbc
Summary:	Applications for Asterisk that use ODBC (except voicemail)
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description odbc
Applications for Asterisk that use ODBC (except voicemail)

%package osp
Summary:	Modules for Asterisk that use Open Settlement Protocol (OSP) Applications
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description osp
Open Settlement Protocol (OSP) Applications.

%package oss
Summary:	Modules for Asterisk that use OSS sound drivers
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description oss
Modules for Asterisk that use OSS sound drivers.

%package portaudio
Summary:	Modules for Asterisk that use the portaudio library
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description portaudio
Modules for Asterisk that use the portaudio library.

%package postgresql
Summary:	Applications for Asterisk that use PostgreSQL
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description postgresql
Applications for Asterisk that use PostgreSQL.

%package radius
Summary:	Applications for Asterisk that use RADIUS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description radius
Applications for Asterisk that use RADIUS.

%package resample
Summary:	resample codec
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description resample
resample codec.

%package skinny
Summary:	Modules for Asterisk that support the SCCP/Skinny protocol
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description skinny
Modules for Asterisk that support the SCCP/Skinny protocol.

%package snmp
Summary:	Module that enables SNMP monitoring of Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description snmp
Module that enables SNMP monitoring of Asterisk.

%package speex
Summary:	Speex codec support
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description speex
Speex codec support.

%package sqlite
Summary:	Sqlite modules for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description sqlite
Sqlite modules for Asterisk.

%package tds
Summary:	Modules for Asterisk that use FreeTDS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description tds
Modules for Asterisk that use FreeTDS.

%package unistim
Summary:	Unistim channel for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description unistim
Unistim channel for Asterisk

%package voicemail
Summary:	Common Voicemail Modules for Asterisk
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-voicemail-implementation = %{version}-%{release}
Requires:	/usr/lib/sendmail
Requires:	sox

%description voicemail
Common Voicemail Modules for Asterisk.

%package voicemail-imap
Summary:	Store voicemail on an IMAP server
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-voicemail = %{version}-%{release}
Provides:	%{name}-voicemail-implementation = %{version}-%{release}

%description voicemail-imap
Voicemail implementation for Asterisk that stores voicemail on an IMAP
server.

%package voicemail-odbc
Summary:	Store voicemail in a database using ODBC
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-voicemail = %{version}-%{release}
Provides:	%{name}-voicemail-implementation = %{version}-%{release}

%description voicemail-odbc
Voicemail implementation for Asterisk that uses ODBC to store
voicemail in a database.

%package voicemail-plain
Summary:	Store voicemail on the local filesystem
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-voicemail = %{version}-%{release}
Provides:	%{name}-voicemail-implementation = %{version}-%{release}

%description voicemail-plain
Voicemail implementation for Asterisk that stores voicemail on the
local filesystem.

%package vorbis
Summary:	Ogg Vorbis format support
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description vorbis
Ogg Vorbis format support.

# define apidocs as last package, as it is the biggest one
%package apidocs
Summary:	API documentation for Asterisk
Group:		Documentation

%description apidocs
API documentation for Asterisk.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
#%patch6 -p0
%patch7 -p1
%patch8 -p1
%patch9 -p1
%if %{with zhone}
sed -i -e 's|.*#define.*ZHONE_HACK.*|#define ZHONE_HACK 1|g' channels/chan_zap.c
%endif
%if %{with rxfax}
cd apps
%patch10 -p0
cp %{SOURCE10} .
cp %{SOURCE11} .
%endif
%{?with_bluetooth:%patch11 -p1}
%{?with_zhonehack:%patch12 -p1}
%if %{with bristuff}
%patch13 -p1
%patch14 -p1
%patch15 -p1
%endif
%patch16 -p1
%patch17 -p1
%patch18 -p1

# Fixup makefile so sound archives aren't downloaded/installed
%{__sed} -i -e 's/^all:.*$/all:/' sounds/Makefile
%{__sed} -i -e 's/^install:.*$/install:/' sounds/Makefile

# avoid using these
rm -rf imap menuselect/mxml main/editline codecs/gsm codecs/lpc10

%build
rm -f pbx/.depend

%{__aclocal} -I autoconf
%{__autoheader}
%{__autoconf}

export ASTCFLAGS="%{rpmcflags}"
export ASTLDFLAGS="%{rpmldflags}"
export WGET="/bin/true"

# be sure to invoke ./configure with our flags
cd menuselect
%{__aclocal} -I ../autoconf
%{__autoheader}
%{__autoconf}
# we need just plain cli for building
%configure \
  --without-newt \
  --without-gtk2 \
  --without-curses \
  --without-ncurses
cd ..

%configure \
	%{?with_bristuff:--with-gsmat=%{_prefix}} \
	--with-imap=system \
	--with-gsm=/usr \
	%{!?with_h323:--without-h323} \
	--with-lpc10=/usr \
	--with-libedit=yes

# safe checks
%{?with_bristuff:grep '^#define HAVE_GSMAT 1' include/asterisk/autoconfig.h || exit 1}

cp -f .cleancount .lastclean

%if %{with h323}
# included conditionally, so make sure its there first
%{__make} -C channels/h323 Makefile.ast \
	%{?with_verbose:NOISY_BUILD=yes} \
%endif

%{__make} DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \

rm apps/app_voicemail.o apps/app_directory.o
mv apps/app_voicemail.so apps/app_voicemail_plain.so
mv apps/app_directory.so apps/app_directory_plain.so

%{__sed} -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=IMAP_STORAGE/' menuselect.makeopts
%{__make} DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \

rm apps/app_voicemail.o apps/app_directory.o
mv apps/app_voicemail.so apps/app_voicemail_imap.so
mv apps/app_directory.so apps/app_directory_imap.so

%{__sed} -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=ODBC_STORAGE/' menuselect.makeopts
%{__make} DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \

rm apps/app_voicemail.o apps/app_directory.o
mv apps/app_voicemail.so apps/app_voicemail_odbc.so
mv apps/app_directory.so apps/app_directory_odbc.so

# so that these modules don't get built again during the install phase
touch apps/app_voicemail.o apps/app_directory.o
touch apps/app_voicemail.so apps/app_directory.so

%if %{with apidocs}
%{__make} progdocs \
	DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \
%endif

%{__make} \
	DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \
	CHANNEL_LIBS+=chan_bluetooth.so || :

# rerun needed; asterisk wants that
%{__make} \
	DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \
	CHANNEL_LIBS+=chan_bluetooth.so

# safe checks
%{?with_bristuff:objdump -p channels/chan_zap.so | grep -qE 'NEEDED +libgsmat\.so' || exit 1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/{log/asterisk/cdr-csv,spool/asterisk/monitor},/etc/{rc.d/init.d,sysconfig,logrotate.d}} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

export ASTCFLAGS="%{rpmcflags}"

%{__make} -j1 install \
	DEBUG= \
	OPTIMIZE= \
	DESTDIR=$RPM_BUILD_ROOT \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk

%{__make} -j1 samples \
	DEBUG= \
	OPTIMIZE= \
	DESTDIR=$RPM_BUILD_ROOT \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk

rm $RPM_BUILD_ROOT%{_libdir}/asterisk/modules/app_directory.so
rm $RPM_BUILD_ROOT%{_libdir}/asterisk/modules/app_voicemail.so
install -D -p apps/app_directory_imap.so $RPM_BUILD_ROOT%{_libdir}/asterisk/modules
install -D -p apps/app_voicemail_imap.so $RPM_BUILD_ROOT%{_libdir}/asterisk/modules
install -D -p apps/app_directory_odbc.so $RPM_BUILD_ROOT%{_libdir}/asterisk/modules
install -D -p apps/app_voicemail_odbc.so $RPM_BUILD_ROOT%{_libdir}/asterisk/modules
install -D -p apps/app_directory_plain.so $RPM_BUILD_ROOT%{_libdir}/asterisk/modules
install -D -p apps/app_voicemail_plain.so $RPM_BUILD_ROOT%{_libdir}/asterisk/modules

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -a %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

install %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

# create some directories that need to be packaged
install -d $RPM_BUILD_ROOT%{_datadir}/asterisk/moh
install -d $RPM_BUILD_ROOT%{_datadir}/asterisk/sounds
ln -s %{_localstatedir}/lib/asterisk/licenses $RPM_BUILD_ROOT%{_datadir}/asterisk/licenses

install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/asterisk/licenses
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/asterisk/cdr-custom
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/festival
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/monitor
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/outgoing
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/uploads

# We're not going to package any of the sample AGI scripts
rm -f $RPM_BUILD_ROOT%{_datadir}/asterisk/agi-bin/*

# Don't package the sample voicemail user
rm -rf $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/voicemail/default

# Don't package example phone provision configs
rm -rf $RPM_BUILD_ROOT%{_datadir}/asterisk/phoneprov/*

# these are compiled with -O0 and thus include unfortified code.
rm -rf $RPM_BUILD_ROOT%{_sbindir}/hashtest
rm -rf $RPM_BUILD_ROOT%{_sbindir}/hashtest2

# we're not using safe_asterisk
rm -f $RPM_BUILD_ROOT%{_sbindir}/safe_asterisk
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/safe_asterisk.8*

rm -rf $RPM_BUILD_ROOT%{_datadir}/asterisk/firmware/iax/*

%if %{with apidocs}
find doc/api/html -name '*.map' -size 0 -delete
%endif

#fixme
rm  $RPM_BUILD_ROOT/etc/asterisk/{app_mysql,cdr_mysql,chan_mobile,chan_ooh323,misdn%{!?with_h323:,h323},res_config_mysql,res_pktccops}.conf

rm -fr $RPM_BUILD_ROOT/usr/include/asterisk/doxygen

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 188 asterisk
%useradd -u 188 -r -s /sbin/nologin -d /var/lib/asterisk -M -c 'Asterisk User' -g asterisk asterisk

%postun
if [ "$1" = 0 ]; then
	%userremove asterisk
	%groupremove asterisk
fi

%post
/sbin/chkconfig --add asterisk
# use -n (NOOP) as restart would be breaking all current calls.
%service -n asterisk restart "Asterisk daemon"

%preun
if [ "$1" = "0" ]; then
	%service asterisk stop
	/sbin/chkconfig --del asterisk
fi

%triggerpostun -- %{name} < 1.6.1.12-0.1
# chown to asterisk previously root owned files
# loose one (not one that cames from rpm), as we're not trying to split the
# hair with file permission bits.
chown -R asterisk:asterisk /var/spool/asterisk
chown -R asterisk:asterisk /var/lib/asterisk

%files
%defattr(644,root,root,755)
%doc README *.txt ChangeLog BUGS CREDITS configs
%doc doc/asterisk.sgml

#%attr(755,root,root) %{_sbindir}/aelparse
%attr(755,root,root) %{_sbindir}/astcanary
%attr(755,root,root) %{_sbindir}/asterisk
%attr(755,root,root) %{_sbindir}/astgenkey
%attr(755,root,root) %{_sbindir}/autosupport
#%attr(755,root,root) %{_sbindir}/conf2ael
#%attr(755,root,root) %{_sbindir}/muted
%attr(755,root,root) %{_sbindir}/rasterisk
#%attr(755,root,root) %{_sbindir}/refcounter
#%attr(755,root,root) %{_sbindir}/smsq
#%attr(755,root,root) %{_sbindir}/stereorize
#%attr(755,root,root) %{_sbindir}/streamplayer
%{_mandir}/man8/asterisk.8*
%{_mandir}/man8/astgenkey.8*
%{_mandir}/man8/autosupport.8*

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%attr(750,root,asterisk) %dir %{_sysconfdir}/asterisk
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/adsi.conf
#%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/adtranvofr.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/agents.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/alarmreceiver.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/amd.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/asterisk.adsi
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/asterisk.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/calendar.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/ccss.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_custom.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_manager.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_syslog.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_custom.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cli.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cli_aliases.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cli_permissions.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/codecs.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/dnsmgr.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/dsp.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/dundi.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/enum.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extconfig.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions.ael
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/features.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/followme.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/iax.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/iaxprov.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/indications.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/logger.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/manager.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/mgcp.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/modules.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/musiconhold.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/muted.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/phone.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/phoneprov.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/queuerules.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/queues.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_stun_monitor.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/rtp.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/say.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/sip*.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/sla.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/smdi.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/telcordia-1.adsi
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/udptl.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/users.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/vpb.conf

%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules

%attr(755,root,root) %{_libdir}/asterisk/modules/app_adsiprog.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_alarmreceiver.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_amd.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_authenticate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_cdr.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_celgenuserevent.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_chanisavail.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_channelredirect.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_chanspy.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_confbridge.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_controlplayback.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_db.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_dial.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_dictate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_directed_pickup.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_disa.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_dumpchan.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_echo.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_exec.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_externalivr.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_followme.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_forkcdr.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_getcpeid.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_image.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_macro.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_milliwatt.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_mixmonitor.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_morsecode.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_mp3.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_nbscat.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_originate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_parkandannounce.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_playback.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_playtones.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_privacy.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_queue.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_read.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_readexten.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_readfile.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_record.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_sayunixtime.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_senddtmf.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_sendtext.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_setcallerid.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_sms.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_softhangup.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_speech_utils.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_stack.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_system.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_talkdetect.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_test.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_transfer.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_url.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_userevent.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_verbose.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_waitforring.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_waitforsilence.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_waituntil.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_while.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_zapateller.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_builtin_features.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_multiplexed.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_simple.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_softmix.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_csv.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_custom.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_manager.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_syslog.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_custom.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_manager.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_agent.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_bridge.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_iax2.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_local.so
#%attr(755,root,root) %{_libdir}/asterisk/modules/chan_mgcp.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_multicast_rtp.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_phone.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_sip.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_a_mu.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_adpcm.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_alaw.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_g722.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_g726.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_ilbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_ulaw.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_g719.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_g723.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_g726.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_g729.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_h263.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_h264.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_ilbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_jpeg.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_pcm.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_siren14.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_siren7.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_sln.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_sln16.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_vox.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_wav.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_aes.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_audiohookinherit.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_base64.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_blacklist.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_callcompletion.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_callerid.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_cdr.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_channel.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_config.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_cut.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_db.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_devstate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_dialgroup.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_dialplan.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_enum.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_env.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_extstate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_frame_trace.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_global.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_groupcount.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_iconv.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_lock.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_logic.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_math.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_md5.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_module.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_pitchshift.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_rand.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_realtime.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_sha1.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_shell.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_sprintf.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_srv.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_strings.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_sysinfo.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_timeout.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_uri.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_version.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_volume.so
%attr(755,root,root) %{_libdir}/asterisk/modules/pbx_ael.so
%attr(755,root,root) %{_libdir}/asterisk/modules/pbx_config.so
%attr(755,root,root) %{_libdir}/asterisk/modules/pbx_dundi.so
%attr(755,root,root) %{_libdir}/asterisk/modules/pbx_loopback.so
%attr(755,root,root) %{_libdir}/asterisk/modules/pbx_realtime.so
%attr(755,root,root) %{_libdir}/asterisk/modules/pbx_spool.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_adsi.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ael_share.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_agi.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar_caldav.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar_ews.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar_exchange.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar_icalendar.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_clialiases.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_clioriginate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_convert.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_crypto.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_limit.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_monitor.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_mutestream.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_musiconhold.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_phoneprov.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_realtime.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_rtp_asterisk.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_rtp_multicast.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_security_log.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_smdi.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_speech.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_srtp.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_stun_monitor.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_timing_pthread.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_timing_timerfd.so
#%attr(755,root,root) %{_libdir}/asterisk/modules/test_dlinklists.so
#%attr(755,root,root) %{_libdir}/asterisk/modules/test_heap.so
/usr/lib/tmpfiles.d/%{name}.conf

%dir %{_datadir}/asterisk
%dir %{_datadir}/asterisk/agi-bin
%dir %{_datadir}/asterisk/firmware
%dir %{_datadir}/asterisk/firmware/iax
%dir %{_datadir}/asterisk/images
%dir %{_datadir}/asterisk/moh
%dir %{_datadir}/asterisk/sounds
%dir %attr(750,root,asterisk) %{_datadir}/asterisk/keys
# no need to protect publicly downloaded and packaged .pub
#%{_datadir}/asterisk/keys/*.pub
%{_datadir}/asterisk/images/*.jpg
%{_datadir}/asterisk/phoneprov
%{_datadir}/asterisk/licenses

%dir %{_datadir}/asterisk/documentation
%{_datadir}/asterisk/documentation/appdocsxml.dtd
%{_datadir}/asterisk/documentation/core-en_US.xml

%attr(770,root,asterisk) %dir %{_localstatedir}/lib/asterisk
%dir %attr(750,root,asterisk) %{_localstatedir}/lib/asterisk/licenses

%attr(770,root,asterisk) %dir %{_localstatedir}/log/asterisk
%attr(770,root,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-csv
%attr(770,root,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-custom

%attr(770,root,asterisk) %dir %{_localstatedir}/spool/asterisk
%attr(770,root,asterisk) %dir %{_localstatedir}/spool/asterisk/monitor
%attr(770,root,asterisk) %dir %{_localstatedir}/spool/asterisk/outgoing
%attr(770,root,asterisk) %dir %{_localstatedir}/spool/asterisk/tmp
%attr(770,root,asterisk) %dir %{_localstatedir}/spool/asterisk/uploads
%attr(770,root,asterisk) %dir %{_localstatedir}/spool/asterisk/voicemail

%attr(775,root,asterisk) %dir %{_localstatedir}/run/asterisk

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/asterisk
%{_includedir}/asterisk/*.h
%{_includedir}/asterisk.h

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/api/html/*
%endif

%if %{with openais}
%files ais
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/ais.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ais.so
%endif

%files alsa
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/alsa.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_alsa.so

#%files astman
#%defattr(644,root,root,755)
#%attr(755,root,root) %{_sbindir}/astman

%files curl
%defattr(644,root,root,755)
%doc contrib/scripts/dbsep.cgi
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/dbsep.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_curl.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/func_curl.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_curl.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_curl.so

%files dahdi
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/meetme.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/chan_dahdi.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/app_dahdibarge.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_dahdiras.so
#%attr(755,root,root) %{_libdir}/asterisk/modules/app_dahdiscan.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_flash.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_meetme.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_page.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_dahdi.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_dahdi.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_timing_dahdi.so

%files fax
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_fax.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/res_fax.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_fax_spandsp.so

%files festival
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/festival.conf
%attr(770,root,asterisk) %dir %{_localstatedir}/spool/asterisk/festival
%attr(755,root,root) %{_libdir}/asterisk/modules/app_festival.so

%files gsm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_gsm.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_gsm.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_wav_gsm.so

%if %{with h323}
%files h323
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/h323.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_h323.so
%endif

%files http
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/http.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/res_http_post.so
%{_datadir}/asterisk/static-http

%files ices
%defattr(644,root,root,755)
%doc contrib/asterisk-ices.xml
%attr(755,root,root) %{_libdir}/asterisk/modules/app_ices.so

%files jabber
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/gtalk.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/jabber.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/jingle.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_gtalk.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_jingle.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_jabber.so

%files jack
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/app_jack.so

%files lua
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions.lua
%attr(755,root,root) %{_libdir}/asterisk/modules/pbx_lua.so

%files ldap
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_ldap.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_ldap.so

%if 0
%files ldap-fds
%defattr(644,root,root,755)
%{_sysconfdir}/dirsrv/schema/99asterisk.ldif
%endif

%files lpc10
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_lpc10.so

%files minivm
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions_minivm.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/minivm.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/app_minivm.so

%if %{with misdn}
%files misdn
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/misdn.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_misdn.so
%endif

%files odbc
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_adaptive_odbc.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_odbc.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_odbc.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/func_odbc.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_odbc.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_adaptive_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_odbc.so

%files osp
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/osp.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/app_osplookup.so

%files oss
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/oss.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_oss.so

%files portaudio
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/console.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_console.so

%files postgresql
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_pgsql.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_pgsql.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_pgsql.conf
%doc contrib/realtime/postgresql/realtime.sql
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_pgsql.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_pgsql.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_pgsql.so

%files radius
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_radius.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_radius.so

%files resample
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_resample.so

%files skinny
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/skinny.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_skinny.so

%files snmp
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_snmp.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/res_snmp.so

%files speex
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_speex.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_speex.so

%files sqlite
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_sqlite3_custom.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_sqlite3_custom.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_config_sqlite.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_sqlite3_custom.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_sqlite.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_sqlite3_custom.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_sqlite.so

%files tds
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_tds.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_tds.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_tds.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_tds.so

%files unistim
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/unistim.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_unistim.so

%files voicemail
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/voicemail.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/func_vmcount.so

%files voicemail-imap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/app_directory_imap.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_voicemail_imap.so

%files voicemail-odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/app_directory_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_voicemail_odbc.so

%files voicemail-plain
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/app_directory_plain.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_voicemail_plain.so

%files vorbis
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/format_ogg_vorbis.so
