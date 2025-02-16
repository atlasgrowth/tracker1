import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Code2 } from "lucide-react";

interface WebhookCodeProps {
  businessId: string;
}

export function WebhookCode({ businessId }: WebhookCodeProps) {
  const trackingCode = `
<!-- Add this before </body> -->
<script>
  // Record page visit duration and send to API
  let startTime = Date.now();
  window.addEventListener('beforeunload', async () => {
    const duration = Math.round((Date.now() - startTime) / 1000);
    try {
      await fetch('/api/businesses/${businessId}/visits', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          duration,
          source: document.referrer || 'direct'
        })
      });
    } catch (e) {
      console.error('Failed to record visit:', e);
    }
  });
</script>`.trim();

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline" className="gap-2">
          <Code2 className="h-4 w-4" />
          Tracking Code
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Website Tracking Code</DialogTitle>
        </DialogHeader>
        <div className="bg-gray-900 text-gray-100 p-4 rounded-md">
          <pre className="text-sm overflow-x-auto">
            <code>{trackingCode}</code>
          </pre>
        </div>
        <p className="text-sm text-gray-500">
          Add this code to your website to track visits and duration.
        </p>
      </DialogContent>
    </Dialog>
  );
}
