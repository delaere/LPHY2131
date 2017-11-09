#/bin/env bash

# some checks
if [ ! -f ../../Delphes-3.3.2/delpheAnalysisZ.root ]; then
    echo "delpheAnalysisZ.root File not found!"
    echo "Did you complete lab 1?"
    exit
fi
if [ ! -f ../../Delphes-3.3.2/delpheAnalysisW.root ]; then
    echo "delpheAnalysisW.root File not found!"
    echo "Did you complete lab 1?"
    exit
fi
#switch the "NtupesfilesMuons" with the path of the list of Ntuples files available on the virtual machine
if [ ! -f ../../LPHY2131_data/doubleMu2011_ntuple.root ]; then
    echo "doubleMu2011_ntuple.root File not found!"
    echo "This should have been downloaded by the installation script."
    exit
fi
#switch the "NtupesfilesElectrons" with the path of the list of Ntuples files available on the virtual machine
if [ ! -f ../../LPHY2131_data/doubleEl2011_ntuple.root ]; then
    echo "doubleEl2011_ntuple.root File not found!"
    echo "This should have been downloaded by the installation script."
    exit
fi

# create sym links
ln -sf ../../../Delphes-3.3.2/delpheAnalysisZ.root labo2/
ln -sf ../../../LPHY2131_data/doubleMu2011_ntuple.root labo2/
ln -sf ../../../LPHY2131_data/doubleEl2011_ntuple.root labo2/
ln -sf ../../../LPHY2131_data/ppNeutralCurrentFullsim_ntuple.root labo2/
ln -sf ../../../Delphes-3.3.2/delpheAnalysisW.root labo3/
ln -sf ../../../LPHY2131_data/singleMu2011_ntuple.root labo3/
ln -sf ../../../LPHY2131_data/singleEl2011_ntuple.root labo3/
ln -sf ../../../LPHY2131_data/ppChargedCurrentFullsim_ntuple.root labo3/

echo "Analysis workspace ready"
