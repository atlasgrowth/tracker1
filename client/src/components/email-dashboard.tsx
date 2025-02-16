
import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Mail, Users } from 'lucide-react';

export function EmailDashboard() {
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [template, setTemplate] = useState('');

  const { data: templates } = useQuery({
    queryKey: ['email-templates'],
    queryFn: () => fetch('/api/ghl/templates').then(r => r.json())
  });

  const { data: contacts } = useQuery({
    queryKey: ['contacts'],
    queryFn: () => fetch('/api/ghl/contacts').then(r => r.json())
  });

  const sendCampaign = useMutation({
    mutationFn: async () => {
      await fetch('/api/ghl/send-campaign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          templateId: template,
          subject,
          body 
        })
      });
    }
  });

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Mail className="h-5 w-5" />
            Marketing Campaigns
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Select value={template} onValueChange={setTemplate}>
              <SelectTrigger>
                <SelectValue placeholder="Select template" />
              </SelectTrigger>
              <SelectContent>
                {templates?.map((t: any) => (
                  <SelectItem key={t.id} value={t.id}>
                    {t.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Input 
              placeholder="Subject" 
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />
            <Textarea 
              placeholder="Email content..." 
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="min-h-[200px]"
            />
            <Button onClick={() => sendCampaign.mutate()}>
              Send Campaign
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            Contact List
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {contacts?.map((contact: any) => (
              <div key={contact.id} className="flex items-center justify-between p-2 border rounded">
                <div>
                  <div className="font-medium">{contact.name}</div>
                  <div className="text-sm text-gray-500">{contact.email}</div>
                </div>
                <div className="text-sm text-gray-500">
                  Added: {new Date(contact.createdAt).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
