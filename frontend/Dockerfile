FROM imbios/bun-node:18-slim AS deps

RUN apt-get -y update && \
    apt-get install -yq openssl git ca-certificates tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
WORKDIR /app

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

FROM deps AS builder
WORKDIR /app
COPY . .

RUN bun run build


FROM node:18-slim AS runner
WORKDIR /app

COPY --from=builder  /app/.next/standalone ./

EXPOSE 3000

CMD ["node", "server.js"]