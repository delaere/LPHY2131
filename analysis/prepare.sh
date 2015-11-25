#/bin/env bash

# some checks
if [ ! -f ../../Delphes-3.3.0/delpheAnalysisZ.root ]; then
    echo "delpheAnalysisZ.root File not found!"
    echo "Did you complete lab 1?"
    exit
fi
if [ ! -f ../../Delphes-3.3.0/delpheAnalysisW.root ]; then
    echo "delpheAnalysisW.root File not found!"
    echo "Did you complete lab 1?"
    exit
fi
if [ ! -f ../../data/Mu2010data_flat.root ]; then
    echo "Mu2010data_flat.root File not found!"
    echo "This should have been downloaded by the installation script."
    exit
fi
if [ ! -f ../../data/Electron2010data_flat.root ]; then
    echo "Electron2010data_flat.root File not found!"
    echo "This should have been downloaded by the installation script."
    exit
fi

# create sym links
ln -s ../../Delphes-3.3.0/delpheAnalysisZ.root labo2/
ln -s ../../data/Mu2010data_flat.root labo2/
ln -s ../../data/Electron2010data_flat.root labo2/
ln -s ../../Delphes-3.3.0/delpheAnalysisW.root labo3/
ln -s ../../data/Mu2010data_flat.root labo3/
ln -s ../../data/Electron2010data_flat.root labo3/

echo "Analysis workspace ready"
