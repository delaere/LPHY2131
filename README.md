# LPHY2131
Material for the LPHY2131 lab

To install, follow the instructions below:

1. Download the virtual machine from http://opendata.cern.ch/VM/CMS#how
  - Increase the RAM to 2GB (optional. The minimum is 1GB)
  - Enable 3D acceleration
  - after booting, change the keyboard layout (if needed)
2. In a terminal (black icon at the bottom left of the screen), run the following two commands. Note that the second command starts with a dot followed by a space.
  - git clone https://github.com/delaere/LPHY2131.git
  - . LPHY2131/install.sh

This prepares the environment for the lab: 
- install CMSSW 4.2.8 (used for 2010 data processing)
- install CMSSW 7.1.1 (used to setup the analysis environment)
- install MadGraph 5
- install Delphes 3.3
