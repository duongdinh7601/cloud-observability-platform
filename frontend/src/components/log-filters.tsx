"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

type LogFiltersValue = {
  level: string
  service_name: string
}

type LogFiltersProps = {
  value: LogFiltersValue
  onChange: (next: LogFiltersValue) => void
}

export function LogFilters({ value, onChange }: LogFiltersProps) {
    const selectValue = value.level === "" ? "all" : value.level

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

                <Select
                    value={selectValue}
                    onValueChange={(v) => onChange({ ...value, level: v === "all" ? "" : v })}
                >
                    <SelectTrigger id="level">
                        <SelectValue placeholder="All levels" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="all">All</SelectItem>
                        <SelectItem value="debug">Debug</SelectItem>
                        <SelectItem value="info">Info</SelectItem>
                        <SelectItem value="warn">Warn</SelectItem>
                        <SelectItem value="error">Error</SelectItem>
                    </SelectContent>
                </Select>
            </div>
        </div>
    )
}
