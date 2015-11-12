#!/bin/env sh

#Download the virtual machine from http://opendata.cern.ch/VM/CMS#how
#Increase the RAM to 2GB
#Enable 3D acceleration
#after booting, change the keyboard layout (if needed)
#git clone https://github.com/delaere/LPHY2131.git
#. LPHY2131/install.sh

xmessage -buttons Ok:0 -nearmouse "Downloading sample CMS data file" -timeout 5 &
mkdir data
wget https://cernbox.cern.ch/index.php/s/nFgkXD5e1W9KEJX/download -O data/Mu2010data_sample.root
wget https://cernbox.cern.ch/index.php/s/VHkv9wHTK4r9whl/download -O data/Electron2010data_500files_1.root
xmessage -buttons Ok:0 -nearmouse "Installing CMSSW 4.2.8 (used for 2010 data processing)" -timeout 5 &
cmsrel CMSSW_4_2_8
cd CMSSW_4_2_8/src
cp -r ~/LPHY2131/CMSSW LPHY2131
cmsenv
scram b
cd ../..
xmessage -buttons Ok:0 -nearmouse "Installing CMSSW 7.1.1 (used to setup the analysis environment)" -timeout 5 &
export SCRAM_ARCH=slc5_amd64_gcc481
cmsrel CMSSW_7_1_1
cd CMSSW_7_1_1/src
cmsenv
cd ../..
xmessage -buttons Ok:0 -nearmouse "Installing MadGraph 5" -timeout 5 &
wget --no-check-certificate -qO- https://launchpad.net/mg5amcnlo/2.0/2.3.0/+download/MG5_aMC_v2.3.3.tar.gz | tar zxv
cd MG5_aMC_v2_3_3/
echo "install pythia-pgs" | bin/mg5_aMC
cd ..
xmessage -buttons Ok:0 -nearmouse "Installing Delphes 3.3.0" -timeout 5 &
wget -qO- http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.3.0.tar.gz | tar zxv 
cd Delphes-3.3.0
make -j 4
make -j 4 display
cd
xmessage -buttons Ok:0 -nearmouse "DONE" -timeout 5 &

