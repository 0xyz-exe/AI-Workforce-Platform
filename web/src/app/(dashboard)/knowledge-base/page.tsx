"use client";

import { useState } from "react";

import { Header } from "@/components/layout/header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useCreateKnowledgeBase, useKnowledgeBases } from "@/hooks/use-knowledge";

export default function KnowledgeBasePage() {
  const knowledgeBasesQuery = useKnowledgeBases();
  const createKnowledgeBase = useCreateKnowledgeBase();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  return (
    <>
      <Header title="Knowledge Base" subtitle="Upload files, build embeddings, and power retrieval with tenant-isolated vectors." />
      <div className="grid gap-6 p-6 xl:grid-cols-[0.9fr_1.1fr]">
        <Card>
          <CardHeader>
            <CardTitle className="font-display">Create knowledge base</CardTitle>
            <CardDescription>Organize files by team, product, or customer segment.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Input placeholder="Knowledge base name" value={name} onChange={(event) => setName(event.target.value)} />
            <Input placeholder="Description" value={description} onChange={(event) => setDescription(event.target.value)} />
            <Button
              onClick={() =>
                createKnowledgeBase.mutate({ name, description, is_default: false }, { onSuccess: () => { setName(""); setDescription(""); } })
              }
            >
              Create base
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="font-display">Uploaded bases</CardTitle>
            <CardDescription>Files are stored in S3 and indexed in Qdrant after processing.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {(knowledgeBasesQuery.data ?? []).map((base) => (
              <div key={base.id} className="rounded-2xl border border-border/60 p-4">
                <div className="font-medium">{base.name}</div>
                <div className="text-sm text-muted-foreground">{base.description ?? "No description"}</div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </>
  );
}