#
# MIT License
#
# (C) Copyright 2022 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
BuildRequires: systemd-rpm-macros
Name: craycli
License: MIT License
Summary: Cray Command Line Tool
Version: %(echo $VERSION)
Release: 1
Vendor: Cray Inc.
Group: Cloud
Source: %{name}-%{version}.tar.gz

%description
A CLI tool to interact with a cray system.

%prep
%setup -q
pip3 install pyinstaller

%build
pyinstaller --clean -y \
    --hidden-import toml \
    --hidden-import configparser \
    --hidden-import boto3 \
    --hidden-import websocket \
    --hidden-import argparse \
    --add-data ../build_version:cray \
    --add-data ../cray/modules:cray/modules \
    -p cray --onefile cray/cli.py -n cray --specpath dist

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 dist/cray %{buildroot}%{_bindir}/cray

%files
%license LICENSE
%{_bindir}/cray

%changelog
