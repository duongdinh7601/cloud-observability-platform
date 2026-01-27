import { Suspense } from "react"
import LogsClient from "./logs-client"

export default function LogsPage() {
  return (
    <Suspense fallback={<div className="p-4 text-sm text-muted-foreground">Loading…</div>}>
      <LogsClient />
    </Suspense>
  )
}
