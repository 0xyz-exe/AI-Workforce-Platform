"use client";

import { BellRing } from "lucide-react";

import { Button } from "@/components/ui/button";

export function NotificationBell() {
  return (
    <Button variant="outline" size="sm" className="relative">
      <BellRing className="h-4 w-4" />
      <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-emerald-400" />
    </Button>
  );
}