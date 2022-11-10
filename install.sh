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
#this seems necessary in the VM... 
if [ -d /nfs ]
	echo "install lhapdf6" | bin/mg5_aMC
fi
cd -

xmessage -buttons Ok:0 -nearmouse "Installing Delphes 3.5.0" -timeout 5 &

wget -qO- http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.5.0.tar.gz | tar zxv
cd Delphes-3.5.0
make -j 4
make -j 4 display
cd -

conda deactivate

xmessage -buttons Ok:0 -nearmouse "Downloading sample CMS data files, MC and ntuples" -timeout 5 &
mkdir LPHYS2131_data
if [ -d /nfs ] ; then
	echo "Creating symlinks to NFS."
	cd LPHYS2131_data
	ln -sf /nfs/data/LPHYS2131/ppChargedCurrentFullsim_ntuple.root
	ln -sf /nfs/data/LPHYS2131/ppNeutralCurrentFullsim_ntuple.root
	ln -sf /nfs/data/LPHYS2131/doubleMu2011_PAT.root
	ln -sf /nfs/data/LPHYS2131/doubleEl2011_ntuple.root
	ln -sf /nfs/data/LPHYS2131/doubleMu2011_ntuple.root 
	ln -sf /nfs/data/LPHYS2131/singleEl2011_ntuple.root
	ln -sf /nfs/data/LPHYS2131/singleMu2011_ntuple.root
	cd ..
else
	echo "Downloading files... this will take a while!"
	wget --no-check-certificate -nv https://cernbox.cern.ch/remote.php/dav/public-files/AInTeOOKfrcz1IA/LPHY2131tree_mc_W.root -O LPHYS2131_data/ppChargedCurrentFullsim_ntuple.root
	wget --no-check-certificate -nv https://cernbox.cern.ch/remote.php/dav/public-files/aa1I9COX7mqHUuo/LPHY2131tree_mc_Z.root -O LPHYS2131_data/ppNeutralCurrentFullsim_ntuple.root
	wget --no-check-certificate -nv https://cernbox.cern.ch/remote.php/dav/public-files/wO6JNKMgWEz6dBU/1C422B79-9235-E311-895A-0025905964C2_PAT.root -O LPHYS2131_data/doubleMu2011_PAT.root
	wget --no-check-certificate -nv https://cernbox.cern.ch/remote.php/dav/public-files/5Qy6eqba6Sxczuk/Ntuples_double_e.root -O LPHYS2131_data/doubleEl2011_ntuple.root
	wget --no-check-certificate -nv https://cernbox.cern.ch/remote.php/dav/public-files/gXhShqac0pdLXTA/Ntuples_Double_Mu_v2.root -O LPHYS2131_data/doubleMu2011_ntuple.root
	wget --no-check-certificate -nv https://cernbox.cern.ch/remote.php/dav/public-files/kZSKh8Ux3ZfsdOI/Ntuples_Single_e.root -O LPHYS2131_data/singleEl2011_ntuple.root
	wget --no-check-certificate -nv https://cernbox.cern.ch/remote.php/dav/public-files/hNXV6wUFj31j7NP/Ntuples_Single_Mu_v2.root -O LPHYS2131_data/singleMu2011_ntuple.root
fi
echo "DONE."

xmessage -buttons Ok:0 -nearmouse "DONE" -timeout 5 &

