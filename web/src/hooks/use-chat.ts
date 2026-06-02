"use client";

import { useMutation, useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export type ChatSession = {
  id: number;
  company_id: number;
  agent_id: number;
  user_id: number | null;
  knowledge_base_id: number | null;
  title: string;
  memory_json: Record<string, unknown>;
  is_archived: boolean;
};

export function useChatSessions() {
  const { accessToken } = useAuthStore();
  return useQuery({
    queryKey: ["chat-sessions", accessToken],
    queryFn: () => apiFetch<ChatSession[]>("/api/v1/chat/sessions"),
    enabled: Boolean(accessToken),
  });
}

export function useCreateChatSession() {
  return useMutation({
    mutationFn: (payload: { agent_id: number; knowledge_base_id?: number | null; title: string }) =>
      apiFetch<ChatSession>("/api/v1/chat/sessions", { method: "POST", body: JSON.stringify(payload) }),
  });
}