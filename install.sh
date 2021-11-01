#!/bin/env sh

#Download the virtual machine from http://opendata.cern.ch/VM/CMS#how
#after booting, change the keyboard layout (if needed)
#git clone https://github.com/delaere/LPHY2131.git LPHYS2131
#. LPHYS2131/install.sh

xmessage -buttons Ok:0 -nearmouse "Downloading sample CMS data files, MC and ntuples" -timeout 5 &
mkdir LPHYS2131_data
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/AInTeOOKfrcz1IA/download -O LPHYS2131_data/ppChargedCurrentFullsim_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/aa1I9COX7mqHUuo/download -O LPHYS2131_data/ppNeutralCurrentFullsim_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/wO6JNKMgWEz6dBU/download -O LPHYS2131_data/doubleMu2011_PAT.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/5Qy6eqba6Sxczuk/download -O LPHYS2131_data/doubleEl2011_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/gXhShqac0pdLXTA/download -O LPHYS2131_data/doubleMu2011_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/kZSKh8Ux3ZfsdOI/download -O LPHYS2131_data/singleEl2011_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/hNXV6wUFj31j7NP/download -O LPHYS2131_data/singleMu2011_ntuple.root

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

xmessage -buttons Ok:0 -nearmouse "Installing Jupyter and required modules" -timeout 5 &
echo -e 'password\n' | sudo -S -s yum install python3-devel -y
sudo pip3 install jupyterlab
sudo pip3 install mplhep uproot awkward probfit

xmessage -buttons Ok:0 -nearmouse "Installing LibreOffice" -timeout 5 &
sudo -S -s yum install libreoffice-writer libreoffice-calc -y

xmessage -buttons Ok:0 -nearmouse "DONE" -timeout 5 &
