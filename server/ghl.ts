
import fetch from 'node-fetch';

const GHL_API_KEY = process.env.GHL_API_KEY;
const GHL_LOCATION_ID = process.env.GHL_LOCATION_ID;
const GHL_API_URL = 'https://rest.gohighlevel.com/v1';

export async function getTemplates() {
  const response = await fetch(`${GHL_API_URL}/email-templates`, {
    headers: {
      Authorization: `Bearer ${GHL_API_KEY}`,
      'Content-Type': 'application/json',
      Version: '2021-07-28'
    }
  });
  return response.json();
}

export async function getContacts() {
  const response = await fetch(`${GHL_API_URL}/contacts?locationId=${GHL_LOCATION_ID}`, {
    headers: {
      Authorization: `Bearer ${GHL_API_KEY}`,
      'Content-Type': 'application/json',
      Version: '2021-07-28'
    }
  });
  return response.json();
}

export async function sendCampaign(templateId: string, subject: string, body: string) {
  const response = await fetch(`${GHL_API_URL}/campaigns`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${GHL_API_KEY}`,
      'Content-Type': 'application/json',
      Version: '2021-07-28'
    },
    body: JSON.stringify({
      templateId,
      subject,
      body,
      locationId: GHL_LOCATION_ID
    })
  });
  return response.json();
}
