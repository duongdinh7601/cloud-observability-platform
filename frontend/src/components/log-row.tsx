import { Badge } from "@/components/ui/badge"
import { LogItem } from "@/lib/api/logs"

type LogRowProps = 
{
  log: LogItem
}

export function LogRow({ log }: LogRowProps) 
{
  return (
    <div className="flex gap-4 rounded-md border p-3 text-sm">
      <div className="w-40 shrink-0 font-mono text-muted-foreground">
        {new Date(log.timestamp).toLocaleString()}
      </div>

      <div className="w-20">
        <Badge variant="outline">
            {log.level}
        </Badge>
      </div>

      <div className="w-40 truncate text-muted-foreground">
        {log.service_name}
      </div>

      <div className="flex-1 break-words">
        {log.message}
      </div>
    </div>
  )
}
