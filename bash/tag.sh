
#set -e

PROG=${0##*/}
SCRIPTS_DIR=$(realpath ${0%/*})

usage()
{
    echo "Usage: $PROG <tag>" >&2
    echo "    Tag and push the tag of toolchain repo and it's submodules." >&2
}

case "$1" in
	-h | --help) usage ; exit ;;
esac


if [ $# -ne 1 ]
then
    usage
    exit 1
fi

if [[ $1 == -* ]]
then
    echo "Do not start tag with -" 
    usage
    exit 1
fi

if [ -z $T64_DEV_HOME ]
then
    echo "T64_DEV_HOME is not defined" >&2
    exit 1
fi

tag=$1
echo "Going to tag the repos with '$tag' tag."

toolchain_dir=$T64_DEV_HOME/*/toolchain

cd $toolchain_dir 
git show-ref --tags  --quiet --verify -- refs/tags/$tag
if [ "$?" != "0" ] ; then
    echo "toolchain doesnt have tag $tag"
else
    echo "toolchain has tag $tag"
fi
git submodule foreach 'git show-ref --tags  --quiet --verify -- refs/tags/$tag ; if [ "$?" != "0" ] ; then echo "not present"; else echo "present"; fi'

