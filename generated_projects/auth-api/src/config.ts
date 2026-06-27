export const config = { apiTimeoutMs: Number(process.env.API_TIMEOUT_MS ?? 5000), jwtAudience: process.env.JWT_AUDIENCE ?? 'local' };
