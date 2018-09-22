#!/bin/bash 
# This file defines local environments includin file path.
# Please add or modify to include your local environement. 
# Load this file, e.g., "source setenv/setenv.bashrc"

echo "####################"
echo "#     PYGROWTH     #"
echo "####################"

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

echo PYGROWTH_GITSOFT_PATH    = $PYGROWTH_GITSOFT_PATH
echo PYGROWTH_REPOSITORY_PATH = $PYGROWTH_REPOSITORY_PATH
