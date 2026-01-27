"use client"

import { useInfiniteQuery } from "@tanstack/react-query"
import type { Cursor, LogListResponse } from "@/lib/api/logs"
import { fetchLogs } from "@/lib/api/logs"
import { LogList } from "@/components/log-list"
import { Button } from "@/components/ui/button"
import { LogListSkeleton } from "@/components/log-list-skeleton"
import { useState, useEffect } from "react"
import { LogFilters } from "@/components/log-filters"
import { useDebouncedValue } from "@/lib/use-debounced-value"
import { useSearchParams, useRouter } from "next/navigation"

export default function LogsClient() {
  const limit = 10

  const router = useRouter()
  const searchParams = useSearchParams()

  const [filters, setFilters] = useState(() => {
    const level = searchParams.get("level") ?? ""
    const service_name = searchParams.get("service") ?? ""
    return { level, service_name }
  })

  const debouncedService = useDebouncedValue(
    filters.service_name,
    filters.service_name === "" ? 0 : 600
  )

  const hasActiveFilters = filters.level !== "" || filters.service_name !== ""

  const clearFilters = () => {
    setFilters({
      level: "",
      service_name: "",
    })
  }

  // URL -> state (back/forward sync)
  useEffect(() => {
    const level = searchParams.get("level") ?? ""
    const service_name = searchParams.get("service") ?? ""

    setFilters((prev) => {
      if (prev.level === level && prev.service_name === service_name) {
        return prev
      }
      return { level, service_name }
    })
  }, [searchParams])

  // state -> URL (replace to avoid history spam)
  useEffect(() => {
    const params = new URLSearchParams()

    if (filters.level) params.set("level", filters.level)
    if (debouncedService) params.set("service", debouncedService)

    const qs = params.toString()
    router.replace(qs ? `/logs?${qs}` : "/logs")
  }, [filters.level, debouncedService, router])

  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isFetching,
  } = useInfiniteQuery({
    queryKey: ["logs", { limit, level: filters.level, service_name: debouncedService }],
    queryFn: ({ pageParam }) =>
      fetchLogs({
        limit,
        cursor: pageParam as Cursor | undefined,
        level: filters.level || undefined,
        service_name: debouncedService || undefined,
      }),
    initialPageParam: undefined as Cursor | undefined,
    getNextPageParam: (lastPage: LogListResponse) =>
      lastPage.next_cursor ?? undefined,
  })

  // Computing a flat list of items
  const items = data?.pages.flatMap((p) => p.items) ?? []
  const hasItems = items.length > 0

  // Error
  if (isError) {
    return (
      <div className="space-y-4">
        <h1 className="text-2xl font-semibold">Logs</h1>

        <div className="text-sm text-destructive">
          Failed to load logs: {error.message}
        </div>

        <Button onClick={() => refetch()}>Retry</Button>
      </div>
    )
  }

  // Display logs
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Logs</h1>

      <LogFilters value={filters} onChange={setFilters} />

      <div className="flex items-center gap-3">
        {hasActiveFilters && (
          <Button variant="outline" onClick={clearFilters}>
            Clear filters
          </Button>
        )}

        {isFetching && (
          <div className="text-sm text-muted-foreground">Filtering…</div>
        )}
      </div>

      {!hasItems && isLoading ? (
        <LogListSkeleton rows={8} />
      ) : hasItems ? (
        <LogList items={items} />
      ) : (
        <div className="text-sm text-muted-foreground">
          No logs match the current filters.
        </div>
      )}

      <div>
        <Button
          onClick={() => fetchNextPage()}
          disabled={!hasNextPage || isFetchingNextPage}
        >
          {isFetchingNextPage
            ? "Loading..."
            : hasNextPage
              ? "Load more"
              : "No more logs"}
        </Button>
      </div>
    </div>
  )
}
