const url = process.env.HEALTHCHECK_URL ?? "http://localhost:3000/health"

async function main() {
  try {
    const response = await fetch(url, {
      signal: AbortSignal.timeout(2000),
    })

    process.exit(response.status === 200 ? 0 : 1)
  } catch {
    process.exit(1)
  }
}

main()
