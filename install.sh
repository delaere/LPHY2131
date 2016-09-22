#i#!/bin/env sh

#Download the virtual machine from http://opendata.cern.ch/VM/CMS#how
#after booting, change the keyboard layout (if needed)
#git clone https://github.com/delaere/LPHY2131.git
#cd LPHY2131
#. install.sh

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
echo "install pythia-pgs" | bin/mg5_aMC
cd ..

xmessage -buttons Ok:0 -nearmouse "Installing Delphes 3.3.2" -timeout 5 &
wget -qO- http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.3.2.tar.gz | tar zxv
cd Delphes-3.3.2
make -j 4
make -j 4 display
cd
xmessage -buttons Ok:0 -nearmouse "DONE" -timeout 5 &
