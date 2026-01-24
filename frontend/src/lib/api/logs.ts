export type LogLevel = "debug" | "info" | "warn" | "error"

export type LogItem = {
  id: number
  timestamp: string
  level: LogLevel
  service_name: string
  message: string
}

export type Cursor = {
  cursor_ts: string
  cursor_id: number
}

export type LogListResponse = {
  items: LogItem[]
  next_cursor: Cursor | null
}

import { getApiBaseUrl } from "./http"

export type FetchLogsParams = {
  limit?: number
  cursor?: {
    cursor_ts: string
    cursor_id: number
  }
  level?: string
  service_name?: string
  start_time?: string
  end_time?: string
}

export async function fetchLogs(params: FetchLogsParams = {}): Promise<LogListResponse> {
  const url = new URL("/logs", getApiBaseUrl())

  if (params.limit !== undefined) url.searchParams.set("limit", String(params.limit))
  if (params.level) url.searchParams.set("level", params.level)
  if (params.service_name) url.searchParams.set("service_name", params.service_name)
  if (params.start_time) url.searchParams.set("start_time", params.start_time)
  if (params.end_time) url.searchParams.set("end_time", params.end_time)

  if (params.cursor) {
    url.searchParams.set("cursor_ts", params.cursor.cursor_ts)
    url.searchParams.set("cursor_id", String(params.cursor.cursor_id))
  }

  const res = await fetch(url.toString(), { cache: "no-store" })
  if (!res.ok) {
    const text = await res.text().catch(() => "")
    throw new Error(`fetchLogs failed (${res.status}): ${text}`)
  }

  return (await res.json()) as LogListResponse
}
