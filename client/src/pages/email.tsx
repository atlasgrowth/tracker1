
import { EmailDashboard } from "@/components/email-dashboard";
import { Link } from "wouter";
import { ChevronLeft } from "lucide-react";

export default function Email() {
  return (
    <div className="container mx-auto p-4">
      <Link href="/" className="inline-flex items-center mb-4 text-blue-600 hover:text-blue-800">
        <ChevronLeft className="h-4 w-4" />
        Back to Home
      </Link>
      <EmailDashboard />
    </div>
  );
}
