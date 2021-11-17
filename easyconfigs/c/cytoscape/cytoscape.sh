#!/bin/bash
#
# Run cytoscape from a jar file
# This script is a UNIX-only (i.e. Linux, Mac OS, etc.) version
#-------------------------------------------------------------------------------

# First, see if help (-h, --help) or version (-v, --version) command line arguments
# are specified. If so, display help or the current version and exit.

CYTOSCAPE_VERSION="Cytoscape version: 3.8.2"

if [[ $# > 0 ]]; then
	if [ $1 == "-h" -o $1 == "--help" ]; then
		cat <<-EOF
		
	Cytoscape Command-line Arguments
	================================
	usage: cytoscape.{sh|bat} [OPTIONS]
	 -h,--help             Print this message.
	 -v,--version          Print the version number.
	 -s,--session <file>   Load a cytoscape session (.cys) file.
	 -N,--network <file>   Load a network file (any format).
	 -P,--props <file>     Load cytoscape properties file (Java properties
	                       format) or individual property: -P name=value.
	 -V,--vizmap <file>    Load vizmap properties file (Cytoscape VizMap
	                       format).
	 -S,--script <file>    Execute commands from script file.
	 -R,--rest <port>      Start a rest service.
	 
	EOF
		exit 0
	fi
	
	if [ $1 == "-v" -o $1 == "--version" ]; then
		echo $CYTOSCAPE_VERSION
		exit 0
	fi
fi

DEBUG_PORT=12345

script_path="$(dirname -- $0)"
if [ -h $0 ]; then
	link="$(readlink $0)"
	script_path="$(dirname -- $link)"
fi


export JAVA_DEBUG_OPTS="-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=${DEBUG_PORT}"
if [ `uname` = "Darwin" ]; then
	CYTOSCAPE_MAC_OPTS="-Xdock:icon=$script_path/framework/cytoscape_logo_512.png -Xdock:name=Cytoscape"
	export JAVAFX_DIR="mac"
else
	export JAVAFX_DIR="linux"
fi

echo "JAVA_OPTS: $JAVA_OPTS"

# The Cytoscape home directory contains the "framework" directory
# and this script.
CYTOSCAPE_HOME_REL=$script_path
CYTOSCAPE_HOME_ABS=`cd "$CYTOSCAPE_HOME_REL"; pwd`

export KARAF_OPTS=-Dcytoscape.home="$CYTOSCAPE_HOME_ABS"\ "$CYTOSCAPE_MAC_OPTS"

karaf_data="${HOME}/CytoscapeConfiguration/3/karaf_data"
if [ -n ${USE_TEMP_KARAF+x} ] && [ -n ${CYTOSCAPE_CONFIG_HOME+x} ]; then
    log_suffix=`openssl rand -hex 8`
    karaf_data="${CYTOSCAPE_CONFIG_HOME}/CytoscapeConfiguration/3/karaf_data"
    temp_karaf_data="${karaf_data}.$log_suffix"
    cp -R $karaf_data $temp_karaf_data
    echo "cp -R $karaf_data $temp_karaf_data"
    karaf_data=$temp_karaf_data
fi

export KARAF_DATA=$karaf_data
mkdir -p "${KARAF_DATA}/tmp"

$script_path/framework/bin/karaf "$@"

if [ -n ${USE_TEMP_KARAF+x} ]; then
    rm -rf $karaf_data
fi

