Summary: The GNU libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 1.4.2
Release: 6
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.bz2
URL: http://www.gnu.org/software/libtool/
Patch1: libtool-1.3.5-mktemp.patch
Patch2: libtool-1.4-nonneg.patch
Patch4: libtool-1.4.2-s390.patch
Patch5: libtool-1.4.2-test-quote.patch
Patch6: libtool-1.4.2-filemagic.patch
Patch7: libtool-1.4.2-archive-shared.patch
Prefix: %{_prefix}
PreReq: /sbin/install-info, autoconf, automake >= 1.4p1, m4, perl
Requires: libtool-libs = %{version}-%{release}, mktemp
BuildRoot: %{_tmppath}/%{name}-root

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
libtool.  GNU libtool uses these libraries to provide portible dynamic
loading of shared libraries.

If you are using some programs that provide shared libraries built
with GNU libtool, you should install the libtool-libs package to
provide the dynamic loading library

%prep
%setup -q
%patch1 -p1 -b .mktemp
%patch2 -p1 -b .nonneg
%patch4 -p1 -b .s390
%patch5 -p1 -b .test
#%patch6 -p1 -b .magic
#%patch7 -p1 -b .archive

%build
# define libtoolize to true, in case configure calls it
%define __libtoolize /bin/true
%configure
						
make -k -C doc
make

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

%makeinstall

cp install-sh missing mkinstalldirs demo

{ cd ${RPM_BUILD_ROOT}
  gzip -9nf .%{_infodir}/*.info*
# XXX remove zero length file
  rm -f .%{_datadir}/libtool/libltdl/stamp-h.in
# XXX forcibly break hardlinks
  mv .%{_datadir}/libtool/libltdl .%{_datadir}/libtool/libltdl-X
  mkdir .%{_prefix}/share/libtool/libltdl
  cp .%{_datadir}/libtool/libltdl-X/* .%{_datadir}/libtool/libltdl
  rm -rf .%{_prefix}/share/libtool/libltdl-X
}

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/libtool.info.gz %{_infodir}/dir

# the rest of the post script is not needed, right?
exit 0

# XXX hack alert
cd %{_defaultdocdir}/libtool-%{version}/demo || cd %{_prefix}/doc/libtool-%{version}/demo || exit 0
libtoolize --copy --force
aclocal
autoheader
automake
autoconf

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/libtool.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README
%doc THANKS TODO ChangeLog demo
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
