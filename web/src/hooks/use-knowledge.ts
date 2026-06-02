"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { apiFetch } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export type KnowledgeBase = {
  id: number;
  company_id: number;
  name: string;
  description: string | null;
  is_default: boolean;
  indexing_status: string;
};

export function useKnowledgeBases() {
  const { accessToken } = useAuthStore();
  return useQuery({
    queryKey: ["knowledge-bases", accessToken],
    queryFn: () => apiFetch<KnowledgeBase[]>("/api/v1/knowledge/bases"),
    enabled: Boolean(accessToken),
  });
}

export function useCreateKnowledgeBase() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: { name: string; description?: string; is_default?: boolean }) =>
      apiFetch<KnowledgeBase>("/api/v1/knowledge/bases", { method: "POST", body: JSON.stringify(payload) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["knowledge-bases"] }),
  });
}