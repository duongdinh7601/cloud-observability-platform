import { LogRowSkeleton } from "@/components/log-row-skeleton"

export function LogListSkeleton({ rows = 8 }: { rows?: number }) {
  return (
    <div className="space-y-2">
      {Array.from({ length: rows }).map((_, i) => (
        <LogRowSkeleton key={i} />
      ))}
    </div>
  )
}
