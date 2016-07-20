#/bin/env bash

# some checks
if [ ! -f ../Delphes-3.3.2/delpheAnalysisZ.root ]; then
    echo "delpheAnalysisZ.root File not found!"
    echo "Did you complete lab 1?"
    exit
fi
if [ ! -f ../Delphes-3.3.2/delpheAnalysisW.root ]; then
    echo "delpheAnalysisW.root File not found!"
    echo "Did you complete lab 1?"
    exit
fi
#switch the "NtupesfilesMuons" with the path of the list of Ntuples files available on the virtual machine
if [ ! -f ../data/NtuplesfilesMuons ]; then
    echo "NtuplesfilesMuons File not found!"
    echo "This should have been downloaded by the installation script."
    exit
fi
#switch the "NtupesfilesElectrons" with the path of the list of Ntuples files available on the virtual machine
if [ ! -f ../data/NtuplesfilesElectrons ]; then
    echo "NtuplesfilesElectrons File not found!"
    echo "This should have been downloaded by the installation script."
    exit
fi

# create sym links
ln -s ../Delphes-3.3.2/delpheAnalysisZ.root labo2/
#insert sym links for the input Ntuples datafiles in the labo2 directory for electrons and muons
ln -s ../data/NtuplesfilesMuons labo2/
ln -s ../data/NtuplesfilesElectrons labo2/
ln -s ../Delphes-3.3.2/delpheAnalysisW.root labo3/
#create sym links for the input Ntuples datafiles in the labo3 directory for electrons and muons
ln -s ../data/NtuplesfilesMuons labo3/
ln -s ../data/NtuplesfilesElectrons labo3/

echo "Analysis workspace ready"
