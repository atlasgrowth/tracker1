import { useQuery } from "@tanstack/react-query";
import { BusinessList } from "@/components/business-list";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import type { Business } from "@shared/schema";
import { PIPELINE_STAGES } from "@/lib/constants";

export default function Dashboard() {
  const { data: businesses, isLoading } = useQuery<Business[]>({
    queryKey: ["/api/businesses"]
  });

  if (isLoading) {
    return (
      <div className="container mx-auto p-4">
        <Card>
          <CardHeader className="border-b">
            <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
              Pipeline Dashboard
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <Skeleton className="h-[400px] w-full" />
          </CardContent>
        </Card>
      </div>
    );
  }

  // Group businesses by pipeline stage
  const businessesByStage = businesses?.reduce((acc, business) => {
    const stage = business.pipelineStage || "website_created";
    if (!acc[stage]) acc[stage] = [];
    acc[stage].push(business);
    return acc;
  }, {} as Record<string, Business[]>);

  return (
    <div className="container mx-auto p-4 space-y-8">
      <Card className="border-0 shadow-lg">
        <CardHeader className="border-b bg-gradient-to-r from-blue-50 to-blue-100">
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
            Pipeline Dashboard
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {Object.entries(PIPELINE_STAGES).map(([key, { label, color }]) => (
              <Card key={key} className="shadow-md">
                <CardHeader className={`${color} text-white`}>
                  <CardTitle className="text-lg font-semibold">{label}</CardTitle>
                  <div className="text-sm opacity-90">
                    {businessesByStage?.[key]?.length || 0} businesses
                  </div>
                </CardHeader>
                <CardContent className="p-4">
                  {businessesByStage?.[key] && (
                    <BusinessList businesses={businessesByStage[key]} />
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
