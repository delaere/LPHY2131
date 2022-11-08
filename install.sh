# git clone https://github.com/delaere/LPHY2131 LPHYS2131
# source LPHYS2131/install.sh

apptainer exec -B /cvmfs /cvmfs/cernvm-prod.cern.ch/cvm3 /bin/bash <<- EOF_CMSSW

xmessage -buttons Ok:0 -nearmouse "Installing CMSSW 5.3.32 (used for 2011 data processing)" -timeout 5 &

. /cvmfs/cms.cern.ch/cmsset_default.sh

export SCRAM_ARCH=slc6_amd64_gcc472
cmsrel CMSSW_5_3_32
cd CMSSW_5_3_32/src
cp -r ../../LPHYS2131/CMSSW Labo
cmsenv
scram b
cd -

EOF_CMSSW

conda activate cms-analysis

xmessage -buttons Ok:0 -nearmouse "Installing MadGraph 5" -timeout 5 &

wget -qO- https://launchpad.net/mg5amcnlo/3.0/3.4.x/+download/MG5_aMC_v2.9.12.tar.gz | tar zxv
cd MG5_aMC_v2_9_12
sed -i '/import os/aos.unsetenv("PYTHIA8DATA")' bin/mg5_aMC
sed -i 's/6500/3500/g' ./madgraph/various/banner.py
echo "install pythia8" | bin/mg5_aMC
cd -

xmessage -buttons Ok:0 -nearmouse "Installing Delphes 3.5.0" -timeout 5 &

wget -qO- http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.5.0.tar.gz | tar zxv
cd Delphes-3.5.0
make -j 4
make -j 4 display
cd -

conda deactivate

xmessage -buttons Ok:0 -nearmouse "DONE" -timeout 5 &

