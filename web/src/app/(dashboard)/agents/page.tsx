"use client";

import { Header } from "@/components/layout/header";
import { AgentCard } from "@/components/dashboard/agent-card";
import { useMarketplaceAgents } from "@/hooks/use-agents";

export default function AgentsPage() {
  const agentsQuery = useMarketplaceAgents();
  const agents = agentsQuery.data ?? [
    { id: 1, code: "sales-agent", name: "Sales Agent", category: "sales", description: "Qualifies leads and writes follow-up emails.", prompt_template: "", system_prompt: "", default_model: "gpt-4o-mini", is_marketplace: true, is_active: true, metadata_json: {} },
    { id: 2, code: "hr-agent", name: "HR Agent", category: "hr", description: "Screens resumes and generates interview packs.", prompt_template: "", system_prompt: "", default_model: "gpt-4o-mini", is_marketplace: true, is_active: true, metadata_json: {} },
    { id: 3, code: "finance-agent", name: "Finance Agent", category: "finance", description: "Summarizes spend and invoices.", prompt_template: "", system_prompt: "", default_model: "gpt-4o-mini", is_marketplace: true, is_active: true, metadata_json: {} },
  ];

  return (
    <>
      <Header title="Agents Marketplace" subtitle="Browse, subscribe, and enable specialized AI employees for each business function." />
      <div className="grid gap-4 p-6 md:grid-cols-2 xl:grid-cols-3">
        {agents.map((agent) => (
          <AgentCard key={agent.id} name={agent.name} description={agent.description} category={agent.category} enabled={agent.is_active} />
        ))}
      </div>
    </>
  );
}