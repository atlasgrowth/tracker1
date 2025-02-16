import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import type { Visit } from "@shared/schema";
import { formatDistance } from "date-fns";

interface AnalyticsDashboardProps {
  businessId: number;
  siteId: string;
}

export function AnalyticsDashboard({ businessId, siteId }: AnalyticsDashboardProps) {
  const { data: visits = [], isLoading: visitsLoading } = useQuery<Visit[]>({
    queryKey: [`/api/businesses/${siteId}/visits`]
  });

  const { data: analytics, isLoading: analyticsLoading } = useQuery({
    queryKey: [`/api/businesses/${siteId}/analytics`],
    queryFn: async () => {
      const resp = await fetch(`/api/businesses/${siteId}/analytics`);
      if (!resp.ok) throw new Error('Failed to fetch analytics');
      return resp.json();
    }
  });

  if (visitsLoading || analyticsLoading) {
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

  // Prepare devices data for pie chart
  const deviceData = analytics?.deviceStats?.browsers 
    ? Object.entries(analytics.deviceStats.browsers).map(([browser, count]) => ({
        name: browser,
        value: count
      }))
    : [];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Analytics</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
          {analytics?.totalVisits && (
            <Card>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold">{analytics.totalVisits}</div>
                <div className="text-sm text-gray-500">Unique Sessions</div>
              </CardContent>
            </Card>
          )}
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

        {deviceData.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Browser Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={deviceData}
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                      label={({name, value}) => `${name}: ${value}`}
                    >
                      {deviceData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        )}

        {analytics?.pageViews && (
          <Card>
            <CardHeader>
              <CardTitle>Popular Pages</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(analytics.pageViews).map(([path, views]) => (
                  <div key={path} className="flex justify-between items-center">
                    <div className="font-medium">{path}</div>
                    <div className="text-sm text-gray-500">{views} views</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

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