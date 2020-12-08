#!/usr/bin/env bash

##############################################################################
#
# This script is for building the esdump container.
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

Repo="quay.io/avili/esdump"
# This is the repository that the container will push into.
# This need to be change if you want to use a different repository.
#Repo="docker-registry.upshift.redhat.com/esdump/esdump"

CMD_TOOL='podman'  # if you want this can be replace with : 'docker'


if [[ ${Tag} == "" ]] ; then
	echo "Error: you mast give the tag name for the build !"
	exit 1
fi

echo "Build the container image"
${CMD_TOOL} build -t ${Repo}:${Tag} .

