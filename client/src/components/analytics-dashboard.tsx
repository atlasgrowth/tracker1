import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import type { Visit } from "@shared/schema";
import { formatDistance } from "date-fns";

interface AnalyticsDashboardProps {
  businessId: number;
}

export function AnalyticsDashboard({ businessId }: AnalyticsDashboardProps) {
  const { data: visits = [], isLoading } = useQuery<Visit[]>({
    queryKey: [`/api/businesses/${businessId}/visits`]
  });

  if (isLoading) {
    return <div>Loading analytics...</div>;
  }

  const visitsByDay = visits.reduce((acc, visit) => {
    const date = new Date(visit.timestamp).toISOString().split('T')[0];
    if (!acc[date]) acc[date] = [];
    acc[date].push(visit);
    return acc;
  }, {} as Record<string, Visit[]>);

  const chartData = Object.entries(visitsByDay).map(([date, dayVisits]) => ({
    date,
    visits: dayVisits.length,
    avgDuration: Math.round(dayVisits.reduce((sum, v) => sum + (v.duration || 0), 0) / dayVisits.length)
  }));

  const totalVisits = visits.length;
  const avgDuration = Math.round(visits.reduce((sum, v) => sum + (v.duration || 0), 0) / (visits.length || 1));
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Analytics</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">{totalVisits}</div>
              <div className="text-sm text-gray-500">Total Visits</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">{avgDuration}s</div>
              <div className="text-sm text-gray-500">Average Visit Duration</div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Visit Timeline</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="visits" stroke="#3b82f6" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Visits</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {visits.slice(0, 5).map((visit) => (
                <div key={visit.id} className="flex justify-between items-center">
                  <div>
                    <div className="font-medium">
                      {formatDistance(new Date(visit.timestamp), new Date(), { addSuffix: true })}
                    </div>
                    <div className="text-sm text-gray-500">
                      Source: {visit.source}
                    </div>
                  </div>
                  <div className="text-sm">
                    Duration: {visit.duration}s
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </CardContent>
    </Card>
  );
}
