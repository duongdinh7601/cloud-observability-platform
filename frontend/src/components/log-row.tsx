"use client"

import { Badge } from "@/components/ui/badge"
import { LogItem } from "@/lib/api/logs"
import { useState } from "react"
import { Button } from "@/components/ui/button"


type LogRowProps = 
{
  log: LogItem
}

function levelClass(level: string)
{
  switch (level.toLowerCase())
  {
    case "error":
      return "border-red-500/30 text-red-600"
    case "warn":
    case "warning":
      return "border-yellow-500/30 text-yellow-700"
    case "info":
      return "border-blue-500/30 text-blue-600"
    case "debug":
      return "border-muted-foreground/30 text-muted-foreground"
    default:
      return ""
  }
}

function timeAgo(iso: string) 
{
  const ms = Date.now() - new Date(iso).getTime()
  const s = Math.floor(ms / 1000)
  if (s < 60) return `${s}s ago`
  const m = Math.floor(s / 60)
  if (m < 60) return `${m}m ago`
  const h = Math.floor(m / 60)
  if (h < 24) return `${h}h ago`
  const d = Math.floor(h / 24)
  return `${d}d ago`
}

export function LogRow({ log }: LogRowProps) 
{
  const [copied, setCopied] = useState(false)

  async function onCopy() {
    await navigator.clipboard.writeText(log.message)
    setCopied(true)
    window.setTimeout(() => setCopied(false), 800)
  }

  return (
    <div className="flex gap-4 rounded-md border p-3 text-sm">
      <div className="w-40 shrink-0 font-mono text-muted-foreground"
        title={new Date(log.timestamp).toLocaleString()}>
          {timeAgo(log.timestamp)}
      </div>

      <div className="w-20">
        <Badge variant="outline" className={levelClass(log.level)}>
            {log.level}
        </Badge>
      </div>

      <div className="w-40 truncate text-muted-foreground">
        {log.service_name}
      </div>

      <div className="flex-1 break-words">
        {log.message}
      </div>

      <div className="shrink-0">
        <Button variant="ghost" size="sm" onClick={onCopy}>
          {copied ? "Copied" : "Copy"}
        </Button>
      </div>
    </div>
  )
}
