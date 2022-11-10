# LPHYS2131

This project assembles material for the [LPHYS2131 lab at UCLouvain](https://uclouvain.be/cours-2021-lphys2131). 
It also documents the three sessions of the laboratory and provides some additional information.

The results that are obtained in this lab can be compared to the published cross-section measurement for the Z and W at the LHC, at 7TeV, by the CMS collaboration:
[Measurement of the Inclusive W and Z Production Cross Sections in pp Collisions at sqrt(s) = 7 TeV](http://arxiv.org/abs/1107.4789)

## Credits:

Thanks to Liliya Milenska, Gilles Parez and Martin Michel for their help in preparing this activity during their internship in summer 2015.
Thanks to Victor Massart and Julien Touchèque for their help in porting the lab to 2011 data in summer 2016.
Thanks to Jérôme de Favereau, Pavel Demin and Michele Selvaggi for their support.


# Instructions to install the virtual machine

Ressources are available one [UCLouvain OneDrive](https://uclouvain-my.sharepoint.com/:f:/g/personal/pavel_demin_uclouvain_be/EpNisUlEWipMmZSxd7MPi80BF-31nBaOelQ8NBE9JVQNpA).

1. Install VirtualBox

Installers for Windows and Mac OSX are in the same directory.

2. Copy virtual machine file 'LPHYS2131.vdi' to your computer

3. Start VirtualBox

4. Create a new virtual machine using the provided image:
  1. Click the blue 'New' icon
  2. Pick a name for the machine and select 'Linux' and 'Debian (64-bit)'
  3. Set the memory size to at least 4096 MB
  4. Select 'Use an existing hard disk file' and choose 'LPHYS2131.vdi'
  5. Select the newly created virtual machine and click the yellow 'Settings' icon
  6. Select 'Display' and set 'Graphics Controller' to 'VBoxVGA'
  7. Click 'OK'
  8. Select the newly created virtual machine and click the green 'Start' icon

Now, you should be in Linux session with the software required for LPHYS2131.
To install, follow the instructions below:

1. Open the Virtual Machine
2. In a terminal, run the following two commands.
  - git clone https://github.com/delaere/LPHY2131.git LPHYS2131
  - LPHYS2131/install.sh

This prepares the environment for the lab: 
- downloads samples files and example scripts
- installs CMSSW 5.3.32 (used for 2011 data processing)
- installs and configures MadGraph 5
- installs Delphes 3.5.0

