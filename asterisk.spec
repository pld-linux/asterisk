# TODO:
# - cgi-bin package - separate, because of suid-root
# - separate plugins into packages

Summary:	Asterisk PBX
Summary(pl):	Centralka (PBX) Asterisk
Name:		asterisk
Version:	0.4.0
Release:	0.5
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.asterisk.org/pub/telephony/asterisk/%{name}-%{version}.tar.gz
Patch0:		%{name}-destdir.patch
Patch1:		%{name}-Makefile.patch
URL:		http://www.asteriskpbx.com/
BuildRequires:	glib-devel
BuildRequires:	gtk+-devel
BuildRequires:	mysql-devel
BuildRequires:	openh323-devel >= 1.11.7
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pwlib-devel >= 1.4.11
BuildRequires:	speex-devel
BuildRequires:	zlib-devel
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
current list of supported hardware, see http://www.asteriskpbx.com/.

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
obs³ugiwanego sprzêtu mo¿na znale¼æ pod http://www.asteriskpbx.com/.

%package devel
Summary:	Header files for Asterisk platform
Summary(pl):	Pliki nag³ówkowe platformy Asterisk
Group:		Development
Requires:	%{name} = %{version}

%description devel
Header files for Asterisk development platform.

%description devel -l pl
Pliki nag³ówkowe platformy programistycznej Asterisk.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make}

# H323 plugin:
cd channels/h323/
%{__make} \
	PWLIBDIR="/usr" \
	OPENH323DIR="/usr"
cd ../../

# it requires doxygen - I don't know if we should do this...
#%{__make} progdocs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/log/asterisk

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} samples \
	DESTDIR=$RPM_BUILD_ROOT

cd channels/h323/
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} samples \
	DESTDIR=$RPM_BUILD_ROOT
cd ../../

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog CREDITS HARDWARE README* SECURITY configs doc/{*.txt,linkedlists.README}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/asterisk
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/asterisk/*.conf
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/asterisk/*.adsi
%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules
%attr(755,root,root) %{_libdir}/asterisk/modules/*.so
%dir /var/lib/asterisk
%dir /var/lib/asterisk/agi-bin
%dir /var/lib/asterisk/images
%dir /var/lib/asterisk/keys
%dir /var/lib/asterisk/sounds
%dir /var/lib/asterisk/sounds/digits
/var/lib/asterisk/images/*.jpg
/var/lib/asterisk/keys/*.pub
/var/lib/asterisk/sounds/*.gsm
/var/lib/asterisk/sounds/digits/*.gsm
%dir /var/spool/asterisk
%dir /var/spool/asterisk/vm
%dir /var/log/asterisk

# RedHat specific init script file
#%attr(754,root,root)       /etc/rc.d/init.d/asterisk
#%dir /var/lib/asterisk/agi-bin/*

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/asterisk
%{_includedir}/asterisk/*.h
