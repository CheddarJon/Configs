#!/usr/bin/sh


prmtrn() {
	sel=$(echo -e "yes\nno" | dmenu -p "Do you want to $1")
	echo $sel
}

opt="restart WM\nquit WM\nreboot\nshutdown"

sel=$(echo -e $opt | dmenu -p "What to do?")
chc=$(prmtrn $sel)

if [ $chc = "no" ]; then
	exit
fi

# TODO Add option to save wm state. Add option on startup to use this state.
case $sel in
	restart*)
		bspc wm --restart
		;;
	quit*)
		bspc wm --dump-state > ${BSPWM_STATE}
		bspc quit 0
		;;
	reboot)
		reboot
		;;
	shutdown)
		poweroff
		;;
esac
