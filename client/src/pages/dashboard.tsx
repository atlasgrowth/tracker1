import { useQuery } from "@tanstack/react-query";
import { BusinessList } from "@/components/business-list";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import type { Business } from "@shared/schema";
import { PIPELINE_STAGES } from "@/lib/constants";

export default function Dashboard() {
  const [selectedRegion, setSelectedRegion] = React.useState<string>("all");
  const { data: businesses, isLoading } = useQuery<Business[]>({
    queryKey: ["/api/businesses"]
  });

  const regions = [
    { id: "all", name: "All Regions" },
    { id: "arkansas", name: "Arkansas" },
    { id: "alabama", name: "Alabama" }
  ];

  const filteredBusinesses = React.useMemo(() => {
    if (!businesses) return [];
    return selectedRegion === "all" 
      ? businesses 
      : businesses.filter(b => b.region === selectedRegion);
  }, [businesses, selectedRegion]);

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
  const businessesByStage = filteredBusinesses.reduce((acc, business) => {
    const stage = business.pipelineStage || "website_created";
    if (!acc[stage]) acc[stage] = [];
    acc[stage].push(business);
    return acc;
  }, {} as Record<string, Business[]>);

  return (
    <div className="container mx-auto p-4 space-y-8">
      <Card className="border-0 shadow-lg">
        <CardHeader className="border-b bg-gradient-to-r from-blue-50 to-blue-100">
          <div className="flex justify-between items-center">
            <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
              Pipeline Dashboard
            </CardTitle>
            <select 
              value={selectedRegion}
              onChange={(e) => setSelectedRegion(e.target.value)}
              className="px-4 py-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {regions.map(region => (
                <option key={region.id} value={region.id}>{region.name}</option>
              ))}
            </select>
          </div>
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
