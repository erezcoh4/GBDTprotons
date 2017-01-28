# visual
#———————————————————————————————————————————————————————————————————————————
PS1="$(pwd) 🚀 |"


# Aliases 
#———————————————————————————————————————————————————————————————————————————
# ssh…
alias taudaq='echo pwd=Ycoda734;ssh -Y taudaq@taudaq'
alias taudaq2='echo pwd=1ppmgf;ssh -Y l_daq@taudaq2'
alias JLAB='echo pwd=Ff$123456;ssh -Y cohen@login.jlab.org'
alias LINGO2='echo pwd=Dd123456;ssh -Y erezcoh4@lingo2.tau.ac.il'
alias Deuteron='echo pwd=ere2014z;ssh -Y erez@deuteron'
alias Electron='echo pwd= Aa\$123456;ssh -Y ecohen@electron.tau.ac.il'
alias Helion='echo pwd= ere2014z;ssh -Y erez@helion'
alias Nudot='echo pwd= Aa$123456;ssh -Y ecohen@nudot.lns.mit.edu'
alias Davis='echo pwd= Aa$123456;ssh -Y ecohen@davis.physics.lsa.umich.edu'

# git…
alias GitAdd='git add .'
alias GitCommit='git commit -m "$(date)"'
alias GitPush='git push'
alias gitpush='GitAdd && GitCommit && GitPush'

# ls…
alias ls='ls -G'
alias ll='ls -lth'

# python
alias ipynb='ipython notebook'

# my software
alias Energy2Momentum='python /Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac/energy2momentum.py'



# Environmental variables
#———————————————————————————————————————————————————————————————————————————
export MyJlab=cohen@login.jlab.org
export MyHelion=erez@helion
export DecTestMUSE=~/MUSE/Tests/Dec-14
export DataMiningAnaFiles=/Users/erezcohen/Desktop/DataMining/AnaFiles
export SIMCFiles=/Users/erezcohen/Desktop/A3/Simulation/simc_files
export AnalysisTreesAna=/Users/erezcohen/larlite/UserDev/AnalysisTreesInformation/AnaTreesPackage







# Directions to specific locations 
#———————————————————————————————————————————————————————————————————————————

alias MUSEBuild=' cd ~/muse/build; open -a xcode /Users/erezcohen/muse/src/plugins/analysis/testbeamanalysis/src/*.cpp /Users/erezcohen/muse/src/plugins/analysis/scifi_analysis/src/*.cpp'

alias OpenSoftware='open *.cxx  *.h mac/*.py'
alias MySoftware='cd ~/larlite/UserDev/mySoftware/MySoftwarePackage; OpenSoftware; echo now in my software… '





echo set environmental variables and Aliases
source $HOME/.profile


export PATH="/opt/local/bin:/opt/local/sbin:$PATH"




# shortcuts
#———————————————————————————————————————————————————————————————————————————
alias GoEG2='cdtop; cd UserDev/CLASEG2DataMining/EG2DataMiningPackage; OpenSoftware; echo now in CLASEG2…'
alias GoAnaTrees='cdtop; cd UserDev/AnalysisTreesInformation/AnaTreesPackage; OpenSoftware; echo now in AnalysisTreesInformation…'
alias GoGBDTs='cdtop; cd UserDev/GBDTprotons/GBDTprotonPackage; OpenSoftware; echo now in GBDTs…'

alias MissionsProjects='open /Users/erezcohen/Desktop/Projects/General/missions_projects.numbers'
