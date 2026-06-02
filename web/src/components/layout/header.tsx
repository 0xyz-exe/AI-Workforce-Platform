"use client";

import { Search, Sparkles } from "lucide-react";

import { NotificationBell } from "@/components/layout/notification-bell";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { UserMenu } from "@/components/ui/user-menu";

export function Header({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <header className="flex flex-col gap-4 border-b border-border/60 bg-black/10 px-6 py-5 backdrop-blur-xl lg:flex-row lg:items-center lg:justify-between">
      <div>
        <div className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
          <Sparkles className="h-3.5 w-3.5" /> SaaS control center
        </div>
        <h1 className="mt-3 font-display text-2xl font-semibold tracking-tight lg:text-3xl">{title}</h1>
        {subtitle ? <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p> : null}
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <div className="hidden items-center gap-2 rounded-full border border-border/70 bg-background/60 px-4 py-2 text-sm text-muted-foreground lg:flex">
          <Search className="h-4 w-4" /> Global search
        </div>
        <NotificationBell />
        <ThemeToggle />
        <UserMenu />
      </div>
    </header>
  );
}