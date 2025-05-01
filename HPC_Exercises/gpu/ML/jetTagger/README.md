1. Starting from your home directory, create a new directory called salt_tutorial

mkdir salt_tutorial

2. Copy all files from /eagle/projects/c2thep2/salt_scripts into this new directory

cd salt_tutorial
cp /eagle/projects/c2thep2/salt_scripts/* .

3. Run the install script

source install.sh

NOTE: After installation, if your environment becomes corrupted you can restore it by sourcing the env_setup.sh script

4. Submit a training job using a single GPU with PBS scheduling manager

qsub qsub.pbs

5. Verify that your job is in the queue

qstat

