#!/bin/bash

echo "Launching polybar"

LOGDIR="$HOME/.log/my-i3-desktop"
mkdir -p "$LOGDIR"
INIT_LOG="$LOGDIR/polybar-launch.log"
exec 1>&- 2>&-
exec 1>"$INIT_LOG" 2>&1



detect_primary_monitor() {
	primary="$(xrandr | grep -F " connected primary" | head -n1 | cut -d ' ' -f1)"
	[[ -n $primary ]] || primary="$(echo "$monitors" | grep " connected" | head -n1 | cut -d ' ' -f1)"
	echo "$primary"
}

echo -e "Determining primary monitor..."
primary=$(detect_primary_monitor)
[[ -n $primary ]] || { echo "WARNING: no primary monitor detected!"; notify-send -a "Polybar launcher" "No primary monitor detected" "Couldn't detect primary monitor. Check $INIT_LOG."; }
echo "Primary monitor: $primary"

echo -e "\nDetermining secondary monitors..."
secondary="$(xrandr --listmonitors | sed -n "1d;/$primary\$/d;"'s/^.* \([^ ][^ ]*\)$/\1/p')"
if [[ -n $secondary ]]; then
	echo "Secondary monitors:"; echo "$secondary" | sed -r 's/^/* /'
else
	echo "No secondary monitors."
fi



# Terminate already running bar instances
echo -e "\nTerminating already running bars..."
echo "Running Polybar processes:"
pgrep -u $UID -x polybar | sed -r 's/^/* /'

killall -q polybar

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done
echo "Terminated."

(
	echo -e "\nReading secrets..."
	set -o allexport # Make all assignments exports
	source "$(dirname "$0")"/secrets.sh
	set +o allexport

	echo

	start_polybar() {
		echo "Starting $1 on $2"
		MONITOR="$2" \
			polybar --config="$HOME/.config/polybar/config.ini" "$1" \
			&>"$LOGDIR/polybar-$1-$2.log" & disown
	}

	start_polybar midbard "$primary"

	if [[ -n $secondary ]]; then
		while read -r monitor; do
			start_polybar secondary "$monitor"
		done <<< "$secondary"
	fi
)

exec 1>&- 2>&-

echo "Polybar launched."
