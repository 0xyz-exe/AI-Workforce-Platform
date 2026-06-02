"use client";

import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export type MarketplaceAgent = {
  id: number;
  code: string;
  name: string;
  category: string;
  description: string;
  prompt_template: string;
  system_prompt: string;
  default_model: string;
  is_marketplace: boolean;
  is_active: boolean;
  metadata_json: Record<string, unknown>;
};

export function useMarketplaceAgents() {
  const { accessToken } = useAuthStore();
  return useQuery({
    queryKey: ["marketplace-agents", accessToken],
    queryFn: () => apiFetch<MarketplaceAgent[]>("/api/v1/agents/marketplace"),
    enabled: Boolean(accessToken),
  });
}