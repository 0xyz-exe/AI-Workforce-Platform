"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import type { FormEvent } from "react";

import { AuthCard } from "@/components/auth/auth-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { apiFetch } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function RegisterPage() {
  const router = useRouter();
  const setSession = useAuthStore((state) => state.setSession);
  const [form, setForm] = useState({ company_name: "", company_slug: "", owner_name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await apiFetch<{ access_token: string; refresh_token: string }>("/api/v1/auth/register-company", {
        method: "POST",
        body: JSON.stringify({
          company: { name: form.company_name, slug: form.company_slug },
          owner: { full_name: form.owner_name, email: form.email, password: form.password },
          plan_code: "starter",
        }),
      });
      setSession({ accessToken: result.access_token, refreshToken: result.refresh_token, companySlug: form.company_slug, userEmail: form.email });
      router.push("/dashboard");
    } catch (registerError) {
      setError(registerError instanceof Error ? registerError.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen w-full items-center justify-center px-4 py-10">
      <div className="w-full max-w-6xl">
        <AuthCard title="Create company" description="Register your organization and launch your first AI workforce in minutes.">
        <form className="space-y-4" onSubmit={onSubmit}>
          <Input placeholder="Company name" value={form.company_name} onChange={(event) => setForm({ ...form, company_name: event.target.value })} />
          <Input placeholder="Company slug" value={form.company_slug} onChange={(event) => setForm({ ...form, company_slug: event.target.value })} />
          <Input placeholder="Owner name" value={form.owner_name} onChange={(event) => setForm({ ...form, owner_name: event.target.value })} />
          <Input placeholder="Email" type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
          <Input placeholder="Password" type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} />
          {error ? <p className="text-sm text-red-400">{error}</p> : null}
          <Button className="w-full" type="submit" disabled={loading}>
            {loading ? "Creating..." : "Create account"}
          </Button>
        </form>
        </AuthCard>
      </div>
    </div>
  );
}