"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

type LogFiltersValue = {
  level: string
  service_name: string
}

type LogFiltersProps = {
  value: LogFiltersValue
  onChange: (next: LogFiltersValue) => void
}

export function LogFilters({ value, onChange }: LogFiltersProps) {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      <div className="space-y-2">
        <Label htmlFor="service">Service</Label>
        <Input
          id="service"
          placeholder="e.g. billing-service"
          value={value.service_name}
          onChange={(e) => onChange({ ...value, service_name: e.target.value })}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="level">Level</Label>
        <Input
          id="level"
          placeholder="debug | info | warn | error"
          value={value.level}
          onChange={(e) => onChange({ ...value, level: e.target.value })}
        />
      </div>
    </div>
  )
}
