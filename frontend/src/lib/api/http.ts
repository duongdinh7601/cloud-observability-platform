export function getApiBaseUrl(): string {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL
  if (!base) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set")
  }
  return base.replace(/\/$/, "")
}
