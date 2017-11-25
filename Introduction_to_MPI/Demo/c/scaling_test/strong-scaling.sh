#!/bin/bash -l
if [ $# -lt 4 ]; then
cat <<EOF
Usage:
 	$0 [executable] [max MPI-Tasks] [number of equations] [file to write results]
EOF

else
EXE="$1"
MAX_TASKS="$2"
NEQ="$3"
OUTFILE="$4"

if [ ! -z ${OMP_SCHEDULE} ]; then
	export OMP_SCHEDULE=${SCHEDULE}
fi

if [ -e $OUTFILE ] ; then
	rm $OUTFILE
fi
for (( i=2; i<=$MAX_TASKS ; i=$(expr $i \* 2) ))
	do 
		echo "aprun -n ${i} -j 1 ${EXE} -n ${NEQ} -f ./input_matrices/${NEQ}by${NEQ}.mat"
		echo $i	
		echo -e "${i} $(aprun -n ${i} -j 1 ${EXE} -n ${NEQ} -f ./input_matrices/${NEQ}by${NEQ}.mat |grep  "Average compute time" | cut -d "=" -f 2 | cut -d " " -f 2)">>${OUTFILE}.out
done


echo "Now using GNUPLOT to plot scaling"
gnuplot << EOF
	set term png
	set output "${OUTFILE}.png"
	plot "${OUTFILE}.out" using 1:2 with lines 
EOF

fi
