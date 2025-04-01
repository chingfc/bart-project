#!/bin/bash

export PATH="/home/qiulab_DATA/chingfc/BART/code/function:$PATH" # add the path to the function folder

# Function to run a command in the background
run_background_process() {

    /usr/local/bin/python3.9 run_bart_ewmv.py "$1" &> simulation"$1".log &

}

# Run multiple processes in parallel

# run the first 10 files in parallel
# the simulation 10 failed, so we need to run it again

for i in {10..20}
do 
    run_background_process $i &
done
# Wait for all background processes to finish
wait

echo "All background processes are done"
