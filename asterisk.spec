# TODO:
# - chan_misdn (BR: mISDNuser-devel 1.x, needs update for 2.0)
# - ffmpeg: sws_getContext now in libswscale, not avcodec
# - gmime: reverse version check order, use gmime-2.6 by default
# - nbs (libnbs, nbs.h)
# - ss7 >= 2.0 (libss7, libssh.h)
# - openr2 (libopenr2, libopenr2.h)
# - pwlib+openh323
# - vpb (libvpb, vpbapi.h)
# - make package for moh sound files
# - build res_ari_mailboxes as an alternative for voicemail subpackages
#
# Conditional build:
%bcond_with	corosync	# res_corosync module (broken in 12.0.0)
%bcond_without	sqlite2		# build without old sqlite support
%bcond_without	oss		# build without OSS audio support (SDL dependency)
%bcond_without	tds		# build without TDS support
%bcond_without	ilbc		# build without iLBC codec support
%bcond_without	ldap		# build without LDAP support
%bcond_without	portaudio	# build without PortAudio support
%bcond_without	bluetooth	# build without PortAudio support
%bcond_without	jack		# build without JACK support
%bcond_without	mysql		# build without MySQL support
%bcond_without	pgsql		# build without PostgreSQL support
%bcond_without	odbc		# build without ODBC support
%bcond_without	radius		# build without Radius support
%bcond_without	pjsip		# build without PJSIP stack
%bcond_without	opus_vp8	# build without Opus codec and VP8 passthrough
%bcond_with	malloc_debug	# build with MALLOC_DEBUG
%bcond_with	system_pjproject # build with system pjproject (see below)

%bcond_without	apidocs		# disable apidocs building
%bcond_without	verbose		# verbose build

# NOTE:
#   Building with system pjproject may be not a good idea. pjproject comes
#   optimized for client usage and asterisk is a SIP server. Asterisk requries
#   pjproject properly patched and configured and keeping our pjproject in sync
#   with Asterisk requirements may be tricky. Also, Asterisk is the only
#   package using pjproject in PLD, so there is little gain with using system
#   one.
#
#   Before switching the 'system_pjproject' bcond make sure the pjproject
#   package is updated to the version used by Asterisk, with all Asterisk
#   patches applied and with configuration synced.

%define pjproject_version	2.14.1

%define	opus_commit	a959f072d3f364be983dd27e6e250b038aaef747

Summary:	Asterisk PBX
Summary(pl.UTF-8):	Centralka (PBX) Asterisk
Name:		asterisk
Version:	18.23.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://downloads.asterisk.org/pub/telephony/asterisk/%{name}-%{version}.tar.gz
# Source0-md5:	7b6812192469b2aa3d56aab802f84b99
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
Source4:	%{name}.logrotate
Source5:	%{name}.service
# menuselect.* -> make menuconfig; choose options; copy resulting files here
Source6:	menuselect.makedeps
Source7:	menuselect.makeopts
# https://github.com/traud/asterisk-opus
Source8:	https://github.com/traud/asterisk-opus/archive/%{opus_commit}/asterisk-opus-%{opus_commit}.tar.gz
# Source8-md5:	6543f01b5d56051d6c9becc4089c0042
Source9:	https://raw.githubusercontent.com/asterisk/third-party/master/pjproject/%{pjproject_version}/pjproject-%{pjproject_version}.tar.bz2
# Source9-md5:	de9feca3e4816b1535f63f9d23c7b45b
Patch0:		lua_versions.patch

Patch2:		FHS-paths.patch
Patch3:		pld-banner.patch
Patch4:		lpc10-system.patch
Patch5:		x32.patch
#Patch7:		%{name}-ilbc.patch
URL:		http://www.asterisk.org/
BuildRequires:	OSPToolkit-devel >= 4.0.0
%{?with_oss:BuildRequires:	SDL-devel}
%{?with_oss:BuildRequires:	SDL_image-devel}
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
# libbfd (used only for debug builds?)
#BuildRequires:	binutils-devel
BuildRequires:	bison >= 2
%{?with_bluetooth:BuildRequires:	bluez-libs-devel}
%{?with_corosync:BuildRequires:	corosync-devel >= 2.0.0}
BuildRequires:	curl-devel >= 7.10.1
BuildRequires:	dahdi-linux-devel
BuildRequires:	dahdi-tools-devel >= 2.0.0
BuildRequires:	doxygen
BuildRequires:	flex
%{?with_tds:BuildRequires:	freetds-devel >= 0.63}
BuildRequires:	gawk
BuildRequires:	gcc >= 5:3.4
# TODO: switch to 2.6
BuildRequires:	gmime22-devel
BuildRequires:	iksemel-devel
BuildRequires:	imap-devel >= 1:2007f-5
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	jansson-devel >= 2.11-2
BuildRequires:	libatomic-devel
BuildRequires:	libcap-devel
BuildRequires:	libedit-devel
BuildRequires:	libgsm-devel
BuildRequires:	libical-devel
BuildRequires:	libogg-devel
BuildRequires:	libpri-devel >= 1.4.6
BuildRequires:	libresample-devel
BuildRequires:	libtiff-devel
BuildRequires:	libuuid-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-devel
BuildRequires:	lpc10-devel
BuildRequires:	lua53-devel >= 5.3
#BuildRequires:	mISDNuser-devel < 2
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	ncurses-devel
BuildRequires:	neon-devel
BuildRequires:	net-snmp-devel
BuildRequires:	newt-devel
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	opus-devel
%{?with_opus_vp8:BuildRequires:	opusfile-devel}
BuildRequires:	pam-devel
%if %{with system_pjproject} && %{with pjsip}
BuildRequires:	pjproject-devel >= 2.6-4
%endif
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_portaudio:BuildRequires:	portaudio-devel >= 19}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_radius:BuildRequires:	radiusclient-ng-devel}
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	sed >= 4.0
BuildRequires:	spandsp-devel >= 0.0.5
BuildRequires:	speex-devel
BuildRequires:	speexdsp-devel
%{?with_sqlite2:BuildRequires:	sqlite-devel >= 2}
BuildRequires:	sqlite3-devel
BuildRequires:	libsrtp2-devel
BuildRequires:	unbound-devel
%{?with_odbc:BuildRequires:	unixODBC-devel}
BuildRequires:	uriparser-devel
%{?with_ilbc:BuildRequires:	webrtc-libilbc-devel >= 2}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 0.38
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(asterisk)
Provides:	user(asterisk)
#Obsoletes:	asterisk-ais # should be in -corosync package (when built)?
Obsoletes:	asterisk-examples
Obsoletes:	asterisk-h323 < 13
#Obsoletes:	asterisk-misdn # what is the status of this plugin?
Obsoletes:	asterisk-pjsip
Obsoletes:	asterisk-usbradio < 10.4.0
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# references symbols in the asterisk binary
%define		skip_post_check_so	libasteriskssl.so.* libasteriskpj.so.*

%define		_noautoprovfiles	%{_libdir}/asterisk/modules/.*

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

%package utils
Summary:	Various utilities for Asterisk
Summary(pl.UTF-8):	Różne narzędzia dla Asteriska
Group:		Applications/Networking

%description utils
Various utilities built with Asterisk.

%description utils -l pl.UTF-8
Różne narzędzia budowane z Asteriskiem.

%package astman
Summary:	Astman - a text mode Manager for Asterisk
Summary(pl.UTF-8):	Astman - tekstowy zarządca Asteriska
Group:		Applications/Networking

%description astman
Astman is a text mode Manager for Asterisk.

Astman connects to Asterisk by TCP, so you can run Astman on a
completely different computer than your Asterisk computer.

%description astman -l pl.UTF-8
Astman to tekstowy zarządca dla Asteriska.

Łączy się z Asteriskiem po TCP, dzięki czemu można uruchamiać Astmana
na innym komputerze, niż działa Asterisk.

%package alsa
Summary:	Module for Asterisk that uses ALSA sound drivers
Summary(pl.UTF-8):	Moduł Asteriska wykorzystujący sterowniki dźwięku ALSA
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description alsa
Module for Asterisk that uses ALSA sound drivers.

%description alsa -l pl.UTF-8
Moduł Asteriska wykorzystujący sterowniki dźwięku ALSA.

%package bluetooth
Summary:	chan_mobile - Bluetooth mobile phone interface for Asterisk
Summary(pl.UTF-8):	chan_mobile - interfejs telefonów komórkowych Bluetooth dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description bluetooth
The chan_mobile Asterisk module allows one to pair a mobile phone with
the Asterisk PBX via Bluetooth.

%description bluetooth -l pl.UTF-8
Moduł Asteriska chan_mobile pozwala na sparowanie telefonu komórkowego
z centralką Asterisk poprzez Bluetooth.

%package calendar
Summary:	Calendar modules for Asterisk
Summary(pl.UTF-8):	Moduły kalendarza dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description calendar
Calendar modules for Asterisk.

%description calendar -l pl.UTF-8
Moduły kalendarza dla Asteriska.

%package curl
Summary:	Modules for Asterisk that use cURL library
Summary(pl.UTF-8):	Moduły Asteriska wykorzystujące bibliotekę cURL
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description curl
Modules for Asterisk that use cURL library.

%description curl -l pl.UTF-8
Moduły Asteriska wykorzystujące bibliotekę cURL.

%package dahdi
Summary:	Modules for Asterisk that use DAHDI
Summary(pl.UTF-8):	Moduły Asteriska wykorzystujące DAHDI
Group:		Applications/Networking
Requires(pre):	/usr/sbin/usermod
Requires:	%{name} = %{version}-%{release}
Requires:	dahdi-tools >= 2.0.0

%description dahdi
Modules for Asterisk that use DAHDI.

%description dahdi -l pl.UTF-8
Moduły Asteriska wykorzystujące DAHDI.

%package fax
Summary:	FAX applications for Asterisk
Summary(pl.UTF-8):	Aplikacje faksowe dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description fax
FAX applications for Asterisk.

%description fax -l pl.UTF-8
Aplikacje faksowe dla Asteriska.

%package festival
Summary:	Festival application for Asterisk
Summary(pl.UTF-8):	Aplikacja Festival dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	festival

%description festival
Application for the Asterisk PBX that uses Festival to convert text to
speech.

%description festival -l pl.UTF-8
Aplikacja dla centralki Asterisk wykorzystująca bibliotekę Festival do
przekształcenia tekstu na mowę.

%package gsm
Summary:	Support GSM audio encoding/decoding
Summary(pl.UTF-8):	Obsługa kodowania/dekodowania dźwięku GSM
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description gsm
Support GSM audio encoding/decoding.

%description gsm -l pl.UTF-8
Obsługa kodowania/dekodowania dźwięku GSM.

%package http
Summary:	HTTP Server Support
Summary(pl.UTF-8):	Obsługa serwera HTTP
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description http
HTTP Server Support.

%description http -l pl.UTF-8
Obsługa serwera HTTP.

%package ices
Summary:	Stream audio from Asterisk to an IceCast server
Summary(pl.UTF-8):	Przesyłanie strumienia dźwięku z Asteriska do serwera IceCast
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	ices
Obsoletes:	asterisk < 1.4.18-1
Conflicts:	asterisk < 1.4.18-1

%description ices
Stream audio from Asterisk to an IceCast server.

%description ices -l pl.UTF-8
Przesyłanie strumienia dźwięku z Asteriska do serwera IceCast.

%package ilbc
Summary:	iLBC codec for Asterisk
Summary(pl.UTF-8):	Kodek iLBC dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description ilbc
Support iLBC audio encoding/decoding.

%description ilbc -l pl.UTF-8
Obsługa kodowania/dekodowania dźwięku iLBC.

%package jabber
Summary:	Jabber/XMPP resources for Asterisk
Summary(pl.UTF-8):	Zasoby Jabbera/XMPP dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description jabber
Jabber/XMPP resources for Asterisk.

%description jabber -l pl.UTF-8
Zasoby Jabbera/XMPP dla Asteriska.

%package jack
Summary:	JACK resources for Asterisk
Summary(pl.UTF-8):	Zasoby JACK dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description jack
JACK resources for Asterisk.

%description jack -l pl.UTF-8
Zasoby JACK dla Asteriska.

%package lua
Summary:	Lua resources for Asterisk
Summary(pl.UTF-8):	Zasoby Lua dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description lua
Lua resources for Asterisk.

%description lua -l pl.UTF-8
Zasoby Lua dla Asteriska.

%package ldap
Summary:	LDAP resources for Asterisk
Summary(pl.UTF-8):	Zasoby LDAP dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description ldap
LDAP resources for Asterisk.

%description ldap -l pl.UTF-8
Zasoby LDAP dla Asteriska.

%package ldap-fds
Summary:	LDAP resources for Asterisk and the Fedora Directory Server
Summary(pl.UTF-8):	Zasoby LDAP dla Asteriska oraz serwera usług katalogowych Fedora Directory Server
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-ldap = %{version}-%{release}
Requires:	fedora-ds-base

%description ldap-fds
LDAP resources for Asterisk and the Fedora Directory Server.

%description ldap-fds -l pl.UTF-8
Zasoby LDAP dla Asteriska oraz serwera usług katalogowych Fedora
Directory Server.

%package lpc10
Summary:	LPC-10 2400 bps Voice Codec support
Summary(pl.UTF-8):	Obsługa kodeka głosu LPC-10 2400 bps
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description lpc10
LPC-10 2400 bps Voice Codec support

%description lpc10 -l pl.UTF-8
Obsługa kodeka głosu LPC-10 2400 bps.

%package minivm
Summary:	MiniVM application for Asterisk
Summary(pl.UTF-8):	Aplikacja MiniVM dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description minivm
MiniVM application for Asterisk.

%description minivm -l pl.UTF-8
Aplikacja MiniVM dla Asteriska.

%package mysql
Summary:	Asterisk modules that use MySQL
Summary(pl.UTF-8):	Moduły Asteriska wykorzystujące MySQL
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description mysql
Asterisk modules that use MySQL.

%description mysql -l pl.UTF-8
Moduły Asteriska wykorzystujące MySQL.

%package odbc
Summary:	Applications for Asterisk that use ODBC (except voicemail)
Summary(pl.UTF-8):	Aplikacje Asteriska wykorzystujące ODBC (z wyjątkiem voicemail)
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description odbc
Applications for Asterisk that use ODBC (except voicemail).

%description odbc -l pl.UTF-8
Aplikacje Asteriska wykorzystujące ODBC (z wyjątkiem voicemail).

%package osp
Summary:	Module for Asterisk that uses Open Settlement Protocol (OSP) Applications
Summary(pl.UTF-8):	Moduł Asteriska wykorzystujący aplikacje OSP (Open Settlement Protocol)
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description osp
Open Settlement Protocol (OSP) Applications.

%description osp -l pl.UTF-8
Aplikacje protokołu OSP (Open Settlement Protocol).

%package oss
Summary:	Module for Asterisk that uses OSS sound drivers
Summary(pl.UTF-8):	Moduł Asteriska wykorzystujący sterowniki dźwięku OSS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description oss
Module for Asterisk that uses OSS sound drivers.

%description oss -l pl.UTF-8
Moduł Asteriska wykorzystujący sterowniki dźwięku OSS.

%package portaudio
Summary:	Module for Asterisk that uses the PortAudio library
Summary(pl.UTF-8):	Moduł Asteriska wykorzystujący bibliotekę PortAudio
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description portaudio
Module for Asterisk that uses the PortAudio library.

%description portaudio -l pl.UTF-8
Moduł Asteriska wykorzystującye bibliotekę PortAudio.

%package postgresql
Summary:	Applications for Asterisk that use PostgreSQL
Summary(pl.UTF-8):	Aplikacje Asteriska wykorzystujące PostgreSQL
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description postgresql
Applications for Asterisk that use PostgreSQL.

%description postgresql -l pl.UTF-8
Aplikacje Asteriska wykorzystujące PostgreSQL.

%package radius
Summary:	Applications for Asterisk that use RADIUS
Summary(pl.UTF-8):	Aplikacje Asteriska wykorzystujące bibliotekę RADIUS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description radius
Applications for Asterisk that use RADIUS.

%description radius -l pl.UTF-8
Aplikacje Asteriska wykorzystujące bibliotekę RADIUS.

%package resample
Summary:	resample codec
Summary(pl.UTF-8):	Kodek resample
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description resample
resample codec.

%description resample -l pl.UTF-8
Kodek resample.

%package skinny
Summary:	Module for Asterisk that supportsthe SCCP/Skinny protocol
Summary(pl.UTF-8):	Moduł Asteriska obsługujący protokół SCCP/Skinny
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description skinny
Module for Asterisk that supports the SCCP/Skinny protocol.

%description skinny -l pl.UTF-8
Moduł Asteriska obsługujący protokół SCCP/Skinny.

%package snmp
Summary:	Module that enables SNMP monitoring of Asterisk
Summary(pl.UTF-8):	Moduł pozwalający na monitorowanie Asteriska przez SNMP
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	mibs-dirs

%description snmp
Module that enables SNMP monitoring of Asterisk.

%description snmp -l pl.UTF-8
Moduł pozwalający na monitorowanie Asteriska przez SNMP.

%package speex
Summary:	Speex codec support
Summary(pl.UTF-8):	Obsługa kodeka Speex
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description speex
Speex codec support.

%description speex -l pl.UTF-8
Obsługa kodeka Speex.

%package sqlite2
Summary:	SQLite 2 module for Asterisk
Summary(pl.UTF-8):	Moduł SQLite 2 dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description sqlite2
SQLite 2 module for Asterisk.

%description sqlite2 -l pl.UTF-8
Moduł SQLite 2 dla Asteriska.

%package sqlite3
Summary:	SQLite 3 modules for Asterisk
Summary(pl.UTF-8):	Moduły SQLite 3 dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Obsoletes:	asterisk-sqlite < 12.0.0

%description sqlite3
SQLite 3 modules for Asterisk.

%description sqlite3 -l pl.UTF-8
Moduły SQLite 3 dla Asteriska.

%package tds
Summary:	Modules for Asterisk that use FreeTDS
Summary(pl.UTF-8):	Moduły Asteriska wykorzystujące FreeTDS
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description tds
Modules for Asterisk that use FreeTDS.

%description tds -l pl.UTF-8
Moduły Asteriska wykorzystujące FreeTDS.

%package unistim
Summary:	Unistim channel for Asterisk
Summary(pl.UTF-8):	Kanał Unistim dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description unistim
Unistim channel for Asterisk

%description unistim -l pl.UTF-8
Kanał Unistim dla Asteriska.

%package voicemail
Summary:	Common Voicemail Modules for Asterisk
Summary(pl.UTF-8):	Wspólne moduły Voicemail (poczty głosowej) dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-voicemail-implementation = %{version}-%{release}
Requires:	/usr/lib/sendmail
Requires:	sox

%description voicemail
Common Voicemail Modules for Asterisk.

%description voicemail -l pl.UTF-8
Wspólne moduły Voicemail (poczty głosowej) dla Asteriska.

%package voicemail-imap
Summary:	Store voicemail on an IMAP server
Summary(pl.UTF-8):	Przechowywanie poczty głosowej na serwerze IMAP
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-voicemail = %{version}-%{release}
Provides:	%{name}-voicemail-implementation = %{version}-%{release}

%description voicemail-imap
Voicemail implementation for Asterisk that stores voicemail on an IMAP
server.

%description voicemail-imap -l pl.UTF-8
Implementacja poczty głosowej (Voicemail) dla Asteriska przechowująca
pocztę na serwerze IMAP.

%package voicemail-odbc
Summary:	Store voicemail in a database using ODBC
Summary(pl.UTF-8):	Przechowywanie poczty głosowej w bazie danych poprzez ODBC
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-voicemail = %{version}-%{release}
Provides:	%{name}-voicemail-implementation = %{version}-%{release}

%description voicemail-odbc
Voicemail implementation for Asterisk that uses ODBC to store
voicemail in a database.

%description voicemail-odbc -l pl.UTF-8
Implementacja poczty głosowej (Voicemail) dla Asteriska wykorzystująca
ODBC do przechowywania poczty w bazie danych.

%package voicemail-plain
Summary:	Store voicemail on the local filesystem
Summary(pl.UTF-8):	Przechowywanie poczty głosowej na lokalnym systemie plików
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-voicemail = %{version}-%{release}
Provides:	%{name}-voicemail-implementation = %{version}-%{release}

%description voicemail-plain
Voicemail implementation for Asterisk that stores voicemail on the
local filesystem.

%description voicemail-plain -l pl.UTF-8
Implementacja poczty głosowej (Voicemail) dla Asteriska przechowująca
pocztę na lokalnym systemie plików.

%package vorbis
Summary:	Ogg Vorbis format support
Summary(pl.UTF-8):	Obsługa formatu Ogg Vorbis
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description vorbis
Ogg Vorbis format support.

%description vorbis -l pl.UTF-8
Obsługa formatu Ogg Vorbis.

%package opus
Summary:	Opus codec and file format support
Summary(pl.UTF-8):	Obsługa kodeka i formatu plików Opus
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description opus
Opus codec and file format support.

%description opus -l pl.UTF-8
Obsługa kodeka i formatu plików Opus.

%package debug-tools
Summary:	Debugging scripts for Asterisk
Summary(pl.UTF-8):	Skrypty diagnostyczne dla Asteriska
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description debug-tools
Debugging scripts for Asterisk.

%description debug-tools -l pl.UTF-8
Skrypty diagnostyczne dla Asteriska.

# define apidocs as last package, as it is the biggest one
%package apidocs
Summary:	API documentation for Asterisk
Summary(pl.UTF-8):	Dokumentacja API Asteriska
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Asterisk.

%description apidocs -l pl.UTF-8
Dokumentacja API Asteriska.

%prep
%setup -q -a 8
%patch0 -p1

%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%if %{with opus_vp8}

cp -a asterisk-opus-%{opus_commit}/codecs/* codecs
cp -a asterisk-opus-%{opus_commit}/formats/* formats
cp -a asterisk-opus-%{opus_commit}/res/* rest
cp -a asterisk-opus-%{opus_commit}/include/asterisk/* include/asterisk
%endif

%if %{without system_pjproject} && %{with pjsip}
mkdir externals
ln -s %{SOURCE9} externals
md5sum %{SOURCE9} > externals/pjproject-%{pjproject_version}.md5
%endif

# Fixup makefile so sound archives aren't downloaded/installed
%{__sed} -i -e 's/^all:.*$/all:/' sounds/Makefile
%{__sed} -i -e 's/^install:.*$/install:/' sounds/Makefile

%build
%{__aclocal} -I autoconf $(find third-party/ -maxdepth 1 -type d -printf "-I %p ")
%{__autoheader}
%{__autoconf}

export ASTCFLAGS="%{rpmcflags}"
export ASTLDFLAGS="%{rpmldflags}"
export WGET="/bin/true"

%if %{without system_pjproject} && %{with pjsip}
export EXTERNALS_CACHE_DIR="$PWD/externals"
export PJPROJECT_CONFIGURE_OPTS="--disable-bcg729"
%endif

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
	ac_cv_header_stdc=yes \
	%{__without_if system_pjproject pjproject-bundled} \
	--without-jansson-bundled \
	--with-unbound \
	%{__without oss SDL_image} \
	%{__without bluetooth bluetooth} \
	--without-gtk2 \
	--with-gnu-ld \
	--with-gsm=/usr \
	%{__without ilbc ilbc} \
	--with-imap=system \
	%{__without jack jack} \
	%{__without ldap ldap} \
	--with-lpc10=/usr \
	%{__without mysql mysqlclient} \
	%{__without oss oss} \
	%{__without pjsip pjproject} \
	%{__without portaudio portaudio} \
	%{__without pgsql postgres} \
	%{__without radius radius} \
	%{__without oss sdl} \
	%{__without tds tds} \
	%{__without odbc unixodbc}

cp -f .cleancount .lastclean

%{__make} menuselect/menuselect
%{__make} menuselect-tree

cp %{SOURCE6} .
cp %{SOURCE7} .

%if %{without corosync}
menuselect/menuselect --disable res_corosync menuselect.makeopts
%endif
%if %{without sqlite2}
menuselect/menuselect --disable res_config_sqlite menuselect.makeopts
%endif
%if %{without oss}
menuselect/menuselect --disable chan_oss menuselect.makeopts
%endif
%if %{without tds}
menuselect/menuselect --disable cdr_tds --disable cel_tds menuselect.makeopts
%endif
%if %{without ilbc}
menuselect/menuselect --disable codec_ilbc --disable format_ilbc menuselect.makeopts
%endif
%if %{without ldap}
menuselect/menuselect --disable res_config_ldap menuselect.makeopts
%endif
%if %{without bluetooth}
menuselect/menuselect --disable chan_mobile menuselect.makeopts
%endif
%if %{without jack}
menuselect/menuselect --disable app_jack menuselect.makeopts
%endif
%if %{without mysql}
menuselect/menuselect --disable res_config_mysql --disable app_mysql --disable cdr_mysql menuselect.makeopts
%endif
%if %{without pgsql}
menuselect/menuselect --disable res_config_pgsql --disable cdr_pgsql --disable cel_pgsql menuselect.makeopts
%endif
%if %{without odbc}
menuselect/menuselect --disable res_odbc --disable res_config_odbc --disable cdr_odbc --disable cdr_adaptive_odbc --disable cel_odbc menuselect.makeopts
%endif
%if %{without radius}
menuselect/menuselect --disable cdr_radius --disable cel_radius menuselect.makeopts
%endif
%if %{without pjsip}
menuselect/menuselect --disable res_pjsip --disable chan_pjsip menuselect.makeopts
%endif
%if %{without opus_vp8}
menuselect/menuselect --disable codec_opus_open_source --disable format_ogg_opus_open_source menuselect.makeopts
%endif

%if %{with malloc_debug}
menuselect/menuselect --enable MALLOC_DEBUG menuselect.makeopts
%else
menuselect/menuselect --disable MALLOC_DEBUG menuselect.makeopts
%endif

%{__sed} -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=FILE_STORAGE/' menuselect.makeopts

menuselect/menuselect --enable app_voicemail menuselect.makeopts

menuselect/menuselect --check-deps menuselect.makeopts

# workaround for build failing with asterisk-devel not installed
ln -s libasteriskssl.so.1 ./main/libasteriskssl.so

%{__make} DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \

%{__rm} apps/app_voicemail.o
%{__mv} apps/app_voicemail.so apps/app_voicemail_plain.so

%{__sed} -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=IMAP_STORAGE/' menuselect.makeopts
%{__make} DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \

%{__rm} apps/app_voicemail.o
%{__mv} apps/app_voicemail.so apps/app_voicemail_imap.so

%if %{with odbc}
%{__sed} -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=ODBC_STORAGE/' menuselect.makeopts
%{__make} DEBUG= \
	OPTIMIZE= \
	ASTVARRUNDIR=%{_localstatedir}/run/asterisk \
	ASTDATADIR=%{_datadir}/asterisk \
	ASTVARLIBDIR=%{_datadir}/asterisk \
	ASTDBDIR=%{_localstatedir}/spool/asterisk \
	%{?with_verbose:NOISY_BUILD=yes} \

%{__rm} apps/app_voicemail.o
%{__mv} apps/app_voicemail.so apps/app_voicemail_odbc.so
%endif

# so that these modules don't get built again during the install phase
touch apps/app_voicemail.o
touch apps/app_voicemail.so

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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/{log/asterisk/cdr-csv,spool/asterisk/monitor},/etc/{rc.d/init.d,sysconfig,logrotate.d}} \
	$RPM_BUILD_ROOT{%{systemdunitdir},%{systemdtmpfilesdir},%{_mandir}/man1}

export ASTCFLAGS="%{rpmcflags}"

%{__make} -j1 install install-headers \
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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/asterisk/modules/app_voicemail.so
install -D -p apps/app_voicemail_imap.so $RPM_BUILD_ROOT%{_libdir}/asterisk/modules
%if %{with odbc}
install -D -p apps/app_voicemail_odbc.so $RPM_BUILD_ROOT%{_libdir}/asterisk/modules
%endif
install -D -p apps/app_voicemail_plain.so $RPM_BUILD_ROOT%{_libdir}/asterisk/modules

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -a %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

install %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

# create some directories that need to be packaged
install -d $RPM_BUILD_ROOT%{_datadir}/asterisk/moh
install -d $RPM_BUILD_ROOT%{_datadir}/asterisk/sounds
ln -s %{_localstatedir}/lib/asterisk/licenses $RPM_BUILD_ROOT%{_datadir}/asterisk/licenses

install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/asterisk/licenses
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/archive/asterisk
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/asterisk/cdr-custom
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/festival
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/monitor
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/outgoing
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/uploads

install utils/astman.1 $RPM_BUILD_ROOT%{_mandir}/man1/astman.1

# Don't package the sample voicemail user
%{__rm} -r $RPM_BUILD_ROOT%{_localstatedir}/spool/asterisk/voicemail/default

# Don't package example phone provision configs
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/asterisk/phoneprov/*

# we're not using safe_asterisk
%{__rm} $RPM_BUILD_ROOT%{_sbindir}/safe_asterisk
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/safe_asterisk.8*

%if %{with apidocs}
find doc/api -name '*.map' -size 0 -delete
%endif

# remove configuration files for components never built
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/{app_skel,config_test,misdn,ooh323,test_sorcery}.conf

# remove configuration files for disabled optional components
%if %{without corosync}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/res_corosync.conf
%endif
%if %{without sqlite2}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/res_config_sqlite.conf
%endif
%if %{without oss}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/oss.conf
%endif
%if %{without tds}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/{cdr,cel}_tds.conf
%endif
%if %{without ldap}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/res_ldap.conf
%endif
%if %{without portaudio}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/console.conf
%endif
%if %{without bluetooth}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/chan_mobile.conf
%endif
%if %{without mysql}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/res_config_mysql.conf
%endif
%if %{without pgsql}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/{cdr,cel,res}_pgsql.conf
%endif
%if %{without odbc}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/{cdr{,_adaptive},cel,func,res}_odbc.conf
%endif
%if %{without pjsip}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/asterisk/pjsip{,_notify}.conf
%endif

%{__rm} -r $RPM_BUILD_ROOT/usr/include/asterisk/doxygen

# fix script interpreters
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' $RPM_BUILD_ROOT%{_datadir}/asterisk/scripts/*
%{__sed} -i -e '1s,^#!.*bash,#!/bin/bash,' $RPM_BUILD_ROOT%{_datadir}/asterisk/scripts/*

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
%systemd_reload

%post
/sbin/ldconfig
/sbin/chkconfig --add asterisk
# use -n (NOOP) as restart would be breaking all current calls.
%service -n asterisk restart "Asterisk daemon"
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service asterisk stop
	/sbin/chkconfig --del asterisk
fi
%systemd_preun %{name}.service

%triggerpostun -- %{name} < 1.6.1.12-0.1
# chown to asterisk previously root owned files
# loose one (not one that cames from rpm), as we're not trying to split the
# hair with file permission bits.
chown -R asterisk:asterisk /var/spool/asterisk
chown -R asterisk:asterisk /var/lib/asterisk

%triggerpostun -- %{name} < 12.0.0
%systemd_trigger %{name}.service

%files
%defattr(644,root,root,755)
%doc README*.md *.txt ChangeLogs/*-%{version}.md CHANGES.md BUGS CREDITS configs LICENSE
%doc doc/asterisk.sgml

%attr(755,root,root) %{_sbindir}/astcanary
%attr(755,root,root) %{_sbindir}/astdb2bdb
%attr(755,root,root) %{_sbindir}/astdb2sqlite3
%attr(755,root,root) %{_sbindir}/asterisk
%attr(755,root,root) %{_sbindir}/astgenkey
%attr(755,root,root) %{_sbindir}/astversion
%attr(755,root,root) %{_sbindir}/autosupport
%attr(755,root,root) %{_sbindir}/rasterisk
%{_mandir}/man8/astdb2bdb.8*
%{_mandir}/man8/astdb2sqlite3.8*
%{_mandir}/man8/asterisk.8*
%{_mandir}/man8/astgenkey.8*
%{_mandir}/man8/autosupport.8*

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdunitdir}/%{name}.service

%attr(750,root,asterisk) %dir %{_sysconfdir}/asterisk
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/acl.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/adsi.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/aeap.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/agents.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/alarmreceiver.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/amd.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/ari.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/asterisk.adsi
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/asterisk.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/ccss.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_custom.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_beanstalkd.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_manager.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_syslog.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_beanstalkd.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_custom.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cli.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cli_aliases.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cli_permissions.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/codecs.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/confbridge.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/dnsmgr.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/dsp.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/dundi.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/enum.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extconfig.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions.ael
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/features.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/followme.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/geolocation.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/hep.conf
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
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/pjproject.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/pjsip.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/pjsip_notify.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/pjsip_wizard.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/queuerules.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/queues.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/prometheus.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/resolver_unbound.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_http_media_cache.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_parking.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_pktccops.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_stun_monitor.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/rtp.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/say.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/sip*.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/sla.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/smdi.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/sorcery.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/ss7.timers
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/stasis.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/statsd.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/stir_shaken.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/telcordia-1.adsi
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/udptl.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/users.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/vpb.conf

%attr(755,root,root) %{_libdir}/libasteriskssl.so.1
%if %{without system_pjproject} && %{with pjsip}
%attr(755,root,root) %{_libdir}/libasteriskpj.so.2
%endif

%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules

%attr(755,root,root) %{_libdir}/asterisk/modules/app_adsiprog.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_agent_pool.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_alarmreceiver.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_amd.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_attended_transfer.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_audiosocket.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_authenticate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_blind_transfer.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_bridgeaddchan.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_bridgewait.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_broadcast.so
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
%attr(755,root,root) %{_libdir}/asterisk/modules/app_directory.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_disa.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_dtmfstore.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_dumpchan.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_echo.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_exec.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_externalivr.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_followme.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_forkcdr.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_getcpeid.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_if.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_image.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_macro.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_milliwatt.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_mixmonitor.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_mf.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_morsecode.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_mp3.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_nbscat.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_originate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_playback.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_playtones.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_privacy.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_queue.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_read.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_readexten.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_record.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_reload.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_saycounted.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_sayunixtime.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_senddtmf.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_sendtext.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_sf.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_signal.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_sms.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_softhangup.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_speech_utils.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_stack.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_stasis.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_statsd.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_stream_echo.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_system.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_talkdetect.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_test.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_transfer.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_url.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_userevent.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_verbose.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_waitforcond.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_waitforring.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_waitforsilence.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_waituntil.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_while.so
%attr(755,root,root) %{_libdir}/asterisk/modules/app_zapateller.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_builtin_features.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_builtin_interval_features.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_holding.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_native_rtp.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_simple.so
%attr(755,root,root) %{_libdir}/asterisk/modules/bridge_softmix.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_csv.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_custom.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_manager.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_syslog.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_custom.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_manager.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_audiosocket.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_bridge_media.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_iax2.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_mgcp.so
#%attr(755,root,root) %{_libdir}/asterisk/modules/chan_phone.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_pjsip.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_rtp.so
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_sip.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_a_mu.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_adpcm.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_alaw.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_codec2.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_g722.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_g726.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_ulaw.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_g719.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_g723.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_g726.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_g729.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_h263.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_h264.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_pcm.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_siren14.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_siren7.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_sln.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_vox.so
%if %{with opus_vp8}
%attr(755,root,root) %{_libdir}/asterisk/modules/format_vp8.so
%endif
%attr(755,root,root) %{_libdir}/asterisk/modules/format_wav.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_aes.so
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
%attr(755,root,root) %{_libdir}/asterisk/modules/func_evalexten.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_export.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_extstate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_frame_drop.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_frame_trace.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_global.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_groupcount.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_hangupcause.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_holdintercept.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_iconv.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_jitterbuffer.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_json.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_lock.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_logic.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_math.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_md5.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_module.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_periodic_hook.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_pitchshift.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_aoc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_rfc3329.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_pjsip_aor.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_pjsip_contact.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_pjsip_endpoint.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_presencestate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_rand.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_realtime.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_sayfiles.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_scramble.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_sha1.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_shell.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_sorcery.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_sprintf.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_srv.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_strings.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_sysinfo.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_talkdetect.so
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
%attr(755,root,root) %{_libdir}/asterisk/modules/res_aeap.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ael_share.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_agi.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_applications.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_asterisk.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_bridges.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_channels.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_device_states.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_endpoints.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_events.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_model.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_playbacks.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_recordings.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_ari_sounds.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_audiosocket.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_chan_stats.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_clialiases.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_cliexec.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_clioriginate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_convert.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_crypto.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_endpoint_stats.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_celt.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_g729.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_h263.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_h264.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_opus.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_silk.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_siren14.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_siren7.so
%if %{with opus_vp8}
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_vp8.so
%endif
%attr(755,root,root) %{_libdir}/asterisk/modules/res_geolocation.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_hep.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_hep_pjsip.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_hep_rtcp.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_http_media_cache.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_http_websocket.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_limit.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_manager_devicestate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_manager_presencestate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_monitor.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_mutestream.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_musiconhold.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_mwi_devstate.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_mwi_external.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_mwi_external_ami.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_parking.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_phoneprov.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjproject.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_acl.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_authenticator_digest.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_caller_id.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_config_wizard.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_dialog_info_body_generator.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_diversion.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_dlg_options.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_dtmf_info.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_empty_info.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_anonymous.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_ip.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_user.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_exten_state.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_geolocation.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_header_funcs.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_history.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_logger.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_messaging.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_mwi_body_generator.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_mwi.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_nat.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_notify.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_one_touch_record_info.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_outbound_authenticator_digest.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_outbound_publish.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_outbound_registration.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_path.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_phoneprov_provider.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_pidf_body_generator.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_pidf_digium_body_supplement.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_pidf_eyebeam_body_supplement.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_publish_asterisk.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_pubsub.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_refer.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_registrar.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_rfc3326.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_sdp_rtp.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_send_to_voicemail.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_session.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_sips_contact.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_t38.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_transport_websocket.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pjsip_xpidf_body_generator.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_pktccops.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_prometheus.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_realtime.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_remb_modifier.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_resolver_unbound.so
# res_rtp_asterisk.so pulls some pjproject libs, but it still looks like a core module
%attr(755,root,root) %{_libdir}/asterisk/modules/res_rtp_asterisk.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_rtp_multicast.so
#%attr(755,root,root) %{_libdir}/asterisk/modules/res_sdp_translator_pjmedia.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_security_log.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_smdi.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_sorcery_astdb.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_sorcery_config.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_sorcery_memory.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_sorcery_memory_cache.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_sorcery_realtime.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_speech.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_speech_aeap.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_srtp.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_stasis.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_stasis_answer.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_stasis_device_state.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_stasis_playback.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_stasis_recording.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_stasis_snoop.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_stun_monitor.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_timing_pthread.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_timing_timerfd.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_statsd.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_tonedetect.so
%{systemdtmpfilesdir}/%{name}.conf

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
%{_datadir}/asterisk/documentation/appdocsxml.xslt
%{_datadir}/asterisk/documentation/core-en_US.xml

%dir %{_datadir}/asterisk/rest-api
%{_datadir}/asterisk/rest-api/*.json

%dir %{_datadir}/asterisk/scripts

%attr(770,root,asterisk) %dir %{_localstatedir}/lib/asterisk
%dir %attr(750,root,asterisk) %{_localstatedir}/lib/asterisk/licenses

%attr(750,root,logs) %dir %{_localstatedir}/log/archive/asterisk
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
%attr(755,root,root) %{_libdir}/libasteriskssl.so
%if %{without system_pjproject} && %{with pjsip}
%attr(755,root,root) %{_libdir}/libasteriskpj.so
%endif
%dir %{_includedir}/asterisk
%{_includedir}/asterisk/*.h
%{_includedir}/asterisk.h

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/api/*
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/aelparse
%attr(755,root,root) %{_sbindir}/conf2ael
%attr(755,root,root) %{_sbindir}/muted
%attr(755,root,root) %{_sbindir}/smsq
%attr(755,root,root) %{_sbindir}/stereorize
%attr(755,root,root) %{_sbindir}/streamplayer

%files astman
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/astman
%{_mandir}/man1/astman.1*

%files alsa
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/alsa.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_alsa.so

%if %{with bluetooth}
%files bluetooth
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/chan_mobile.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_mobile.so
%endif

%files calendar
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/calendar.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar_caldav.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar_ews.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar_exchange.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_calendar_icalendar.so

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
%{_datadir}/dahdi/span_config.d/40-asterisk
%attr(755,root,root) %{_libdir}/asterisk/modules/app_dahdiras.so
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

%files http
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/http.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/res_http_post.so
%{_datadir}/asterisk/static-http

%files ices
%defattr(644,root,root,755)
%doc contrib/asterisk-ices.xml
%attr(755,root,root) %{_libdir}/asterisk/modules/app_ices.so

%if %{with ilbc}
%files ilbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_ilbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/format_ilbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_format_attr_ilbc.so
%endif

%files jabber
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/motif.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/xmpp.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_motif.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_xmpp.so

%if %{with jack}
%files jack
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/app_jack.so
%endif

%files lua
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions.lua
%attr(755,root,root) %{_libdir}/asterisk/modules/pbx_lua.so

%if %{with ldap}
%files ldap
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_ldap.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_ldap.so

%if 0
%files ldap-fds
%defattr(644,root,root,755)
%{_sysconfdir}/dirsrv/schema/99asterisk.ldif
%endif
%endif

%files lpc10
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_lpc10.so

%files minivm
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/extensions_minivm.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/minivm.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/app_minivm.so

%if %{with mysql}
%files mysql
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/app_mysql.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_mysql.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_config_mysql.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/app_mysql.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_mysql.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_mysql.so
%endif

%if %{with odbc}
%files odbc
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_adaptive_odbc.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_odbc.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_odbc.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/func_odbc.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_config_odbc.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_odbc.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_adaptive_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_odbc.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_odbc_transaction.so
%endif

%if %{with opus_vp8}
%files opus
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/format_ogg_opus_open_source.so
%attr(755,root,root) %{_libdir}/asterisk/modules/codec_opus_open_source.so
%endif

%files osp
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/osp.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/app_osplookup.so

%if %{with oss}
%files oss
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/oss.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_oss.so
%endif

%if %{with portaudio}
%files portaudio
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/console.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/chan_console.so
%endif

%if %{with pgsql}
%files postgresql
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_pgsql.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_pgsql.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_pgsql.conf
%doc contrib/realtime/postgresql/postgresql_cdr.sql
%doc contrib/realtime/postgresql/postgresql_config.sql
%doc contrib/realtime/postgresql/postgresql_voicemail.sql
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_pgsql.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_pgsql.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_pgsql.so
%endif

%if %{with radius}
%files radius
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_radius.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_radius.so
%endif

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
%attr(755,root,root) %{_libdir}/asterisk/modules/format_ogg_speex.so
%attr(755,root,root) %{_libdir}/asterisk/modules/func_speex.so

%if %{with sqlite2}
%files sqlite2
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_config_sqlite.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_sqlite.so
%endif

%files sqlite3
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_sqlite3_custom.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_sqlite3_custom.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/res_config_sqlite3.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_sqlite3_custom.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_sqlite3_custom.so
%attr(755,root,root) %{_libdir}/asterisk/modules/res_config_sqlite3.so

%if %{with tds}
%files tds
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cdr_tds.conf
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/cel_tds.conf
%attr(755,root,root) %{_libdir}/asterisk/modules/cdr_tds.so
%attr(755,root,root) %{_libdir}/asterisk/modules/cel_tds.so
%endif

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
%attr(755,root,root) %{_libdir}/asterisk/modules/app_voicemail_imap.so

%if %{with odbc}
%files voicemail-odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/app_voicemail_odbc.so
%endif

%files voicemail-plain
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/app_voicemail_plain.so

%files vorbis
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/asterisk/modules/format_ogg_vorbis.so

%files debug-tools
%defattr(644,root,root,755)
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asterisk/ast_debug_tools.conf
%attr(755,root,root) %{_datadir}/asterisk/scripts/ast_coredumper
%attr(755,root,root) %{_datadir}/asterisk/scripts/ast_logescalator
%attr(755,root,root) %{_datadir}/asterisk/scripts/ast_loggrabber
%attr(755,root,root) %{_datadir}/asterisk/scripts/refcounter.py
%attr(755,root,root) %{_datadir}/asterisk/scripts/reflocks.py
%attr(755,root,root) %{_datadir}/asterisk/scripts/refstats.py
