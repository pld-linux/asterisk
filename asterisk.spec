# TODO:
# - cgi-bin package - separate, because of suid-root
# - separate plugins into packages
# - use shared versions of lpc10, gsm,...
# - put chan_h323 into separate package and make obsoletes to chan_oh323 from external spec
#   These two h323 plugin are conflicting...
# - CFLAGS passing
#
# Conditional build:
%bcond_without	openh323	# without OpenH323 support
#
Summary:	Asterisk PBX
Summary(pl):	Centralka (PBX) Asterisk
Name:		asterisk
Version:	1.0.9
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.digium.com/pub/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	0d7f1c680ae53a739f26a069ef8b580a
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-openh323-makefile.patch
Patch1:		%{name}-Makefile_fix_gcc33.patch
Patch2:		%{name}-no_k6_on_sparc.patch
Patch3:		%{name}-lib.patch
Patch4:		%{name}-openh323-formats.patch
Patch5:		%{name}-openh323-rtti.patch
Patch6:		%{name}-freetds.patch
# It's included, but these sources are broken by me :)
# will fit on clean cvs source
#Patch1:		%{name}-DESTDIR.patch
#Patch2:		%{name}-Makefile2.patch
URL:		http://www.asterisk.org/
BuildRequires:	bison
BuildRequires:	freetds >= 0.63
BuildRequires:	gawk
#BuildRequires:	glib-devel
#BuildRequires:	gtk+-devel
BuildRequires:	libpri-devel
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	sed >= 4.0
BuildRequires:	speex-devel
BuildRequires:	zaptel-devel
BuildRequires:	zlib-devel
#BuildRequires:	mpg123
# These libraries are crazy...
# With openh323 1.11.7 and pwlib 1.4.11 i had sig11
#BuildRequires:	openh323-devel = 1.10.4
#BuildRequires:	pwlib-devel = 1.4.4
%{?with_openh323:BuildRequires:	openh323-devel}
%{?with_openh323:BuildRequires:	pwlib-devel}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
%{?with_openh323:%requires_eq	openh323}
%{?with_openh323:%requires_eq	pwlib}
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

%description -l pl
Asterisk to wolnodostêpna centralka (PBX) i platforma programistyczna
dla telefonii, mog±ca zast±piæ konwencjonalne PBX-y oraz s³u¿yæ jako
platforma do rozwijania w³asnych aplikacji telefonicznych do
przekazywania dynamicznej tre¶ci przez telefon, podobnie jak mo¿na
przekazywaæ dynamiczn± tre¶æ przez przegl±darkê WWW przy u¿yciu CGI i
serwera WWW.

Asterisk wspó³pracuje z wielorakim sprzêtem telefonicznym, w tym BRI,
PRI, POTS oraz klienty telefonii IP u¿ywaj±ce protoko³u Inter-Asterisk
eXchange (np. gnophone lub miniphone). Wiêcej informacji i listê
obs³ugiwanego sprzêtu mo¿na znale¼æ pod http://www.asterisk.org/.

%package devel
Summary:	Header files for Asterisk platform
Summary(pl):	Pliki nag³ówkowe platformy Asterisk
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Asterisk development platform.

%description devel -l pl
Pliki nag³ówkowe platformy programistycznej Asterisk.

%package examples
Summary:	Example files for the Asterisk PBX
Summary(pl):	Pliki przyk³adowe dla centralki Asterisk
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description examples
Example files for the Asterisk PBX.

%description examples -l pl
Pliki przyk³adowe dla centralki Asterisk.

%prep
%setup -q
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

sed -i -e "s#/usr/lib/#/usr/%{_lib}/#g#" Makefile

%build
rm -f pbx/.depend
%{__make} -j1 \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%if %{with openh323}
# H323 plugin:
%{__make} -j1 -C channels/h323 \
	PWLIBDIR="%{_prefix}" \
	OPENH323DIR="%{_prefix}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/openh323 -fPIC -I../../include"

%endif

# it requires doxygen - I don't know if we should do this...
#%{__make} progdocs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/{log/asterisk/cdr-csv,spool/asterisk/monitor},/etc/{rc.d/init.d,sysconfig}}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT 
%{__make} -j1 samples \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%if %{with openh323}
install channels/h323/h323.conf.sample $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/h323.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add asterisk
if [ -f /var/lock/subsys/asterisk ]; then
	/etc/rc.d/init.d/asterisk restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/asterisk start\" to start Asterisk daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/asterisk ]; then
		/etc/rc.d/init.d/asterisk stop 1>&2
	fi
	/sbin/chkconfig --del asterisk
fi

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog CREDITS HARDWARE README* SECURITY configs doc/{*.txt,linkedlists.README}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/asterisk
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/asterisk/*.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/asterisk/*.adsi
%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules
%attr(755,root,root) %{_libdir}/asterisk/modules/*.so
%dir /var/lib/asterisk
%dir /var/lib/asterisk/agi-bin
%dir /var/lib/asterisk/images
%dir /var/lib/asterisk/keys
%dir /var/lib/asterisk/mohmp3
/var/lib/asterisk/mohmp3/fpm-calm-river.mp3
/var/lib/asterisk/mohmp3/fpm-sunshine.mp3
/var/lib/asterisk/mohmp3/fpm-world-mix.mp3
%dir /var/lib/asterisk/sounds
%dir /var/lib/asterisk/sounds/digits
%dir /var/lib/asterisk/sounds/letters
%dir /var/lib/asterisk/sounds/phonetic
/var/lib/asterisk/images/*.jpg
/var/lib/asterisk/keys/*.pub
/var/lib/asterisk/sounds/*.gsm
/var/lib/asterisk/sounds/digits/*.gsm
/var/lib/asterisk/sounds/letters/*.gsm
/var/lib/asterisk/sounds/phonetic/*.gsm
%dir /var/spool/asterisk
%dir /var/spool/asterisk/monitor
%dir /var/spool/asterisk/vm
%dir /var/spool/asterisk/voicemail
%dir /var/spool/asterisk/voicemail/default
%dir /var/log/asterisk
%dir /var/log/asterisk/cdr-csv
%{_mandir}/man8/asterisk.8*
%dir /var/lib/asterisk/firmware
%dir /var/lib/asterisk/firmware/iax
/var/lib/asterisk/firmware/iax/iaxy.bin

%files examples
%defattr(644,root,root,755)
%attr(755,root,root) /var/lib/asterisk/agi-bin/agi-test.agi
%attr(755,root,root) /var/lib/asterisk/agi-bin/eagi-sphinx-test
%attr(755,root,root) /var/lib/asterisk/agi-bin/eagi-test
/var/spool/asterisk/voicemail/default/1234/busy.gsm
/var/spool/asterisk/voicemail/default/1234/unavail.gsm

# RedHat specific init script file
#%attr(754,root,root) /etc/rc.d/init.d/asterisk
#%dir /var/lib/asterisk/agi-bin/*

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/asterisk
%{_includedir}/asterisk/*.h
