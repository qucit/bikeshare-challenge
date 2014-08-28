#Author: TropoSco
#Date: 28-08-2014

#Check which packages are installed in Python and which version is running 


import sys

print (sys.version)
import pip 

print (sorted(["%s==%s" % (i.key, i.version) for i in pip.get_installed_distributions()]))#Print out the installed packages in Python