#! /bin/sh

# Read in the environment
# TODO: why is ZENHOME unknown??
if [ -z "$ZENHOME" ]; then
    ZENHOME=/opt/zenoss
fi

ENVFILE="$ZENHOME/rancid/etc/rancid.conf"
. $ENVFILE

#echo "vars: $*" >&2;
#exit 1

# RCS system
RCSSYS=${RCSSYS:=cvs};
if [ $RCSSYS != "cvs" -a $RCSSYS != "svn" ] ; then
    echo "$RCSSYS is not a valid value for RCSSYS, check config file $ENVFILE"
    exit 1
fi

# print a usage message to stderr
pr_usage() {
    echo "usage: $0 [-V] command [revision] group device" >&2;
    echo "command = history | date | cat | log"
}

case "$1" in
    history)
        GROUP=$2
        DEVICE=$3
        ;;
    date)
        REV=$2
        GROUP=$3
        DEVICE=$4
        ;;
    cat)
        REV=$2
        GROUP=$3
        DEVICE=$4
        ;;
    log)
        GROUP=$2
        DEVICE=$3
        ;;
    *)
        pr_usage
        exit 1
esac



if [ $RCSSYS = cvs ]; then
    # TODO
    echo ""
else
    case $1 in
        history)
            CMD="svnlook history $CVSROOT $GROUP/configs/$DEVICE --show-ids"
            ;;
        date)
            CMD="svnlook date -r $REV $CVSROOT $GROUP/configs/$DEVICE"
            ;;
        cat)
            CMD="svnlook cat -r $REV $CVSROOT $GROUP/configs/$DEVICE"
            ;;
        log)
            CMD="svn log --xml $CVSROOT/../$GROUP/configs/$DEVICE"
            ;;
    esac
    #echo "execute: $CMD"
    $CMD
fi
	


