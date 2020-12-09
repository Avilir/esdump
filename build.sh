#!/usr/bin/env bash

##############################################################################
#
# This script is for building the esdump container and push it to repository.
# it used the 'podman' for the build and accept the build TAG 
# from the user.
# without the tag the script will stop and exit with error.
# the script must be run from the top directory of the esdump.
#
# the repository that it will create is on quay, but this can be changed.
#
# Author : Avi Liani <alayani@redhat.com>
# Creation date : Dec,08,2020
#
##############################################################################

Tag=$1

if [[ ${Tag} == "" ]] ; then
	echo "Error: you mast give the tag name for the build !"
	exit 1
fi

Base_Repo=$2
if [[ ${Base_Repo} == "" ]] ; then
	echo "Error: you mast give the Base path for the repository!"
	exit 1
fi
Repo="${Base_Repo}/esdump"

CMD_TOOL='podman'  # if you want this can be replace with : 'docker'

echo "Build the container image"
${CMD_TOOL} build -t ${Repo}:${Tag} .
${CMD_TOOL} push ${Repo}:${Tag}
