"use client";

import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/lib/api";

export type Plan = {
  id: number;
  code: string;
  name: string;
  description: string | null;
  price_monthly_cents: number;
  max_users: number;
  max_agents: number;
  features: Record<string, unknown>;
  is_active: boolean;
};

export function usePlans() {
  return useQuery({
    queryKey: ["plans"],
    queryFn: () => apiFetch<Plan[]>("/api/v1/billing/plans"),
  });
}