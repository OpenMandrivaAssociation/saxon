# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Summary:        Java XPath, XSLT 2.0 and XQuery implementation
Name:           saxon
Version:        9.2.0.3
Release:        5
# net.sf.saxon.om.XMLChar is from ASL-licensed Xerces
License:        MPLv1.0 and ASL 1.1
Group:          Development/Java
URL:            http://saxon.sourceforge.net/
Source0:        http://dl.sourceforge.net/project/saxon/Saxon-HE/9.2/saxon-resources9-2-0-2.zip
Source1:        %{name}.saxon.script
Source2:        %{name}.saxonq.script
Source3:        %{name}.build.script
Source4:        %{name}.1
Source5:        %{name}q.1
# There's no 9.2.0.3 resource bundle, we patch 9.2.0.2 with difference against 9.2.0.3 source bundle
Patch0:         saxon-9.2.0.2-9.2.0.3.patch
BuildRequires:  unzip
BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  bea-stax-api
BuildRequires:  xml-commons-apis
BuildRequires:  xom
BuildRequires:  jdom >= 0:1.0-0.b7
BuildRequires:  java-javadoc
BuildRequires:  jdom-javadoc >= 0:1.0-0.b9.3jpp
BuildRequires:  dom4j
Requires:       jpackage-utils
Requires:       bea-stax-api
Requires:       bea-stax
Requires:       jaxp_parser_impl
Requires:       /usr/sbin/update-alternatives
Provides:       jaxp_transform_impl = %{version}-%{release}

# Older versions were split into multile packages
Obsoletes:	%{name}-xpath < %{version}-%{release}
Obsoletes:	%{name}-xom < %{version}-%{release}
Obsoletes:	%{name}-sql < %{version}-%{release}
Obsoletes:	%{name}-jdom < %{version}-%{release}
Obsoletes:	%{name}-dom < %{version}-%{release}

BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Saxon HE is Saxonica's non-schema-aware implementation of the XPath 2.0,
XSLT 2.0, and XQuery 1.0 specifications aligned with the W3C Candidate
Recommendation published on 3 November 2005. It is a complete and
conformant implementation, providing all the mandatory features of
those specifications and nearly all the optional features. 


%package        manual
Summary:        Manual for %{name}
Group:          Development/Java

%description    manual
Manual for %{name}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demos for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%package        scripts
Summary:        Utility scripts for %{name}
Group:          Development/Java
Requires:       jpackage-utils >= 0:1.5
Requires:       %{name} = %{version}-%{release}

%description    scripts
Utility scripts for %{name}.


%prep
%setup -q -c
unzip -q source.zip -d src
cd src
%patch0 -p1 -b .9.2.0.3
cd ..

cp -p %{SOURCE3} ./build.xml

# deadNET
rm -rf src/net/sf/saxon/dotnet

# Depends on XQJ (javax.xml.xquery)
rm -rf src/net/sf/saxon/xqj

# This requires a EE edition feature (com.saxonica.xsltextn)
rm -rf src/net/sf/saxon/option/sql/SQLElementFactory.java

# cleanup unnecessary stuff we'll build ourselves
rm -rf docs/api
find . \( -name "*.jar" -name "*.pyc" \) -delete


%build
mkdir -p build/classes
cat >build/classes/edition.properties <<EOF
config=net.sf.saxon.Configuration
platform=net.sf.saxon.java.JavaPlatform
EOF

export CLASSPATH=%(build-classpath xml-commons-apis jdom xom bea-stax-api dom4j)
ant \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -Djdom.javadoc=%{_javadocdir}/jdom


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}

# scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -p -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{name}q
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
install -p -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man1/%{name}q.1

# jaxp_transform_impl ghost symlink
ln -s %{_sysconfdir}/alternatives \
  $RPM_BUILD_ROOT%{_javadir}/jaxp_transform_impl.jar


%clean
rm -rf $RPM_BUILD_ROOT


%post
update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl %{_javadir}/%{name}.jar 25

%preun
{
  [ $1 -eq 0 ] || exit 0
  update-alternatives --remove jaxp_transform_impl %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%ghost %{_javadir}/jaxp_transform_impl.jar

%files manual
%defattr(-,root,root,-)
%doc doc/*.html

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name}

%files scripts
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/%{name}q
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}q.1*


