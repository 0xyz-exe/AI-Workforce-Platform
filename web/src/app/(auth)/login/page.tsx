"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import type { FormEvent } from "react";

import { AuthCard } from "@/components/auth/auth-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { apiFetch } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function LoginPage() {
  const router = useRouter();
  const setSession = useAuthStore((state) => state.setSession);
  const [form, setForm] = useState({ company_slug: "", email: "", password: "" });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await apiFetch<{ access_token: string; refresh_token: string; token_type: string }>("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify(form),
      });
      setSession({ accessToken: result.access_token, refreshToken: result.refresh_token, companySlug: form.company_slug, userEmail: form.email });
      router.push("/dashboard");
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen w-full items-center justify-center px-4 py-10">
      <div className="w-full max-w-6xl">
        <AuthCard title="Sign in" description="Access your company AI workspace and continue the conversation with your agents.">
        <form className="space-y-4" onSubmit={onSubmit}>
          <Input placeholder="Company slug" value={form.company_slug} onChange={(event) => setForm({ ...form, company_slug: event.target.value })} />
          <Input placeholder="Email" type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
          <Input placeholder="Password" type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} />
          {error ? <p className="text-sm text-red-400">{error}</p> : null}
          <Button className="w-full" type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </Button>
        </form>
        </AuthCard>
      </div>
    </div>
  );
}