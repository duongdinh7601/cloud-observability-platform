import { fetchLogs } from "@/lib/api/logs"

export default async function LogsPage() {
  const data = await fetchLogs({ limit: 10 })

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Logs</h1>
      <div className="text-sm text-muted-foreground">
        Loaded {data.items.length} logs
      </div>
    </div>
  )
}
