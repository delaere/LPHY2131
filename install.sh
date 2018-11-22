#!/bin/env sh

#Download the virtual machine from http://opendata.cern.ch/VM/CMS#how
#after booting, change the keyboard layout (if needed)
#git clone https://github.com/delaere/LPHY2131.git
#. LPHY2131/install.sh

xmessage -buttons Ok:0 -nearmouse "Downloading sample CMS data files, MC and ntuples" -timeout 5 &
mkdir LPHY2131_data
wget --no-check-certificate https://cernbox.cern.ch/index.php/s/AInTeOOKfrcz1IA/download?x-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOiIyMDE4LTExLTIyVDE1OjU2OjQ3LjkwNzM4MzQwMSswMTowMCIsImV4cGlyZXMiOjAsImlkIjoiODUwNDciLCJpdGVtX3R5cGUiOjAsIm10aW1lIjoxNTEwMTUwNDg2LCJvd25lciI6ImRlbGFlciIsInBhdGgiOiJlb3Nob21lLWQ6MTAxMDYwMjM0MTkzMTQxNzYiLCJwcm90ZWN0ZWQiOmZhbHNlLCJyZWFkX29ubHkiOnRydWUsInNoYXJlX25hbWUiOiJMUEhZMjEzMXRyZWVfbWNfVy5yb290IiwidG9rZW4iOiJBSW5UZU9PS2ZyY3oxSUEifQ.kLy1eOGawZ8x1x548WnRLwkO_DTinhB5Y0WETLMHUZM -O LPHY2131_data/ppChargedCurrentFullsim_ntuple.root
wget --no-check-certificate https://cernbox.cern.ch/index.php/s/aa1I9COX7mqHUuo/download?x-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOiIyMDE4LTExLTIyVDE1OjU3OjUyLjc0NDY2NzM3NCswMTowMCIsImV4cGlyZXMiOjAsImlkIjoiODUwNDUiLCJpdGVtX3R5cGUiOjAsIm10aW1lIjoxNTEwMTUwMzMwLCJvd25lciI6ImRlbGFlciIsInBhdGgiOiJlb3Nob21lLWQ6MTAxMDYwMjM2ODc3NDk2MzIiLCJwcm90ZWN0ZWQiOmZhbHNlLCJyZWFkX29ubHkiOnRydWUsInNoYXJlX25hbWUiOiJMUEhZMjEzMXRyZWVfbWNfWi5yb290IiwidG9rZW4iOiJhYTFJOUNPWDdtcUhVdW8ifQ.PvDe3XcUsWquciLFNkQch1oj2AYlR2WwJ2dOqPOwTPU -O LPHY2131_data/ppNeutralCurrentFullsim_ntuple.root
wget --no-check-certificate https://cernbox.cern.ch/index.php/s/wO6JNKMgWEz6dBU/download?x-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOiIyMDE4LTExLTIyVDE1OjUxOjMxLjIzMzI0NTE2NCswMTowMCIsImV4cGlyZXMiOjAsImlkIjoiODUwNTAiLCJpdGVtX3R5cGUiOjAsIm10aW1lIjoxNTEwMTUwNjI2LCJvd25lciI6ImRlbGFlciIsInBhdGgiOiJlb3Nob21lLWQ6MTAxMDYwMjMxNTA4Nzg3MjAiLCJwcm90ZWN0ZWQiOmZhbHNlLCJyZWFkX29ubHkiOnRydWUsInNoYXJlX25hbWUiOiIxQzQyMkI3OS05MjM1LUUzMTEtODk1QS0wMDI1OTA1OTY0QzJfUEFULnJvb3QiLCJ0b2tlbiI6IndPNkpOS01nV0V6NmRCVSJ9.ytyDlLnYuLraj54XXhSaUgN2EPEkTkRIf4MBdLw6clk -O LPHY2131_data/doubleMu2011_PAT.root
wget --no-check-certificate https://cernbox.cern.ch/index.php/s/5Qy6eqba6Sxczuk/download?x-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOiIyMDE4LTExLTIyVDE1OjU4OjIyLjk0NDUyMTc0MSswMTowMCIsImV4cGlyZXMiOjAsImlkIjoiODUwNDkiLCJpdGVtX3R5cGUiOjAsIm10aW1lIjoxNTEwMTUwNjEwLCJvd25lciI6ImRlbGFlciIsInBhdGgiOiJlb3Nob21lLWQ6MTAxMDYwMjUyOTgzNjIzNjgiLCJwcm90ZWN0ZWQiOmZhbHNlLCJyZWFkX29ubHkiOnRydWUsInNoYXJlX25hbWUiOiJOdHVwbGVzX2RvdWJsZV9lLnJvb3QiLCJ0b2tlbiI6IjVReTZlcWJhNlN4Y3p1ayJ9.7-9lKltVV-spyn22hM90JeTyh03hTMRcxQE_mauo_Ss -O LPHY2131_data/doubleEl2011_ntuple.root
wget --no-check-certificate https://cernbox.cern.ch/index.php/s/gXhShqac0pdLXTA/download?x-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOiIyMDE4LTExLTIyVDE1OjU5OjAxLjQyNjY1NTAxMSswMTowMCIsImV4cGlyZXMiOjAsImlkIjoiMzk1NTYiLCJpdGVtX3R5cGUiOjAsIm10aW1lIjoxNDc5OTk5MjUxLCJvd25lciI6ImRlbGFlciIsInBhdGgiOiJlb3Nob21lLWQ6MTAxMDYwMjQyMjQ2MjA1NDQiLCJwcm90ZWN0ZWQiOmZhbHNlLCJyZWFkX29ubHkiOnRydWUsInNoYXJlX25hbWUiOiJOdHVwbGVzX0RvdWJsZV9NdV92Mi5yb290IiwidG9rZW4iOiJnWGhTaHFhYzBwZExYVEEifQ.0RDS5F7JciNq0CTDgiDmZymVtqkhJfB6i3qji1nTJxs -O LPHY2131_data/doubleMu2011_ntuple.root
wget --no-check-certificate https://cernbox.cern.ch/index.php/s/kZSKh8Ux3ZfsdOI/download?x-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOiIyMDE4LTExLTIyVDE1OjU5OjMwLjYyMzE0NjY1NCswMTowMCIsImV4cGlyZXMiOjAsImlkIjoiODUwNTEiLCJpdGVtX3R5cGUiOjAsIm10aW1lIjoxNTEwMTUwNjYyLCJvd25lciI6ImRlbGFlciIsInBhdGgiOiJlb3Nob21lLWQ6MTAxMDYwMjUwMjk5MjY5MTIiLCJwcm90ZWN0ZWQiOmZhbHNlLCJyZWFkX29ubHkiOnRydWUsInNoYXJlX25hbWUiOiJOdHVwbGVzX1NpbmdsZV9lLnJvb3QiLCJ0b2tlbiI6ImtaU0toOFV4M1pmc2RPSSJ9.19rDoGVP753OD9HqYCpMThYwqRAcu-xiGOaZwLnlzkQ -O LPHY2131_data/singleEl2011_ntuple.root
wget --no-check-certificate https://cernbox.cern.ch/index.php/s/hNXV6wUFj31j7NP/download?x-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOiIyMDE4LTExLTIyVDE1OjU5OjU4LjI5NTYwNDczMSswMTowMCIsImV4cGlyZXMiOjAsImlkIjoiMzk1NTgiLCJpdGVtX3R5cGUiOjAsIm10aW1lIjoxNDc5OTk5MzAyLCJvd25lciI6ImRlbGFlciIsInBhdGgiOiJlb3Nob21lLWQ6MTAxMDYwMjQ3NjE0OTE0NTYiLCJwcm90ZWN0ZWQiOmZhbHNlLCJyZWFkX29ubHkiOnRydWUsInNoYXJlX25hbWUiOiJOdHVwbGVzX1NpbmdsZV9NdV92Mi5yb290IiwidG9rZW4iOiJoTlhWNndVRmozMWo3TlAifQ.fF-h58Xis7-WT2LHeC9wcL-Dvz9JubJtbZJ27lVe1ak -O LPHY2131_data/singleMu2011_ntuple.root

xmessage -buttons Ok:0 -nearmouse "Installing CMSSW 5.3.32 (used for 2011 data processing)" -timeout 5 &
cmsrel CMSSW_5_3_32
cd CMSSW_5_3_32/src
cp -r ~/LPHY2131/CMSSW Labo
cmsenv
scram b
cd ../..

xmessage -buttons Ok:0 -nearmouse "Installing CMSSW 7.1.1 (used to setup the analysis environment)" -timeout 5 &
export SCRAM_ARCH=slc6_amd64_gcc472
cmsrel CMSSW_7_1_1
cd CMSSW_7_1_1/src
cmsenv
cd ../..

xmessage -buttons Ok:0 -nearmouse "Installing MadGraph 5" -timeout 5 &
wget --no-check-certificate -qO- https://launchpad.net/mg5amcnlo/2.0/2.4.x/+download/MG5_aMC_v2.4.3.tar.gz | tar zxv
cd MG5_aMC_v2_4_3/
sed -i -e s/6500/3500/g ./madgraph/various/banner.py
echo "n" | bin/mg5_aMC
echo "install pythia-pgs" | bin/mg5_aMC
cd ..

xmessage -buttons Ok:0 -nearmouse "Installing Delphes 3.3.2" -timeout 5 &
wget -qO- http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.3.2.tar.gz | tar zxv
cd Delphes-3.3.2
make -j 4
make -j 4 display
cd

xmessage -buttons Ok:0 -nearmouse "Update the VM..." -timeout 5 &
sudo cernvm-update -a

xmessage -buttons Ok:0 -nearmouse "Install LibreOffice..." -timeout 5 &
sudo yum install libreoffice-writer libreoffice-calc -y

xmessage -buttons Ok:0 -nearmouse "DONE" -timeout 5 &
