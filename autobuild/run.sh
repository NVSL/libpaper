# Add webhook http://domain_or_ip:9000
# `ssh git@github.com` should return a user/repo with read permission
gunicorn --bind 0.0.0.0:9000 wsgi:app --log-file=web.log -D
