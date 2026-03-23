import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

export default function RetirementChart({ retirementStat }) {
  if (!retirementStat) return;

  console.log(retirementStat);

  const chartData = retirementStat.map((item) => ({
    year: item.year,
    count: item.count,
  }));

  return (
    <div style={{ width: "100%", height: "100%" }}>
      <ResponsiveContainer>
        <LineChart
          style={{
            width: "100%",
            height: 300,
          }}
          data={chartData}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="year" />
          <YAxis allowDecimals={false} />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="count"
            stroke="#16a34a"
            strokeWidth={3}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
