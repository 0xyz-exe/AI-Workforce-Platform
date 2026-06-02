export function UsageChart({ values }: { values: number[] }) {
  const max = Math.max(...values, 1);
  const viewBoxHeight = 160;

  return (
    <div className="rounded-2xl border border-border/60 bg-black/10 p-4">
      <svg viewBox={`0 0 ${values.length * 40} ${viewBoxHeight}`} className="h-44 w-full" role="img" aria-label="Usage chart">
        {values.map((value, index) => {
          const barHeight = (value / max) * (viewBoxHeight - 20);
          const x = index * 40 + 6;
          const y = viewBoxHeight - barHeight - 12;
          return (
            <g key={index}>
              <rect x={x} y={y} width={28} height={barHeight} rx={10} fill="url(#usageGradient)" />
              <text x={x + 14} y={viewBoxHeight - 2} textAnchor="middle" className="fill-muted-foreground text-[10px]">
                {index + 1}
              </text>
            </g>
          );
        })}
        <defs>
          <linearGradient id="usageGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#34d399" />
            <stop offset="55%" stopColor="#22d3ee" />
            <stop offset="100%" stopColor="#0ea5e9" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
}