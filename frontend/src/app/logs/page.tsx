"use client"

import { useQuery } from "@tanstack/react-query"
import { fetchLogs } from "@/lib/api/logs"
import { LogList } from "@/components/log-list"
import { Button } from "@/components/ui/button"

export default function LogsPage() {
  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ["logs", { limit: 10 }],
    queryFn: () => fetchLogs({ limit: 10 }),
  })

  // Loading page
  if (isLoading) 
  {
    return (
      <div className="space-y-4">
        <h1 className="text-2x1 font-semibold">Logs</h1>
        <div className="text-sm text-muted-foreground">Loading logs...</div>
      </div>
    )
  }

  // Error
  if (isError) 
  {
    return (
      <div className="space-y-4">
        <h1 className="text-2x1 font-semibold">Logs</h1>
        
        <div className="text-sm text-destructive">
          Failed to load logs: {(error as Error).message}
        </div>

        <Button onClick={() => refetch()}>Retry</Button>
      </div>
    )
  }

  // Empty logs
  if (!data || data.items.length === 0) {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Logs</h1>
      <div className="text-sm text-muted-foreground">No logs found.</div>
    </div>
  )
}

// Display logs
return (
  <div className="space-y-4">
    <h1 className="text-2xl font-semibold">Logs</h1>
    <LogList items={data.items} />
  </div>
)

}
