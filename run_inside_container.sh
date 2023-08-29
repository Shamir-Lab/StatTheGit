#!/bin/bash
cd /specific/netapp5/gaga/tools/StatTheGit4TAU && python3 fetch_stats.py && python3 sync_mongo.py --db_url localhost && python3 display_stats.py && cp repo_stats/Shamir-Lab/plots/git_stat_Shamir-Lab_*  /specific/netapp5/gaga/html/Private/

