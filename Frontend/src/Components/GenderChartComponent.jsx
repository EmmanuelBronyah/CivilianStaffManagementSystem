import { ResponsiveContainer, PieChart, Pie, Tooltip, Legend } from "recharts";

export default function GenderChart({ genderStat }) {
  if (!genderStat) return;

  const data = genderStat.map((item, index) => ({
    ...item,
    fill: index === 0 ? "#22c55e" : "#004700",
  }));

  return (
    <div style={{ width: "100%", height: "250px" }}>
      <ResponsiveContainer>
        <PieChart style={{ fontWeight: "bolder" }}>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            labelLine={false}
          />
          <Tooltip />
          <Legend verticalAlign="bottom" />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
