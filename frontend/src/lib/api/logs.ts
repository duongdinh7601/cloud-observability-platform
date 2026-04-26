export type LogLevel = "debug" | "info" | "warn" | "error"

export type LogItem = 
{
  id: number
  timestamp: string
  level: LogLevel
  service_name: string
  message: string
}

export type Cursor = 
{
  cursor_ts: string
  cursor_id: number
}

export type LogListResponse = 
{
  items: LogItem[]
  next_cursor: Cursor | null
}

import { getApiBasePath } from "./http"

export type FetchLogsParams = 
{
  limit?: number
  cursor?:  Cursor
  level?: string
  service_name?: string
  start_time?: string
  end_time?: string
}

export async function fetchLogs(params: FetchLogsParams = {}): Promise<LogListResponse> 
{
  const query = new URLSearchParams()

  if (params.limit !== undefined) query.set("limit", String(params.limit))
  if (params.level) query.set("level", params.level)
  if (params.service_name) query.set("service_name", params.service_name)
  if (params.start_time) query.set("start_time", params.start_time)
  if (params.end_time) query.set("end_time", params.end_time)

  if (params.cursor) 
  {
    query.set("cursor_ts", params.cursor.cursor_ts)
    query.set("cursor_id", String(params.cursor.cursor_id))
  }

  const qs = query.toString()
  const path = qs
    ? `${getApiBasePath()}/logs?${qs}`
    : `${getApiBasePath()}/logs`

  const res = await fetch(path, { cache: "no-store" })
  if (!res.ok) 
  {
    const text = await res.text().catch(() => "")
    throw new Error(`fetchLogs failed (${res.status}): ${text}`)
  }

  return (await res.json()) as LogListResponse
}
