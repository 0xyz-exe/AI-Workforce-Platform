"use client";

import { Header } from "@/components/layout/header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { MetricCard } from "@/components/dashboard/metric-card";
import { UsageChart } from "@/components/dashboard/usage-chart";
import { useDashboardMetrics } from "@/hooks/use-dashboard";

export default function DashboardPage() {
  const metricsQuery = useDashboardMetrics();
  const metrics = metricsQuery.data ?? {
    active_users: 12,
    active_agents: 4,
    ai_requests: 1284,
    cost_savings: 482.6,
    time_saved: 7712,
    document_usage: 328,
    subscription_revenue: 24900,
  };

  return (
    <>
      <Header title="Executive Dashboard" subtitle="Track company usage, agent adoption, and AI productivity across the tenant." />
      <div className="flex-1 space-y-6 p-6">
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard label="Active users" value={String(metrics.active_users)} hint="Users active in the last 30 days" />
          <MetricCard label="Active agents" value={String(metrics.active_agents)} hint="Subscribed and enabled agents" accent="bg-cyan-400" />
          <MetricCard label="AI requests" value={String(metrics.ai_requests)} hint="Total prompt executions" accent="bg-blue-400" />
          <MetricCard label="Subscription revenue" value={`$${(metrics.subscription_revenue / 100).toFixed(0)}`} hint="Billed revenue this cycle" accent="bg-emerald-400" />
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
          <Card>
            <CardHeader>
              <CardTitle className="font-display">Daily usage</CardTitle>
              <CardDescription>Last week of platform activity.</CardDescription>
            </CardHeader>
            <CardContent>
              <UsageChart values={[14, 22, 18, 28, 36, 31, 42]} />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="font-display">Product signals</CardTitle>
              <CardDescription>What the company is using right now.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-sm text-muted-foreground">
              <div className="rounded-2xl border border-border/60 p-4">AI cost savings: ${metrics.cost_savings.toFixed(2)}</div>
              <div className="rounded-2xl border border-border/60 p-4">Time saved: {metrics.time_saved.toFixed(0)} minutes</div>
              <div className="rounded-2xl border border-border/60 p-4">Document usage: {metrics.document_usage} indexed documents</div>
            </CardContent>
          </Card>
        </section>
      </div>
    </>
  );
}