"use client";

import { Header } from "@/components/layout/header";
import { PlanCard } from "@/components/dashboard/plan-card";
import { usePlans } from "@/hooks/use-plans";

export default function BillingPage() {
  const plansQuery = usePlans();
  const plans = plansQuery.data ?? [
    { id: 1, code: "starter", name: "Starter", description: null, price_monthly_cents: 4900, max_users: 5, max_agents: 1, features: {}, is_active: true },
    { id: 2, code: "business", name: "Business", description: null, price_monthly_cents: 14900, max_users: 20, max_agents: 3, features: {}, is_active: true },
    { id: 3, code: "enterprise", name: "Enterprise", description: null, price_monthly_cents: 49900, max_users: 0, max_agents: 0, features: {}, is_active: true },
  ];

  return (
    <>
      <Header title="Billing" subtitle="Manage plans, invoices, and Stripe-backed subscriptions." />
      <div className="grid gap-4 p-6 md:grid-cols-2 xl:grid-cols-3">
        {plans.map((plan) => (
          <PlanCard
            key={plan.code}
            name={plan.name}
            price={`$${(plan.price_monthly_cents / 100).toFixed(0)} / month`}
            features={[
              `${plan.max_agents || "Unlimited"} agents`,
              `${plan.max_users || "Unlimited"} users`,
              "RAG + knowledge base",
            ]}
            recommended={plan.code === "business"}
          />
        ))}
      </div>
    </>
  );
}