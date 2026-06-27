export function errorMiddleware(error, _req, res, _next) { res.status(500).json({ error: String(error) }); }
