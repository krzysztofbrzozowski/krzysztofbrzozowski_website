location /static/ {
    alias /usr/src/app/static/;
}

location /media/ {
    alias /usr/src/app/media/;
}