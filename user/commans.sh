server {
    listen 80;
    server_name 3.7.253.222;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root/home/ubuntu/project/shoplifter;
;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}


[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/ubuntu/project/shoplifter
ExecStart=/home/ubuntu/project/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          main_project.wsgi:application