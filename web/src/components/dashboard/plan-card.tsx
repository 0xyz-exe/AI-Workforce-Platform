import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export function PlanCard({ name, price, features, recommended }: { name: string; price: string; features: string[]; recommended?: boolean }) {
  return (
    <Card className={recommended ? "border-primary/40 bg-primary/5" : undefined}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="font-display">{name}</CardTitle>
          {recommended ? <Badge className="bg-primary/20 text-primary">Recommended</Badge> : null}
        </div>
        <CardDescription>{price}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-2 text-sm text-muted-foreground">
        {features.map((feature) => (
          <div key={feature}>• {feature}</div>
        ))}
      </CardContent>
      <CardFooter>
        <Button className="w-full">Choose plan</Button>
      </CardFooter>
    </Card>
    );
  }
