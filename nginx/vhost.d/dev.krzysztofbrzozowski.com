location /media/ {
    alias /usr/src/app/media/;
}