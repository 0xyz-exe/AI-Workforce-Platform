"use client";

import { Header } from "@/components/layout/header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { MetricCard } from "@/components/dashboard/metric-card";
import { UsageChart } from "@/components/dashboard/usage-chart";
import { useDashboardMetrics } from "@/hooks/use-dashboard";

export default function AnalyticsPage() {
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
      <Header title="Analytics" subtitle="Executive metrics and usage patterns across users, agents, and documents." />
      <div className="space-y-6 p-6">
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard label="Cost savings" value={`$${metrics.cost_savings.toFixed(0)}`} hint="Estimated monthly automation savings" />
          <MetricCard label="Time saved" value={`${metrics.time_saved.toFixed(0)}m`} hint="Human minutes saved by agents" accent="bg-cyan-400" />
          <MetricCard label="Documents indexed" value={String(metrics.document_usage)} hint="Knowledge base files processed" accent="bg-blue-400" />
          <MetricCard label="AI requests" value={String(metrics.ai_requests)} hint="Prompt executions in total" accent="bg-emerald-400" />
        </section>

        <Card>
          <CardHeader>
            <CardTitle className="font-display">Monthly usage trend</CardTitle>
            <CardDescription>Visualize adoption over the last week with a simple executive chart.</CardDescription>
          </CardHeader>
          <CardContent>
            <UsageChart values={[8, 11, 18, 24, 28, 31, 40]} />
          </CardContent>
        </Card>
      </div>
    </>
  );
}