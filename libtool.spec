Summary: The GNU libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 1.5.6
Release: 4
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz
Source1: libtool-1.5.4-ltmain-SED.patch
URL: http://www.gnu.org/software/libtool/
#Patch1: libtool-1.5-mktemp.patch
Patch2: libtool-1.4-nonneg.patch
Patch4: libtool-1.5-libtool.m4-x86_64.patch
Patch9: libtool-1.4.2-multilib.patch
Patch10: libtool-1.4.2-demo.patch
## Patch from James Henstridge making restricted symbol exports work on Linux
#Patch11: libtool-1.5-expsym-linux.patch
## http://mail.gnu.org/pipermail/bug-libtool/2002-October/004272.html
#Patch12: libtool-1.5-readonlysym.patch
# Fix automake related test failure
Patch14: libtool-1.5-testfailure.patch
#Patch15: libtool-1.5-relink-libdir-order-91110.patch
#Patch16: libtool-1.5-AC_PROG_LD_GNU-quote-v-97608.patch
#Patch17: libtool-1.5-nostdlib.patch
PreReq: /sbin/install-info, autoconf, automake, m4, perl
BuildRequires: autoconf, automake, texinfo
# make sure we can configure all supported langs
Buildrequires: gcc, gcc-c++, libstdc++-devel, gcc-g77, gcc-java
Requires: libtool-libs = %{version}-%{release}, mktemp
BuildRoot: %{_tmppath}/%{name}-root

# run "make check" by default
%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}
# except ia64 where currently 16/83 tests fail (see #55176)
%ifarch ia64
  %define _without_check 1
%endif

%description
The libtool package contains the GNU libtool, a set of shell scripts
which automatically configure UNIX and UNIX-like architectures to
generically build shared libraries.  Libtool provides a consistent,
portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, you
should install libtool.

%package libs
Summary: Runtime libraries for GNU libtool.
Group: System Environment/Libraries

%description libs
The libtool-libs package contains the runtime libraries from GNU
libtool.  GNU libtool uses these libraries to provide portable dynamic
loading of shared libraries.

If you are using some programs that provide shared libraries built
with GNU libtool, you should install the libtool-libs package to
provide the dynamic loading library

%prep
%setup -q
#%%patch1 -p1 -b .mktemp
%patch2 -p1 -b .nonneg
%patch4 -p1 -b .x86_64
%patch9 -p1 -b .multilib
%ifarch x86_64 s390 s390x
%patch10 -p1 -b .demo
%endif
#%%patch11 -p1 -b .expsym-linux
#%%patch12 -p1 -b .readonlysym
%patch14 -p1 -b .testfailure
#%%patch15 -p1 -b .libdir-order
#%%patch16 -p1 -b .ldquote
#%%patch17 -p1 -b .nostdlib

# patch10 and patch14 change a Makefile.am
# patch9 touches libtool.m4
./bootstrap

%build
export CC=gcc
export CXX=g++
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure
make

%if ! %{_without_check}
  make check # VERBOSE=yes
%endif

%install
rm -rf %{buildroot}
%makeinstall

# add SED definition to ltmain.sh for legacy ltconfig's
patch -d %{buildroot}%{_datadir}/libtool -z .sed < %{SOURCE1}

rm -f %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

%post
/sbin/install-info %{_infodir}/libtool.info.gz %{_infodir}/dir


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/libtool.info.gz %{_infodir}/dir
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README THANKS TODO ChangeLog
%{_bindir}/*
%{_includedir}/*
%{_infodir}/libtool.info*
%{_datadir}/libtool
%{_libdir}/libltdl.so
%{_libdir}/libltdl.*a
%{_datadir}/aclocal/*

%files libs
%defattr(-,root,root)
%{_libdir}/libltdl.so.*

%changelog
* Tue Jul  6 2004 Jens Petersen <petersen@redhat.com> - 1.5.6-4
- improve buildrequires and prereqs
- buildrequire texinfo (Dawid Gajownik, 126950)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 13 2004 Thomas Woerner <twoerner@redhat.com> - 1.5.6-2
- compile libltdl.a PIC

* Mon Apr 12 2004 Jens Petersen <petersen@redhat.com> - 1.5.6-1
- update to 1.5.6 bugfix release

* Sun Apr  4 2004 Jens Petersen <petersen@redhat.com> - 1.5.4-1
- 1.5.4 bugfix release
- improve libtool-1.4.2-multilib.patch (Albert Chin) and only apply to
  libtool.m4
- use bootstrap instead of autoreconf to update configuration
- update libtool-1.4.3-ltmain-SED.patch to libtool-1.5.4-ltmain-SED.patch

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Jens Petersen <petersen@redhat.com> - 1.5.2-1
- update to 1.5.2 bugfix release
- update libtool-1.5-libtool.m4-x86_64.patch
- nolonger need libtool-1.5-mktemp.patch, libtool-1.5-expsym-linux.patch,
  libtool-1.5-readonlysym.patch, libtool-1.5-relink-libdir-order-91110.patch,
  libtool-1.5-AC_PROG_LD_GNU-quote-v-97608.patch and libtool-1.5-nostdlib.patch

* Tue Oct 28 2003 Jens Petersen <petersen@redhat.com> - 1.5-8
- update libtool-1.4.2-multilib.patch to also deal with powerpc64 (#103316)
  [Joe Orton]

* Sun Oct 26 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild again, Jakub has done a new compiler version number

* Thu Oct 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild

* Thu Jul 17 2003 Jens Petersen <petersen@redhat.com> - 1.5-5
- bring back libtool-1.4.2-demo.patch to disable nopic tests on amd64 
  and s390x again

* Tue Jul 15 2003 Owen Taylor <otaylor@redhat.com>
- Fix misapplied chunk for expsym-linux patch

* Tue Jul  8 2003 Jens Petersen <petersen@redhat.com> - 1.5-4
- remove the quotes around LD in AC_PROG_LD_GNU (#97608)
  [reported by twaugh]
- use -nostdlib also when linking with g++ and non-GNU ld in
  _LT_AC_LANG_CXX_CONFIG [reported by fnasser, patch by aoliva]
- use %%configure with CC and CXX set 

* Thu Jun 12 2003 Jens Petersen <petersen@redhat.com> - 1.5-3
- don't use %%configure since target options caused libtool to assume
  i386-redhat-linux-gcc instead of gcc for CC (reported by Joe Orton)
- add libtool-1.5-relink-libdir-order-91110.patch to fix order of lib dirs
  searched when relinking (#91110) [patch from Joe Orton]

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  1 2003 Jens Petersen <petersen@redhat.com> - 1.5-1
- update to 1.5
- no longer override config.{guess,sub} for rpmbuild %%configure,
  redhat-rpm-config owns those now
- update and rename libtool-1.4.2-s390_x86_64.patch to
  libtool-1.5-libtool.m4-x86_64.patch since s390 now included
- buildrequire autoconf and automake, no longer automake14
- skip make check on s390 temporarily
- no longer skip demo-nopic.test on x86_64, s390 and s390x
- from Owen Taylor
  - add libtool-1.4.2-expsym-linux.patch (#55607) [from James Henstridge]
  - add quoting in mktemp patch
  - add libtool-1.5-readonlysym.patch
  - add libtool-1.5-testfailure.patch workaround
  - no longer need libtool-1.4.2-relink-58664.patch

* Sat Feb 08 2003 Florian La Roche <Florian.LaRoche@redhat.de> - 1.4.3-5
- add config.guess and config.sub, otherwise old versions of
  these files can creep into /usr/share/libtool/

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Jens Petersen <petersen@redhat.com> 1.4.3-3
- fix mktemp to work when running mktemp fails (#76602)
  [reported by (Oron Peled)]
- remove info dir file, don't exclude it
- fix typo in -libs description (#79619)
- use buildroot instead of RPM_BUILD_ROOT

* Tue Jan 07 2003 Karsten Hopp <karsten@redhat.de> 1.4.3-2.2
- use lib64 on s390x, too.

* Thu Dec  5 2002 Jens Petersen <petersen@redhat.com>
- add comment to explain why we use an old Automake for building
- buildrequire automake14

* Sat Nov 23 2002 Jens Petersen <petersen@redhat.com>
- add --without check build option to allow disabling of "make check"
- exclude info dir file rather than removing

* Sat Nov 23 2002 Jens Petersen <petersen@redhat.com> 1.4.3-2
- define SED in ltmain.sh for historic ltconfig files
- define macro AUTOTOOLS to hold automake-1.4 and aclocal-1.4, and use it
- leave old missing file for now
- general spec file cleanup
  - don't copy install files to demo nor mess with installed ltdl files
  - don't need to run make in doc
  - force removal of info dir file
  - don't need to create install prefix dir
  - don't bother gzipping info files ourselves

* Mon Nov 18 2002 Jens Petersen <petersen@redhat.com> 1.4.3-1
- update to 1.4.3
- remove obsolete patches (test-quote, dup-deps, libtoolize-configure.ac)
- apply the multilib patch to just the original config files
- update x86_64/s390 patch and just apply to original config files
- use automake-1.4 in "make check" for demo-make.test to pass!
- remove info dir file that is not installed
- make autoreconf update missing

* Mon Oct 07 2002 Phil Knirsch <pknirsch@redhat.com>  1.4.2-12.2
- Added s390x and x64_64 support.

* Fri Oct  4 2002 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-12.1
- rebuild

* Fri Sep 13 2002 Nalin Dahyabhai <nalin@redhat.com>
- patch to find the proper libdir on multilib boxes
 
* Mon Aug 19 2002 Jens Petersen <petersen@redhat.com> 1.4.2-12
- don't include demo in doc, specially now that we "make check" (#71609)

* Tue Aug 13 2002 Jens Petersen <petersen@redhat.com> 1.4.2-11
- don't hardcode "configure.in" in libtoolize (#70864)
  [reported by bastiaan@webcriminals.com]
- make check, but not on ia64

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.4.2-10
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com> 1.4.2-9
- automated rebuild

* Fri Apr 26 2002 Jens Petersen <petersen@redhat.com> 1.4.2-8
- add old patch from aoliva to fix relinking when installing into a buildroot
- backport dup-deps fix from cvs stable branch

* Wed Mar 27 2002 Jens Petersen <petersen@redhat.com> 1.4.2-7
- run ldconfig in postin and postun

* Thu Feb 28 2002 Jens Petersen <petersen@redhat.com> 1.4.2-6
- rebuild in new environment

* Tue Feb 12 2002 Jens Petersen <petersen@redhat.com> 1.4.2-5
- revert filemagic and archive-shared patches following cvs (#54887)
- don't change "&& test" to "-a" in ltmain.in

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.4.2-4
- automated rebuild

* Mon Dec  3 2001 Jens Petersen <petersen@redhat.com> 1.4.2-3
- test quoting patch should be on ltmain.in not ltmain.sh (#53276)
- use file_magic for Linux ELF (#54887)
- allow link against an archive when building a shared library (#54887)
- include ltdl.m4 in manifest (#56671)

* Wed Oct 24 2001 Jens Petersen <petersen@redhat.com> 1.4.2-2
- added URL to spec

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.4.2-1
- 1.4.2 - sync up with autoconf...

* Thu Jul  5 2001 Bernhard Rosenkraenzer <bero@redhat.de> 1.4-8
- extend s390 patch to 2 more files
- s/Copyright/License/

* Wed Jul 04 2001 Karsten Hopp <karsten@redhat.de>
- add s390 patch for deplibs_check_method=pass_all

* Tue Jun 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add patches from Tim Waugh #42724

* Mon Jun 11 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add patches from cvs mainline

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix a "test" bug in ltmain.sh

* Sun Jun 03 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- disable the post commands to modify /usr/share/doc/

* Sat May 12 2001 Owen Taylor <otaylor@redhat.com>
- Require automake 1.4p1

* Wed May 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to libtool 1.4
- adjust or remove patches

* Thu Jul 13 2000 Elliot Lee <sopwith@redhat.com>
- Fix recognition of ^0[0-9]+$ as a non-negative integer.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch to use mktemp to create the tempdir
- use %%configure after defining __libtoolize to /bin/true

* Mon Jul  3 2000 Matt Wilson <msw@redhat.com>
- subpackage libltdl into libtool-libs

* Sun Jun 18 2000 Bill Nottingham <notting@redhat.com>
- running libtoolize on the libtool source tree ain't right :)

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.3.5.

* Fri Mar  3 2000 Jeff Johnson <jbj@redhat.com>
- add prereqs for m4 and perl inorder to run autoconf/automake.

* Mon Feb 28 2000 Jeff Johnson <jbj@redhat.com>
- functional /usr/doc/libtool-*/demo by end-user %post procedure (#9719).

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.4.

* Mon Dec  6 1999 Jeff Johnson <jbj@redhat.com>
- change from noarch to per-arch in order to package libltdl.a (#7493).

* Thu Jul 15 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.3.

* Mon Jun 14 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.2.

* Tue May 11 1999 Jeff Johnson <jbj@redhat.com>
- explicitly disable per-arch libraries (#2210)
- undo hard links and remove zero length file (#2689)

* Sat May  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- disable the --cache-file passing to ltconfig; this breaks the older
  ltconfig scripts found around.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.2f

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- completed arm patch
- added patch to make it more arm-friendly
- upgrade to version 1.2d

* Thu May 07 1998 Donnie Barnes <djb@redhat.com>
- fixed busted group

* Sat Jan 24 1998 Marc Ewing <marc@redhat.com>
- Update to 1.0h
- added install-info support

* Tue Nov 25 1997 Elliot Lee <sopwith@redhat.com>
- Update to 1.0f
- BuildRoot it
- Make it a noarch package
