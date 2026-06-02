"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

type AuthState = {
  accessToken: string | null;
  refreshToken: string | null;
  companySlug: string | null;
  userEmail: string | null;
  setSession: (session: { accessToken: string; refreshToken: string; companySlug?: string; userEmail?: string }) => void;
  clearSession: () => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      companySlug: null,
      userEmail: null,
      setSession: (session) =>
        set({
          accessToken: session.accessToken,
          refreshToken: session.refreshToken,
          companySlug: session.companySlug ?? null,
          userEmail: session.userEmail ?? null,
        }),
      clearSession: () => set({ accessToken: null, refreshToken: null, companySlug: null, userEmail: null }),
    }),
    { name: "ai-workforce-auth" },
  ),
);