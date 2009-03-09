Summary:	Intel IA32 CPU Microcode Utility
Summary(pl.UTF-8):	Aktualizator mikrokodu procesorów Intel IA32
Name:		microcode_ctl
Version:	1.17
Release:	3
Epoch:		1
License:	GPL
Group:		Base
Source0:	http://www.urbanmyth.org/microcode/%{name}-%{version}.tar.gz
# Source0-md5:	98a7f06acef8459c8ef2a1b0fb86a99e
Source1:	%{name}.init
# http://downloadcenter.intel.com/, enter "xeon", go to generic xeon link,
# choose Linux as OS and get latest microcode release
Source2:	http://downloadmirror.intel.com/14303/eng/microcode-20080910.dat
# Source2-md5:	b12d0df79afe9fc363bd3ed5163eb591
URL:		http://www.urbanmyth.org/microcode/
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	uname(release) >= 2.6.20
ExclusiveArch:	i686 pentium2 pentium3 pentium4 x86_64 ia32e
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The microcode_ctl utility is a companion to the IA32 microcode driver.
The utility has two uses: a) it decodes and sends new microcode to the
kernel driver to be uploaded to Intel IA32 family processors. (Pentium
Pro, PII, Celeron, PIII, Xeon Pentium 4 etc.) b) it signals the kernel
driver to release any buffers it may hold

The microcode update is volatile and needs to be uploaded on each
system boot i.e. it doesn't reflash your cpu permanently, reboot and
it reverts back to the old microcode.

%description -l pl.UTF-8
Narzędzie będące dodatkiem do sterownika mikrokodu IA32. Program
dekoduje i wysyła nowy mikrokod do jądra systemu w celu załadowania go
do jednego z procesorów rodziny IA32 (Pentium Pro, PII, Celeron, PIII,
Xeon, Pentium 4 itd.). Ponadto wysyłany jest sygnał do jądra by to
zwolniło wszystkie bufory.

Aktualizacja mikrokodu musi być dokonywana po każdym restarcie systemu
tzn. nie jest to trwała aktualizacja. Po restarcie procesor zawiera
stary mikrokod.

%prep
%setup -q

%build
%{__cc} %{rpmldflags} %{rpmcflags} -Wall \
	microcode_ctl.c -o microcode_ctl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir}}
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

install	%{name} $RPM_BUILD_ROOT%{_sbindir}
install %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/microcode.dat

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc Changelog README
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/microcode.dat
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
