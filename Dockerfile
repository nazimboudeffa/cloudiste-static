FROM nginx:alpine

COPY *.html /usr/share/nginx/html/
COPY favicon.svg og-image.png robots.txt sitemap.xml /usr/share/nginx/html/
