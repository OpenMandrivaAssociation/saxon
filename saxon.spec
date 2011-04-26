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

%define resolverdir %{_sysconfdir}/java/resolver
%define gcj_support 1

Summary:        Java XSLT processor
Name:           saxon
Version:        6.5.5
Release:        %mkrel 1.2.6
Epoch:          0
License:        MPL
Group:          Development/Java
URL:            http://saxon.sourceforge.net/
Source0:        http://download.sf.net/saxon/saxon6-5-5.zip
Source1:        %{name}.saxon.script
Source2:        %{name}.build.script
Source3:        %{name}.1
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  jdom >= 0:1.0
BuildRequires:  ant
Requires:       xml-commons-jaxp-1.3-apis
Requires:       jpackage-utils >= 0:1.6
Requires:       jdom >= 0:1.0
Requires:       jaxp_parser_impl
Requires:       update-alternatives
Provides:       jaxp_transform_impl
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel >= 0:1.4.2
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The SAXON package is a collection of tools for processing XML documents.
The main components are:
- An XSLT processor, which implements the Version 1.0 XSLT and XPath
  Recommendations from the World Wide Web Consortium, found at
  http://www.w3.org/TR/1999/REC-xslt-19991116 and
  http://www.w3.org/TR/1999/REC-xpath-19991116 with a number of powerful
  extensions. This version of Saxon also includes many of the new features
  defined in the XSLT 1.1 working draft, but for conformance and portability
  reasons these are not available if the stylesheet header specifies
  version="1.0".
- A Java library, which supports a similar processing model to XSL, but allows
  full programming capability, which you need if you want to perform complex
  processing of the data or to access external services such as a relational
  database.
So you can use SAXON with any SAX-compliant XML parser by writing XSLT
stylesheets, by writing Java applications, or by any combination of the two.

%package        aelfred
Summary:        Java XML parser
Group:          Development/Java
Requires:       xml-commons-jaxp-1.3-apis

%description    aelfred
A slightly improved version of the AElfred Java XML parser from Microstar.

%package        manual
Summary:        Manual for %{name}
Group:          Development/Java

%description    manual
Manual for %{name}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
BuildRequires:  java-javadoc
BuildRequires:  jdom-javadoc >= 0:1.0
Requires:       java-javadoc
Requires:       jdom-javadoc >= 0:1.0

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demos for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%package        jdom
Summary:        JDOM support for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jdom >= 0:1.0

%description    jdom
JDOM support for %{name}.

%package        scripts
Summary:        Utility scripts for %{name}
Group:          Development/Java
Requires:       jpackage-utils >= 0:1.6
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    scripts
Utility scripts for %{name}.

%prep
%setup -q -c
%{_bindir}/unzip -q source.zip
%{__cp} -a %{SOURCE2} ./build.xml
# cleanup unnecessary stuff we'll build ourselves
%{__rm} -v *.jar
# fix newlines in docs
for i in doc/*.html; do
    %{__perl} -pi -e 's/\r$//g' $i
done

%build
export CLASSPATH=$(build-classpath xml-commons-jaxp-1.3-apis jdom)
export OPT_JAR_LIST=:
%{ant} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -Djdom.javadoc=%{_javadocdir}/jdom

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a build/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

%{__cp} -a build/lib/%{name}-aelfred.jar \
    %{buildroot}%{_javadir}/%{name}-aelfred-%{version}.jar

%{__cp} -a build/lib/%{name}-jdom.jar \
    %{buildroot}%{_javadir}/%{name}-jdom-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do \
    %{__ln_s} ${jar} `echo $jar | %{__sed} "s|-%{version}||g"`; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a build/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# demo
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__cp} -a samples/* %{buildroot}%{_datadir}/%{name}

# scripts
%{__mkdir_p} %{buildroot}%{_bindir}
%{__sed} 's,__RESOLVERDIR__,%{resolverdir},' < %{SOURCE1} \
  > %{buildroot}%{_bindir}/%{name}
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__sed} 's,__RESOLVERDIR__,%{resolverdir},' < %{SOURCE3} \
  > %{buildroot}%{_mandir}/man1/%{name}.1

%if 0
# jaxp_transform_impl ghost symlink
%{__ln_s} %{_sysconfdir}/alternatives \
  %{buildroot}%{_javadir}/jaxp_transform_impl.jar
%endif

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%post
%{_sbindir}/update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl %{_javadir}/%{name}.jar 25

%preun
{
  [ $1 -eq 0 ] || exit 0
  %{_sbindir}/update-alternatives --remove jaxp_transform_impl %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if 0
%ghost %{_javadir}/jaxp_transform_impl.jar
%endif
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/java.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/java.so
%attr(-,root,root) %{_libdir}/gcj/%{name}/saxon-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/saxon-%{version}.jar.so
%endif

%files aelfred
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-aelfred*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/saxon-aelfred-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/saxon-aelfred-%{version}.jar.so
%endif

%files jdom
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-jdom*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/saxon-jdom-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/saxon-jdom-%{version}.jar.so
%endif

%files manual
%defattr(0644,root,root,0755)
%doc doc/*.html

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%files scripts
%defattr(0755,root,root,0755)
%{_bindir}/%{name}
%attr(0644,root,root) %{_mandir}/man1/%{name}.1*
