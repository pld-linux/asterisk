# TODO:
# - cgi-bin package - separate, because of suid-root

Summary:	Asterisk PBX
Name:		asterisk
Version:	0.4.0
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.asterisk.org/pub/telephony/asterisk/%{name}-%{version}.tar.gz
BuildRequires:	glib-devel
BuildRequires:	gtk+-devel
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	speex-devel
BuildRequires:	zlib-devel
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
current list of supported hardware, see www.asteriskpbx.com.

%package devel
Summary:	Header files for Asterisk
Summary(pl):	Pliki nag³ówkowe do Asterisk
Group:		Development
Requires:	%{name} = %{version}

%description devel
Header files for Asterisk.

%description devel -l pl
Pakiet ten zawiera pliki nag³ówkowe do Asterisk.

%prep
%setup -q

%build
%{__make}

# it requires doxygen - I don't know if we should do this...
#%{__make} progdocs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_PREFIX=$RPM_BUILD_ROOT
%{__make} samples \
	INSTALL_PREFIX=$RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc BUGS ChangeLog CREDITS HARDWARE README* SECURITY configs doc/{*.txt,linkedlists.README}
%attr(0755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/asterisk
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/asterisk/*.conf
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/asterisk/*.adsi
%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules
%attr(0755,root,root) %{_libdir}/asterisk/modules/*.so
%dir /var/lib/asterisk
%dir /var/lib/asterisk/agi-bin
%dir /var/lib/asterisk/sounds/digits
%attr(0644,root,root) /var/lib/asterisk/sounds/digits/*.gsm
%dir /var/lib/asterisk/images
%attr(0644,root,root) /var/lib/asterisk/images/*.jpg
%dir /var/lib/asterisk/keys
%attr(0644,root,root) /var/lib/asterisk/keys/*.pub
%dir /var/lib/asterisk/sounds
%attr(0644,root,root) /var/lib/asterisk/sounds/*.gsm

%dir /var/spool/asterisk
%dir /var/spool/asterisk/vm

# RedHat specific init script file
#%attr(0755,root,root)       /etc/rc.d/init.d/asterisk
#%attr(0755,root,root) %dir /var/lib/asterisk/agi-bin/*

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/asterisk
%attr(0644,root,root) %{_includedir}/asterisk/*.h

%clean
rm -rf $RPM_BUILD_ROOT
