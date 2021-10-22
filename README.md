# UKLI_Collimator_SK_Steering

source set_env.sh --> Sets up the required envirnoment variables

To make the SK steering plots just run "run.sh". It is rather self-explanatory.
The plots for the steering meeting will be stored in plots/steering/.
This has to be run after Jordan has processed the data of the week.
Previous data must be copied to your personal folder. For that just copy the /home/pablofer/calib/analysis/sk_ukli/daily_col_plots folder to this code's location.

./process_bacteria.sh --> Reads the bacteria counters data and stores them into root files in the data/ folder. It also stores plots of the data in the plots/ folder.

There are both sets of code for making the analogous plots for the two collimator analyses (position and angular). Check run.sh.

