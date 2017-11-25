#!/bin/bash -l
if [ $# -lt 4 ]; then
cat <<EOF
Usage:
 	$0 [executable] [Start NTASKS] [End NTASKS] [file to write results]
EOF

else

EXE="$1"
NTASKS_START="$2"
NTASKS_END="$3"
OUTFILE="$4"

#neq=(2 4 8 16 32 64 128 256 512 1024 2048)
neq=(32 64 128 256 512 1024 2048) 
if [ -e $OUTFILE ] ; then
	rm $OUTFILE
fi
counter=0
for (( i=${NTASKS_START}; i<=${NTASKS_END} ; i=$(expr $i \* 2) ))
	do 
		NEQ=${neq[${counter}]}
		NUM_TASKS=${i}
		echo "aprun -n ${NUM_TASKS} -j 1 ${EXE} -n ${NEQ} -f ./input_matrices/${NEQ}by${NEQ}.mat"	
		if [ ${NUM_TASKS} -eq ${NTASKS_START} ]; then
			scalar=$(aprun -n ${NUM_TASKS} -j 1 ${EXE} -n ${NEQ} -f ./input_matrices/${NEQ}by${NEQ}.mat |grep  "Average compute time" | cut -d "=" -f 2 | cut -d " " -f 2)
			compute_time=${scalar}
		else 
			compute_time=$(aprun -n ${NUM_TASKS} -j 1 ${EXE} -n ${NEQ} -f ./input_matrices/${NEQ}by${NEQ}.mat |grep  "Average compute time" | cut -d "=" -f 2 | cut -d " " -f 2)
		fi

		echo -e "${NUM_TASKS}   ${compute_time}   $(echo $(expr ${scalar}/${compute_time})|bc -l)">>${OUTFILE}.out
counter=$(expr $counter + 1)
done

echo "Now using GNUPLOT to plot scaling"
gnuplot << EOF
	set term png
	set output "${OUTFILE}.png"
	plot "${OUTFILE}.out" using 1:3 with lines 
EOF
fi
