import Redis from "ioredis";

const redisUrl = "redis://localhost:6379";

const redis = new Redis(redisUrl, {
  tls: redisUrl.startsWith("rediss://") ? {} : undefined,
  maxRetriesPerRequest: null,
  enableOfflineQueue: false,
});

redis.on("connect", () => console.log("✅ Redis Connected"));
redis.on("error", (err) => console.error("❌ Redis Error:", err));

export default redis;
