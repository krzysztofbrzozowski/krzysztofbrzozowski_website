location /static/ {
    alias /usr/src/app/static/;
}

location /media/ {
    alias /usr/src/app/media/;
}

client_max_body_size 100M;