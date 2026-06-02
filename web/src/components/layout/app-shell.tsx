import { Sidebar } from "@/components/layout/sidebar";
import type { ReactNode } from "react";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen lg:flex">
      <Sidebar />
      <main className="flex min-h-screen flex-1 flex-col">{children}</main>
    </div>
  );
}