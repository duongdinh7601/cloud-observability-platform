# Build stage
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build


# Runtime stage
FROM node:20-slim AS runtime
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=build /app/next.config.mjs ./
COPY scripts ./scripts
EXPOSE 3000
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 CMD ["node", "scripts/container_healthcheck.js"]
CMD ["npm", "run", "start"]
