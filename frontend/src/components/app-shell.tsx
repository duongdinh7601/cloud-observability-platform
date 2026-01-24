import Link from "next/link"
import { ReactNode } from "react"

type AppShellProps = {
  children: ReactNode
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen">
      <div className="mx-auto max-w-6xl px-6 py-6">
        <div className="grid grid-cols-12 gap-6">
          <aside className="col-span-3">
            <div className="rounded-lg border p-4">
              <div className="text-sm font-semibold">Cloud Observability</div>
              <nav className="mt-4 space-y-2 text-sm">
                <Link className="block hover:underline" href="/logs">
                  Logs
                </Link>
              </nav>
            </div>
          </aside>

          <main className="col-span-9">{children}</main>
        </div>
      </div>
    </div>
  )
}
