"use client"

import { useQuery } from "@tanstack/react-query"
import { fetchLogs } from "@/lib/api/logs"

export default function LogsPage() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["logs", { limit: 10 }],
    queryFn: () => fetchLogs({ limit: 10 }),
  })

  if (isLoading) return <div>Loading…</div>
  if (isError) return <div>Error: {(error as Error).message}</div>

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Logs</h1>
      <div className="text-sm text-muted-foreground">
        Loaded {data.items.length} logs
      </div>
    </div>
  )
}
