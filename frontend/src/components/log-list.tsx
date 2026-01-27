import { LogItem } from "@/lib/api/logs"
import { LogRow } from "@/components/log-row"

type LogListProps = 
{
  items: LogItem[]
}

export function LogList({ items }: LogListProps) 
{
  return (
    <div className="space-y-2">
      {items.map((log) => (
        <LogRow key={log.id} log={log} />
      ))}
    </div>
  )
}
