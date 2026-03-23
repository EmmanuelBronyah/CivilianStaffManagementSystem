import { ResponsiveContainer, PieChart, Pie, Tooltip, Legend } from "recharts";

export default function GenderChart({ genderStat }) {
  if (!genderStat) return;

  const data = genderStat.map((item, index) => ({
    ...item,
    fill: index === 0 ? "#22c55e" : "#004700",
  }));

  const renderLabel = ({ percent }) => `${(percent * 100).toFixed(0)}%`;

  return (
    <div style={{ width: "100%", height: "100%" }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={90}
            label={renderLabel}
            labelLine={false}
          />
          <Tooltip />
          <Legend verticalAlign="bottom" height={36} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
