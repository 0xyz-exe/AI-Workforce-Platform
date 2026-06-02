import { Bot, ToggleLeft } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export function AgentCard({ name, description, category, enabled, onAction }: { name: string; description: string; category: string; enabled?: boolean; onAction?: () => void }) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div>
            <CardTitle className="flex items-center gap-2 font-display">
              <Bot className="h-5 w-5 text-primary" /> {name}
            </CardTitle>
            <CardDescription className="mt-1">{description}</CardDescription>
          </div>
          <Badge>{category}</Badge>
        </div>
      </CardHeader>
      <CardContent className="text-sm text-muted-foreground">Status: {enabled ? "Enabled" : "Disabled"}</CardContent>
      <CardFooter>
        <Button variant="outline" className="gap-2" onClick={onAction}>
          <ToggleLeft className="h-4 w-4" /> {enabled ? "Disable" : "Enable"}
        </Button>
      </CardFooter>
    </Card>
  );
}