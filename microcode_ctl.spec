Summary:	Intel IA32 CPU Microcode Utility
Summary(pl):	Aktualizator Mikrokodu Intel IA32 CPU
Name:		microcode_ctl
Version:	1.06
Release:	2
License:	GPL
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Source0:	http://www.urbanmyth.org/microcode/%{name}-%{version}.tar.gz
Source1:	%{name}.init
URL:		http://www.urbanmyth.org/microcode/
Conflicts:	kernel < 2.2.0
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
ExclusiveArch:	%{ix86}
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
Narzêdzie bêd±ce dodatkiem do sterownika mikrokodu IA32. Program
dekoduje i wys³a nowy mikrokod do j±dra systemu w celu za³adowania go
do jednego z procesorów rodziny IA32 (Pentium Pro, PII, Celeron, PIII,
Xeon, Pentium 4 itd.). Ponadto wysy³any jest sygna³ do j±dra by to
zwolni³o wszystkie bufory.

Aktualizacja mikrokodu musi byæ dokonywana po ka¿dym restarcie systemu
tzn. nie jest to trwa³a aktualizacja. Po restarcie procesor zawiera
stary mikrokod.

%prep
%setup -q

%build
%{__cc} -Wall -I%{_kernelsrcdir}/include %{rpmcflags} %{rpmldflags}\
	microcode_ctl.c -o microcode_ctl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

install	%{name} $RPM_BUILD_ROOT%{_sbindir}
install %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install intel-ia32microcode-*.txt \
	$RPM_BUILD_ROOT%{_sysconfdir}/microcode.dat

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

gzip -9nf README Change*

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
%doc *.gz
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(640,root,root) %config %{_sysconfdir}/microcode.dat
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
