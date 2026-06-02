"use client";

import { useState } from "react";
import type { ChangeEvent } from "react";

import { Header } from "@/components/layout/header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

type ChatMessage = { role: "assistant" | "user"; content: string };

const initialMessages: ChatMessage[] = [
  { role: "assistant", content: "Welcome to AI Workforce chat. Ask any question and the selected agent will respond with citations." },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [message, setMessage] = useState("");

  function sendMessage() {
    if (!message.trim()) return;
    setMessages((current: ChatMessage[]) => [...current, { role: "user", content: message }, { role: "assistant", content: "This is a frontend-ready chat shell connected to the streaming API." }]);
    setMessage("");
  }

  return (
    <>
      <Header title="AI Chat" subtitle="ChatGPT-like interface with session history, agent selection, and streaming-ready UX." />
      <div className="grid gap-6 p-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <CardHeader>
            <CardTitle className="font-display">Conversation</CardTitle>
            <CardDescription>Selected agent responses will stream from the backend.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3 rounded-2xl border border-border/60 bg-black/10 p-4">
              {messages.map((entry, index) => (
                <div key={index} className={entry.role === "user" ? "ml-auto max-w-[80%] rounded-2xl bg-primary/20 p-3 text-sm text-primary-foreground" : "max-w-[80%] rounded-2xl bg-white/5 p-3 text-sm"}>
                  {entry.content}
                </div>
              ))}
            </div>
            <Textarea value={message} onChange={(event: ChangeEvent<HTMLTextAreaElement>) => setMessage(event.target.value)} placeholder="Ask the agent something..." />
            <Button onClick={sendMessage}>Send message</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="font-display">Agent selection</CardTitle>
            <CardDescription>Choose the operational context for the conversation.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            <Input placeholder="Sales Agent" />
            <Input placeholder="Knowledge base" />
            <Input placeholder="Attachments" />
            <div className="rounded-2xl border border-border/60 p-4">WebSocket stream endpoint ready at <span className="text-foreground">/api/v1/chat/sessions/:id/stream</span></div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}