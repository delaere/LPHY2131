#!/bin/env sh

#Download the virtual machine from http://opendata.cern.ch/VM/CMS#how
#after booting, change the keyboard layout (if needed)
#git clone https://github.com/delaere/LPHY2131.git LPHYS2131
#LPHYS2131/install.sh

TMPRC=$(mktemp)
cat > $TMPRC << EOF
PS1='\[\e]2;CMS Shell\a\]\[\e[1;32m\]CMS Shell >\[\e[m\]\[\e[0;32m\] '
. /cvmfs/cms.cern.ch/cmsset_default.sh

xmessage -buttons Ok:0 -nearmouse "Installing CMSSW 5.3.32 (used for 2011 data processing)" -timeout 5 &
cmsrel CMSSW_5_3_32
cd CMSSW_5_3_32/src
cp -r ~/LPHYS2131/CMSSW Labo
cmsenv
scram b
cd ../..

xmessage -buttons Ok:0 -nearmouse "Installing CMSSW 7.1.1 (used to setup the analysis environment)" -timeout 5 &
export SCRAM_ARCH=slc6_amd64_gcc481
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
exit
EOF
echo 'HISTFILE=~/.cms_history' >> $TMPRC
echo '. /cvmfs/cms.cern.ch/cmsset_default.sh' >> $TMPRC
cvmfs_config probe
echo "Starting up CMS shell..."
TZ_SRC=$(readlink /etc/localtime)
TZ_DST=$(readlink /cvmfs/cernvm-prod.cern.ch/cvm3/etc/localtime)
singularity exec   -B $TZ_SRC:$TZ_DST   -B /usr/share/X11/xkb/rules   -B /etc/mtab   -B /etc/cvmfs   -B /etc/cms   -B /cvmfs   -B /eos   /cvmfs/cernvm-prod.cern.ch/cvm3 /bin/bash --noprofile --rcfile $TMPRC
rm -f $TMPRC

xmessage -buttons Ok:0 -nearmouse "Installing LibreOffice, Jupyter and required modules" -timeout 5 &
echo -e 'password\n' | sudo -S yum install libreoffice-writer libreoffice-calc python3-devel -y
echo -e 'password\n' | sudo -S pip3 install jupyterlab mplhep uproot awkward probfit

xmessage -buttons Ok:0 -nearmouse "Downloading sample CMS data files, MC and ntuples" -timeout 5 &
mkdir LPHYS2131_data
echo "Downloading files... this will take a while!"
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/AInTeOOKfrcz1IA/download -O LPHYS2131_data/ppChargedCurrentFullsim_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/aa1I9COX7mqHUuo/download -O LPHYS2131_data/ppNeutralCurrentFullsim_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/wO6JNKMgWEz6dBU/download -O LPHYS2131_data/doubleMu2011_PAT.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/5Qy6eqba6Sxczuk/download -O LPHYS2131_data/doubleEl2011_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/gXhShqac0pdLXTA/download -O LPHYS2131_data/doubleMu2011_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/kZSKh8Ux3ZfsdOI/download -O LPHYS2131_data/singleEl2011_ntuple.root
wget --no-check-certificate -nv https://cernbox.cern.ch/index.php/s/hNXV6wUFj31j7NP/download -O LPHYS2131_data/singleMu2011_ntuple.root

xmessage -buttons Ok:0 -nearmouse "DONE" -timeout 5 &
