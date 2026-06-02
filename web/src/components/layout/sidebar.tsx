"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bot, BriefcaseBusiness, Building2, ChartColumnBig, FolderInput, LayoutDashboard, MessagesSquare, Settings2, ShieldCheck } from "lucide-react";

import { cn } from "@/lib/utils";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/agents", label: "Agents", icon: Bot },
  { href: "/chat", label: "Chat", icon: MessagesSquare },
  { href: "/knowledge-base", label: "Knowledge Base", icon: FolderInput },
  { href: "/billing", label: "Billing", icon: BriefcaseBusiness },
  { href: "/analytics", label: "Analytics", icon: ChartColumnBig },
  { href: "/settings", label: "Settings", icon: Settings2 },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden min-h-screen w-72 flex-col border-r border-border/60 bg-black/20 px-5 py-6 backdrop-blur-xl lg:flex">
      <div className="mb-8 flex items-center gap-3">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/15 text-primary shadow-glow">
          <Building2 className="h-6 w-6" />
        </div>
        <div>
          <p className="font-display text-lg font-semibold">AI Workforce</p>
          <p className="text-xs text-muted-foreground">Multi-tenant SaaS</p>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-2">
        {navItems.map((item) => {
          const active = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-2xl px-4 py-3 text-sm transition-all duration-200 hover:bg-white/5",
                active ? "bg-primary/15 text-primary ring-1 ring-primary/20" : "text-slate-300",
              )}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="mt-6 rounded-3xl border border-border/60 bg-gradient-to-br from-primary/10 via-cyan-400/5 to-blue-500/10 p-4">
        <div className="flex items-center gap-2 text-sm font-medium text-primary">
          <ShieldCheck className="h-4 w-4" /> Enterprise Ready
        </div>
        <p className="mt-2 text-sm text-muted-foreground">
          Tenant isolation, RBAC, RAG, billing, and audit-ready foundations are wired into the stack.
        </p>
      </div>
    </aside>
  );
}