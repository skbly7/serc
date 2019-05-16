### Commands to update the publications on the site
1. ssh serc@serc.iiit.ac.in
2. cd ~/serc
3. source deploy/bin/activate
4. python website/manage.py shell < website/dblp_parse.py
