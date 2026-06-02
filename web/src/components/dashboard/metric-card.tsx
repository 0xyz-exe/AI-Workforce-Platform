import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export function MetricCard({ label, value, hint, accent }: { label: string; value: string; hint: string; accent?: string }) {
  return (
    <Card className="relative overflow-hidden">
      <div className={`absolute inset-x-0 top-0 h-1 ${accent ?? "bg-primary"}`} />
      <CardHeader>
        <CardDescription>{label}</CardDescription>
        <CardTitle className="font-display text-3xl">{value}</CardTitle>
      </CardHeader>
      <CardContent className="pt-0 text-sm text-muted-foreground">{hint}</CardContent>
    </Card>
  );
}