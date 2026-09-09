# The libraries have the same SONAMEs as the system Qt 6 ones but are ABI
# incompatible with them (see the patch), so they must never be visible to
# anything except Steam Link.
%global __provides_exclude ^libQt6.*\\.so.*$
%global __requires_exclude ^libQt6.*\\.so.*$

# The plugins are loaded by Steam Link only, they provide nothing to the system.
%global __provides_exclude_from ^%{_libdir}/steamlink/plugins/.*$

%global qtdir %{_libdir}/steamlink

Name:           steamlink-qtbase
Version:        6.11.2
Release:        1%{?dist}
Summary:        Steam Link compatibility package - Qt 6 base libraries
License:        LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
URL:            https://www.qt.io

Source0:        https://download.qt.io/archive/qt/6.11/%{version}/submodules/qtbase-everywhere-src-%{version}.tar.xz

# Valve's QControllerEvent extension, extracted from the Steam Link Flatpak:
# https://github.com/flathub/com.valvesoftware.SteamLink/blob/beta/patches/steamlink/qtbase.patch
Patch0:         qtbase-steamlink-controller-event.patch

# Match the ELF private API version node used by the Fedora Qt 6 build.
Patch1:         qtbase-major-minor-private-api-tag.patch

ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  perl
BuildRequires:  python3
BuildRequires:  double-conversion-devel
BuildRequires:  libb2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libzstd-devel
BuildRequires:  md4c-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(libpcre2-16)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-cursor)
BuildRequires:  pkgconfig(xcb-glx)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-image)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xcb-xkb)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(zlib)

# %%check compares the exported symbols against the system libQt6Svg.
BuildRequires:  binutils
BuildRequires:  qt6-qtsvg

# steamlink is linked against libQt6Svg.so.6 as well, but that one is ABI
# compatible with the stock Fedora build and does not need to be duplicated.
Requires:       qt6-qtsvg%{?_isa}

%description
This package is meant for compatibility purposes with Steam Link, which
requires a Qt 6 build carrying Valve's out of tree QControllerEvent extension
in a non-standard path.

The extension adds a virtual member to QWidget and is therefore not ABI
compatible with the system Qt 6; the libraries are installed privately and are
of no use to anything but Steam Link.

%prep
%autosetup -p1 -n qtbase-everywhere-src-%{version}

%build
# Qt does not build correctly with LTO (rhbz#1900527).
%global _lto_cflags %{nil}

%cmake -GNinja \
    -DBUILD_SHARED_LIBS=ON \
    -DQT_BUILD_BENCHMARKS=OFF \
    -DQT_BUILD_EXAMPLES=OFF \
    -DQT_BUILD_TESTS=OFF \
    -DQT_QMAKE_TARGET_MKSPEC=linux-g++ \
\
    -DINSTALL_ARCHDATADIR=%{_lib}/steamlink \
    -DINSTALL_BINDIR=%{_lib}/steamlink/bin \
    -DINSTALL_DATADIR=%{_lib}/steamlink/share \
    -DINSTALL_DESCRIPTIONSDIR=%{_lib}/steamlink/modules \
    -DINSTALL_DOCDIR=%{_lib}/steamlink/doc \
    -DINSTALL_EXAMPLESDIR=%{_lib}/steamlink/examples \
    -DINSTALL_INCLUDEDIR=%{_lib}/steamlink/include \
    -DINSTALL_LIBDIR=%{_lib}/steamlink \
    -DINSTALL_LIBEXECDIR=%{_lib}/steamlink/libexec \
    -DINSTALL_MKSPECSDIR=%{_lib}/steamlink/mkspecs \
    -DINSTALL_PLUGINSDIR=%{_lib}/steamlink/plugins \
    -DINSTALL_SYSCONFDIR=%{_lib}/steamlink/etc \
    -DINSTALL_TESTSDIR=%{_lib}/steamlink/tests \
    -DINSTALL_TRANSLATIONSDIR=%{_lib}/steamlink/translations \
\
    -DFEATURE_elf_private_full_version=ON \
    -DFEATURE_reduce_relocations=OFF \
    -DFEATURE_relocatable=OFF \
    -DFEATURE_separate_debug_info=OFF \
\
    -DFEATURE_rpath=ON \
\
    -DFEATURE_glib=ON \
    -DFEATURE_icu=ON \
    -DFEATURE_openssl_hash=ON \
    -DFEATURE_openssl_linked=ON \
    -DFEATURE_system_freetype=ON \
    -DFEATURE_system_harfbuzz=ON \
    -DFEATURE_system_jpeg=ON \
    -DFEATURE_system_pcre2=ON \
    -DFEATURE_system_png=ON \
    -DFEATURE_system_zlib=ON \
    -DFEATURE_zstd=ON \
\
    -DFEATURE_fontconfig=ON \
    -DFEATURE_opengl=ON \
    -DINPUT_opengl=desktop \
    -DFEATURE_xcb=ON \
    -DFEATURE_xcb_xlib=ON \
    -DFEATURE_xkbcommon=ON \
    -DFEATURE_xkbcommon_x11=ON \
\
    -DFEATURE_concurrent=OFF \
    -DFEATURE_cups=OFF \
    -DFEATURE_dbus=OFF \
    -DFEATURE_directfb=OFF \
    -DFEATURE_eglfs=OFF \
    -DFEATURE_evdev=OFF \
    -DFEATURE_journald=OFF \
    -DFEATURE_libinput=OFF \
    -DFEATURE_libproxy=OFF \
    -DFEATURE_linuxfb=OFF \
    -DFEATURE_mtdev=OFF \
    -DFEATURE_printsupport=OFF \
    -DFEATURE_sctp=OFF \
    -DFEATURE_sql=OFF \
    -DFEATURE_testlib=OFF \
    -DFEATURE_tslib=OFF \
    -DFEATURE_vkkhrdisplay=OFF \
    -DFEATURE_vnc=OFF \
    -DFEATURE_vulkan=OFF \
    -DFEATURE_xml=OFF

%cmake_build

%install
%cmake_install

# Runtime only: no headers, no build system integration, no host tools.
rm -fr %{buildroot}%{qtdir}/{bin,doc,etc,examples,include,libexec,mkspecs,modules,share,tests,translations}
rm -fr %{buildroot}%{qtdir}/{cmake,metatypes,objects-*,pkgconfig,sbom}

# Wayland protocol descriptions and JSON schemas for building other Qt modules.
rm -fr %{buildroot}%{_datadir}/qt6
rm -f  %{buildroot}%{qtdir}/*.a %{buildroot}%{qtdir}/*.la %{buildroot}%{qtdir}/*.prl
rm -f  %{buildroot}%{qtdir}/libQt6*.so

# steamlink links the GIF and JPEG image format plugins in statically, the same
# way the Flatpak builds them.
rm -fr %{buildroot}%{qtdir}/plugins/imageformats

# TUIO is multi touch over UDP, of no use here.
rm -fr %{buildroot}%{qtdir}/plugins/generic

%check
libs="%{buildroot}%{qtdir}/libQt6Core.so.6 %{buildroot}%{qtdir}/libQt6Gui.so.6 %{buildroot}%{qtdir}/libQt6Widgets.so.6 %{buildroot}%{qtdir}/libQt6Network.so.6"

# The symbols the prebuilt steamlink binary looks up in Qt at startup.
for sym in \
    _ZN16QControllerEventC1Ev \
    _ZN16QControllerEvent9setButtonENS_9EventTypeEb \
    _ZN16QControllerEvent7setDPadENS_9DirectionE \
    _ZN16QControllerEvent13setThumbstickENS_9EventTypeEdd \
    _ZN16QControllerEvent10setTriggerENS_9EventTypeEd \
    _ZN7QWidget15controllerEventEP16QControllerEvent ; do
    nm -D --defined-only $libs | grep -qw "${sym}@@Qt_6" || {
        echo "missing controller event symbol: ${sym}" >&2
        exit 1
    }
done

# The system libQt6Svg.so.6 binds against these libraries, so everything it
# imports from Qt - including the Qt_6.11_PRIVATE_API node - has to be here.
# Symbol lines have three fields; skip the per file headers and blank lines.
nm -D --defined-only $libs | awk 'NF == 3 { print $3 }' | sed 's/@@/@/' \
    > provided.txt
nm -D --undefined-only %{_libdir}/libQt6Svg.so.6 | awk '{ print $2 }' \
    | grep -E '@Qt_6' > svg-needed.txt
missing=$(grep -vxF -f provided.txt svg-needed.txt || :)
if [ -n "$missing" ]; then
    echo "libQt6Svg.so.6 symbols not provided by this build:" >&2
    echo "$missing" >&2
    exit 1
fi

%files
%license LICENSES/LGPL-3.0-only.txt LICENSES/GPL-3.0-only.txt
%license LICENSES/Qt-GPL-exception-1.0.txt
# Shared with the steamlink package, which installs bin/ and lib/ here.
%dir %{qtdir}
%{qtdir}/libQt6*.so.6*
%{qtdir}/plugins/

%changelog
* Wed Sep 09 2026 Simone Caronni <negativo17@gmail.com> - 6.11.2-1
- Update to 6.11.2.

* Sat Aug 22 2026 Simone Caronni <negativo17@gmail.com> - 6.11.1-1
- First build.
