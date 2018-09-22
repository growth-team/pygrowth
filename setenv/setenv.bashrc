#!/bin/bash 
# This file defines local envrionmental parameters, including 
# file path to the data repository. Please modify as you like.

echo "######################################"
echo "#     PYGROWTH ENVIRONMENT SETUP     #"
echo "######################################"

NAME=$(scutil --get ComputerName)
if [ $NAME = 'vicuna' ]; then
	echo '...setting for machine of "vicuna"'
	export PYGROWTH_GITSOFT_PATH="/Users/enoto/work/growth/soft/pygrowth"	
	export PYGROWTH_REPOSITORY_PATH="/Users/enoto/work/growth/data"		
elif [ $NAME = 'nebula' ]; then
	echo '...setting for machine of "nebula"'
	export PYGROWTH_GITSOFT_PATH="/Users/enoto/work/growth/soft/pygrowth"	
	export PYGROWTH_REPOSITORY_PATH="/Users/enoto/work/growth/data"		
elif [ $NAME = 'llama' ]; then
	echo '...setting for machine of "llama"'
	export PYGROWTH_GITSOFT_PATH="/Users/enoto/work/growth/soft/pygrowth"	
	export PYGROWTH_REPOSITORY_PATH="/Users/enoto/work/growth/data"				
elif [ $NAME = 'ramen' ]; then
	echo '...setting for machine of "ramen"'
	export PYGROWTH_GITSOFT_PATH="/Users/enoto/work/growth/soft/pygrowth"	
	export PYGROWTH_REPOSITORY_PATH="/Users/enoto/work/growth/data"					
else	
	echo 'no corresponding computer setup.'
fi

# Following two lines are preapred during the developping phase 
export PATH=$PYGROWTH_GITSOFT_PATH/pygrowth/common:$PATH
export PYTHONPATH=$PYGROWTH_GITSOFT_PATH:$PYTHONPATH

echo ComputerName    = $NAME
echo PYGROWTH_GITSOFT_PATH = $PYGROWTH_GITSOFT_PATH
echo PYGROWTH_REPOSITORY_PATH = $PYGROWTH_REPOSITORY_PATH
