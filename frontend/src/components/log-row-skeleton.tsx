export function LogRowSkeleton() {
  return (
    <div className="flex gap-4 rounded-md border p-3 text-sm">
      <div className="h-4 w-40 animate-pulse rounded bg-muted" />
      <div className="h-5 w-16 animate-pulse rounded bg-muted" />
      <div className="h-4 w-40 animate-pulse rounded bg-muted" />
      <div className="h-4 flex-1 animate-pulse rounded bg-muted" />
    </div>
  )
}
