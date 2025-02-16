
import { Link } from "wouter";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Mail, Pipeline } from "lucide-react";

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-8 bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
        Business Management Dashboard
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Link href="/pipeline">
          <Card className="cursor-pointer hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Pipeline className="h-6 w-6" />
                Pipeline Dashboard
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                View and manage your business pipeline stages and analytics
              </p>
            </CardContent>
          </Card>
        </Link>
        <Link href="/email">
          <Card className="cursor-pointer hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Mail className="h-6 w-6" />
                Email Marketing
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Manage your email campaigns and contact lists
              </p>
            </CardContent>
          </Card>
        </Link>
      </div>
    </div>
  );
}
