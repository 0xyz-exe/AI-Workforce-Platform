"use client";

import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export function useDashboardMetrics() {
  const { accessToken } = useAuthStore();
  return useQuery({
    queryKey: ["dashboard-metrics", accessToken],
    queryFn: () => apiFetch<{ active_users: number; active_agents: number; ai_requests: number; cost_savings: number; time_saved: number; document_usage: number; subscription_revenue: number }>("/api/v1/analytics/dashboard"),
    enabled: Boolean(accessToken),
  });
}