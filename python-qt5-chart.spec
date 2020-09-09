# we don't want to provide private python extension libs
%define _exclude_files_from_autoprov %{python_sitearch}/.*\\.so

%define sname PyQtChart

Name:		python-qt5-chart
Version:	5.15.0
Release:	1
Summary:	Set of Python bindings for The Qt Charts library
License:	GPLv3
Group:		Development/KDE and Qt
URL:		https://www.riverbankcomputing.com/software/pyqtchart/
Source0:	http://pypi.io/packages/source/p/pyqtchart/%{sname}-%{version}.tar.gz

BuildRequires:	pkgconfig(python)
BuildRequires:	python-qt5-devel
BuildRequires:	python-sip
BuildRequires:	python-sip-qt5
BuildRequires:	python-qt5-qscintilla
BuildRequires:	pkgconfig(Qt5Charts)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)

%description
PyQtChart is a set of Python bindings for The Qt Company's Qt Charts library.
The bindings sit on top of PyQt5 and are implemented as a single module.


%prep
%autosetup -p1 -n %{sname}-%{version}

%build
### Python 3 build:
%{__python} ./configure.py \
  --pyqt-sipdir=%{_datadir}/sip/PyQt5 \
  --qmake="%{_qt5_bindir}/qmake" \
  --debug \
  --verbose

%make_build CXXFLAGS="%{optflags} -fPIC \$(DEFINES)"

%install
### python 3 Install:
%make_install INSTALL_ROOT=%{buildroot}

mkdir -p %{buildroot}%{_docdir}/%{name}/examples
    cp -fr examples/* %{buildroot}%{_docdir}/%{name}/examples/

# ensure .so modules are executable for proper -debuginfo extraction
for i in %{buildroot}%{python_sitearch}/PyQt5/*.so ; do
    test -x $i  || chmod a+rx $i
done

%files
%doc ChangeLog NEWS README
%doc %{_docdir}/%{name}/examples
%{python_sitearch}/PyQt5/QtChart.*
%{python_sitearch}/PyQtChart-%{version}.dist-info
%{_datadir}/python-sip/PyQt5/QtChart/
%dir %{_qt5_datadir}/qsci/
%dir %{_qt5_datadir}/qsci/api/
%dir %{_qt5_datadir}/qsci/api/python/
%{_qt5_datadir}/qsci/api/python/PyQtChart.api
