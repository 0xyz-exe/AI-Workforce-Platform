"use client";

import { Header } from "@/components/layout/header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function SettingsPage() {
  return (
    <>
      <Header title="Settings" subtitle="Company profile, security, and workspace preferences." />
      <div className="grid gap-6 p-6 xl:grid-cols-[1fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle className="font-display">Company profile</CardTitle>
            <CardDescription>Update the tenant identity and metadata.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Input placeholder="Company name" />
            <Input placeholder="Industry" />
            <Input placeholder="Tenant slug" />
            <Button>Save changes</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="font-display">Security</CardTitle>
            <CardDescription>Control access and session behavior.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            <div className="rounded-2xl border border-border/60 p-4">JWT auth enabled</div>
            <div className="rounded-2xl border border-border/60 p-4">RBAC roles: Owner, Admin, Manager, Staff</div>
            <div className="rounded-2xl border border-border/60 p-4">Tenant isolation enforced by company_id</div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}