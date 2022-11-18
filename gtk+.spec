%global _install install -p -m0644
%global vendor %{?_vendor:%{_vendor}}%{!?_vendor:openEuler}
%global rpmvdir /usr/lib/rpm/%{vendor}

Name:           gtk+
Version:        1.2.10
Epoch:          1
Release:        92
Summary:        A toolkit for creating graphical user interfaces
License:        LGPLv2+
URL:            http://www.gtk.org/
Source0:        http://download.gimp.org/pub/gtk/v1.2/gtk+-%{version}.tar.gz
Source1:        gtkrc-default
Source2:        gtk+-pofiles.tar.gz
Source3:        gtkrc.ja.utf8
Source4:        gtkrc.ko.utf8
Source5:        gtkrc.zh_CN.utf8
Source6:        gtkrc.zh_TW.utf8

Provides:       gtk1 = %{version}-%{release}

Patch0001:      gtk+-1.2.10-ahiguti.patch
Patch0002:      gtk+-1.2.8-wrap-alnum.patch
Patch0003:      gtk+-1.2.10-alignment.patch
Patch0004:      gtk+-1.2.10-expose.patch
Patch0005:      gtk+-1.2.10-focus.patch
Patch0006:      gtk+-1.2.10-encoding.patch
Patch0007:      gtk+-1.2.10-ctext.patch
Patch0008:      gtk+-1.2.10-utf8fontset.patch
Patch0009:      gtk+-1.2.10-kpenter.patch
Patch0010:      gtk+-1.2.10-themeswitch.patch
Patch0011:      gtk+-1.2.10-pixmapref.patch
Patch0012:      gtk+-1.2.10-missingchar.patch
Patch0013:      gtk+-1.2.10-ukfont.patch
Patch0014:      gtk+-1.2.10-deletedir.patch
Patch0015:      gtk+-1.2.10-fontwarning.patch
Patch0016:      gtk+-1.2.10-troughpaint.patch
Patch0017:      gtk+-1.2.10-localecrash.patch
Patch0018:      gtk+-1.2.10-dndorder.patch
Patch0019:      gtk+-1.2.10-clistfocusrow.patch
Patch0020:      gtk+-1.2.10-bellvolume.patch
Patch0021:      gtk+-1.2.10-libtool.patch
Patch0022:      gtk+-1.2.10-gtkgdkdep.patch
Patch0023:      gtk+-underquoted.patch
Patch0024:      gtk+-1.2.10-ppc64.patch
Patch0025:      gtk+-1.2.10-no_undefined.patch
Patch0026:      gtk+-1.2.10-multilib.patch
Patch0027:      gtk+-1.2.10-unused-deps.patch
Patch0028:      gtk+-1.2.10-autotools.patch
Patch0029:      gtk+-1.2.10-format.patch

BuildRequires:  make coreutils gettext glib-devel >= 1:%{version} glibc-common
BuildRequires:  libtool libX11-devel libXext-devel libXi-devel libXt-devel

%description
GTK, or the GIMP Toolkit, is a multi-platform toolkit for creating graphical
user interfaces. Offering a complete set of widgets, GTK is suitable for
projects ranging from small one-off tools to complete application suites.

%package        devel
Summary:        Development for GTK+ applications
Provides:       gtk1-devel = %{version}-%{release}
Requires:       %{name} = %{epoch}:%{version}-%{release} glib-devel
Requires:       libX11-devel libXext-devel libXi-devel libXt-devel

%description    devel
Libraries, header files and other related documents for development of GTK+ applications.

%package        help
Summary:        Documents for gtk+
Provides:       gtk1-help = %{version}-%{release}
Buildarch:      noarch

%description    help
Man pages and other related documents.

%prep
%autosetup -p1 -a 2

cp -p %{rpmvdir}/config.{guess,sub} .

%build
%configure --disable-static --with-xinput=xfree --with-native-locale LIBTOOL=/usr/bin/libtool

%make_build LIBTOOL=/usr/bin/libtool

%install
%make_install LIBTOOL=/usr/bin/libtool

./mkinstalldirs tmpdocs/tutorial
%_install docs/html/gtk_tut.html docs/html/gtk_tut-[0-9]*.html docs/html/*.gif tmpdocs/tutorial
for dir in examples/*; do
        if [ -d $dir ]; then
                ./mkinstalldirs tmpdocs/$dir
                for file in $dir/* ; do
                        case $file in
                        *pre1.2.7)
                                ;;
                        *)
                                %_install $file tmpdocs/$dir
                                ;;
                        esac
                done
        fi
done

%_install -D %{SOURCE1} %{buildroot}/etc/gtk/gtkrc

for source in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}; do
        %_install $source %{buildroot}/etc/gtk/
done

rm -rf %{buildroot}%{_infodir} %{buildroot}%{_libdir}/lib*.la %{buildroot}%{_libdir}/lib*.a

%find_lang %{name}

%check
make check LIBTOOL=/usr/bin/libtool

%files -f %{name}.lang
%license COPYING
%{_libdir}/libg{d,t}k-1.2.so.*
%{_datadir}/themes/Default/
%dir %{_sysconfdir}/gtk/
%config(noreplace) %{_sysconfdir}/gtk/gtkrc*

%files devel
%{_bindir}/gtk-config
%{_includedir}/gtk-1.2/
%{_libdir}/libg{d,t}k.so
%{_libdir}/pkgconfig/g{d,t}k*.pc
%{_datadir}/aclocal/gtk.m4

%files help
%doc AUTHORS ChangeLog NEWS README TODO
%doc tmpdocs/tutorial/
%doc tmpdocs/examples/
%{_mandir}/man1/gtk-config.1*

%changelog
* Thu Nov 17 2022 wangkai <wangkai385@h-partners.com> - 1:1.2.10-92
- Replace openEuler with vendor

* Fri Jan 07 2022 wulei <wulei80@huawei.com> - 1.2.10-91
- Fix config.guess and config.sub not found

* Mon Dec 02 2019 zhouyihang <zhouyihang1@huawei.com> - 1.2.10-90
- Package init
