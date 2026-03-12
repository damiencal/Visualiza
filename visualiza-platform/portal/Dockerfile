FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ─── Runtime ──────────────────────────────────────────────────────────────────
FROM node:20-alpine

WORKDIR /app
COPY --from=builder /app/.output ./

ENV PORT=3002
ENV HOST=0.0.0.0
EXPOSE 3002

CMD ["node", "server/index.mjs"]
