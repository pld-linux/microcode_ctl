Summary:	Intel IA32 CPU Microcode Utility
Summary(pl):	Aktualizator Mikrokodu Intel IA32 CPU
Name:		microcode_ctl
Version:	1.08
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.urbanmyth.org/microcode/%{name}-%{version}.tar.gz
# Source0-md5:	b0cb86263c136b5bf7a44c723cb6996e
Source1:	%{name}.init
Patch0:		%{name}-llh.patch
URL:		http://www.urbanmyth.org/microcode/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Conflicts:	kernel < 2.2.0
ExclusiveArch:	i386 i486 i586 i686 pentium2 pentium3 pentium4
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

%description -l pl
Narz�dzie b�d�ce dodatkiem do sterownika mikrokodu IA32. Program
dekoduje i wysy�a nowy mikrokod do j�dra systemu w celu za�adowania go
do jednego z procesor�w rodziny IA32 (Pentium Pro, PII, Celeron, PIII,
Xeon, Pentium 4 itd.). Ponadto wysy�any jest sygna� do j�dra by to
zwolni�o wszystkie bufory.

Aktualizacja mikrokodu musi by� dokonywana po ka�dym restarcie systemu
tzn. nie jest to trwa�a aktualizacja. Po restarcie procesor zawiera
stary mikrokod.

%prep
%setup -q
%patch0 -p1

%build
%{__cc} %{rpmldflags} %{rpmcflags} -Wall \
	microcode_ctl.c -o microcode_ctl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

install	%{name} $RPM_BUILD_ROOT%{_sbindir}
install %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8
install intel-ia32microcode-*.txt \
	$RPM_BUILD_ROOT%{_sysconfdir}/microcode.dat

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
%doc README Change*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config %{_sysconfdir}/microcode.dat
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
