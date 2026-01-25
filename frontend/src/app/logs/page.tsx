"use client"

import { useInfiniteQuery } from "@tanstack/react-query"
import { fetchLogs } from "@/lib/api/logs"
import { LogList } from "@/components/log-list"
import { Button } from "@/components/ui/button"
import { LogListSkeleton } from "@/components/log-list-skeleton"
import { Cursor, LogListResponse } from "@/lib/api/logs"
import { useState } from "react"
import { LogFilters } from "@/components/log-filters"
import { useDebouncedValue } from "@/lib/use-debounced-value"

export default function LogsPage() {
  const limit = 10

  const [filters, setFilters] = useState
  ({
    level: "",
    service_name: "",
  })

  const debouncedService = useDebouncedValue(filters.service_name, 600)
  
  const 
  { 
    data, 
    isLoading, 
    isError, 
    error, 
    refetch, 
    fetchNextPage, 
    hasNextPage, 
    isFetchingNextPage, 
  } = useInfiniteQuery<
    LogListResponse, 
    Error, 
    LogListResponse, 
    ["logs", { limit: number }], 
    Cursor | undefined
  >({
    queryKey: ["logs", { limit, level: filters.level, service_name: debouncedService }],
    queryFn: ({ pageParam }) => fetchLogs({ 
      limit, 
      cursor: pageParam, 
      level: filters.level || undefined,
      service_name: debouncedService || undefined,
    }),
    initialPageParam: undefined,
    getNextPageParam: (lastPage) => lastPage.next_cursor ?? undefined,
  })

  // Computing a flat list of items
  const items = data?.pages.flatMap((p) => p.items) ?? []

  // Loading page
  if (isLoading) 
  {
    return (
      <div className="space-y-4">
        <h1 className="text-2x1 font-semibold">Logs</h1>
        <LogListSkeleton rows={8} />
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
          Failed to load logs: {error.message}
        </div>

        <Button onClick={() => refetch()}>Retry</Button>
      </div>
    )
  }

  // Empty logs
  if (items.length === 0) {
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

    <LogFilters value={filters} onChange={setFilters} />
    <LogList items={items} />

    <div>
      <Button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? "Loading..." : hasNextPage ? "Load more" : "No more logs"}
      </Button>
    </div>

  </div>
)

}
