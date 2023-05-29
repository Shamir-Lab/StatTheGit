#!/bin/bash
# export LD_LIBRARY_PATH=/usr/local/lib/openssl-1.1.1a/lib
# cd /specific/netapp5/gaga/tools/StatTheGit4TAU/ && pwd
# python-venv/bin/python fetch_stats.py
# python-venv/bin/python sync_mongo.py
# python-venv/bin/python display_stats.py
# cp repo_stats/Shamir-Lab/plots/git_stat_Shamir-Lab_*  /specific/netapp5/gaga/html/Private/

#!/bin/bash
export UDOCKER_DIR=/specific/elkon/hagailevi/PRS/docker
udocker=/usr/local/bin/udocker
$udocker run --containerauth --publish=27017:27017 --volume /specific:/mnt/specific --volume /run/shm:/dev/shm statistics_git bash -c 'cd /specific/netapp5/gaga/tools/StatTheGit4TAU && python3 fetch_stats.py && python3 sync_mongo.py --db_url localhost && python3 display_stats.py && cp repo_stats/Shamir-Lab/plots/git_stat_Shamir-Lab_*  /specific/netapp5/gaga/html/Private/'

