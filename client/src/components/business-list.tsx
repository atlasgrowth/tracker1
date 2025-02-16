import { Link } from "wouter";
import { Card, CardContent } from "@/components/ui/card";
import { Building2, Star, MessageSquare } from "lucide-react";
import type { Business } from "@shared/schema";

interface BusinessListProps {
  businesses: Business[];
}

export function BusinessList({ businesses }: BusinessListProps) {
  return (
    <div className="space-y-4">
      {businesses.map((business) => (
        <Link key={business.siteId} href={`/business/${business.siteId}`}>
          <Card className="cursor-pointer hover:border-blue-500 transition-colors">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Building2 className="h-4 w-4 text-gray-500" />
                    <h3 className="font-medium">{business.name}</h3>
                  </div>
                  <div className="text-sm text-gray-500">
                    {business.city}
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  {business.rating && (
                    <div className="flex items-center gap-1">
                      <Star className="h-4 w-4 text-yellow-400 fill-yellow-400" />
                      <span className="text-sm">{business.rating}</span>
                    </div>
                  )}
                  {business.notes && (
                    <MessageSquare className="h-4 w-4 text-blue-500" />
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </Link>
      ))}
    </div>
  );
}
