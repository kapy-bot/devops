# --- Stage 1: build the static bundle ---------------------------------------
# node:20-alpine is only needed to run the Vite build; none of it (node,
# npm, node_modules) belongs in the final image that actually serves traffic.
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

# --- Stage 2: serve with nginx ------------------------------------------------
# nginx-unprivileged instead of the plain nginx image: the official nginx
# image runs as root and binds port 80, which needs extra work to run
# rootless. This variant already runs as a non-root user on port 8080.
FROM nginxinc/nginx-unprivileged:1.27-alpine

# The base image's OS packages (openssl, zlib, libxml2, etc.) are only as
# current as whatever snapshot was last published upstream. Upgrading here
# pulls in security patches Alpine has released since then, independent of
# how stale that snapshot is.
RUN apk update && apk upgrade --no-cache

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
