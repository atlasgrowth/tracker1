import { Business, Visit, InsertBusiness, PIPELINE_STAGES } from "@shared/schema";
import { promises as fs } from 'fs';
import { join } from 'path';

export interface IStorage {
  // Business operations
  getBusinesses(): Promise<Business[]>;
  getBusiness(siteId: string): Promise<Business | undefined>;
  createBusiness(business: InsertBusiness): Promise<Business>;
  updateBusinessStage(siteId: string, stage: string): Promise<Business>;
  updateBusinessNotes(siteId: string, notes: string): Promise<Business>;

  // Visit operations
  recordVisit(businessId: number, duration: number, source: string): Promise<Visit>;
  getVisits(businessId: number): Promise<Visit[]>;
}

interface MetadataBusinesses {
  last_updated: string;
  business_count: number;
  businesses: {
    [key: string]: {
      name: string;
      site_id: string;
      place_id: string;
      rating: number;
      total_reviews: number;
      scores: {
        photo_score: number;
        facebook_score: number;
      };
      has_website: boolean;
      has_facebook: boolean;
      city: string;
    };
  };
}

export class MemStorage implements IStorage {
  private businesses: Map<string, Business>;
  private visits: Map<number, Visit[]>;
  private currentId: number;
  private visitId: number;

  constructor() {
    this.businesses = new Map();
    this.visits = new Map();
    this.currentId = 1;
    this.visitId = 1;

    // Load initial data from metadata file
    this.initializeBusinesses().catch(error => {
      console.error('Failed to initialize businesses:', error);
      process.exit(1); // Exit if we can't load the businesses
    });
  }

  private async loadMetadataFromFile(): Promise<MetadataBusinesses> {
    try {
      const url = 'https://raw.githubusercontent.com/atlasgrowth/Arkansasplumbers/main/data/processed/metadata.json';
      console.log('Fetching metadata from:', url);

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to fetch metadata: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Parsed businesses count:', Object.keys(data.businesses || {}).length);

      if (!data || typeof data !== 'object' || !data.businesses) {
        throw new Error('Invalid metadata structure - missing businesses object');
      }

      return data as MetadataBusinesses;
    } catch (error) {
      console.error('Error loading metadata:', error);
      throw error;
    }
  }

  private async initializeBusinesses() {
    try {
      const metadata = await this.loadMetadataFromFile();
      const businessesData = metadata.businesses;

      console.log('Initializing businesses, found:', Object.keys(businessesData).length);

      // Load all businesses from the metadata
      Object.entries(businessesData).forEach(([siteId, business]) => {
        const id = this.currentId++;
        const newBusiness: Business = {
          id,
          siteId,
          name: business.name,
          placeId: business.place_id,
          rating: business.rating ?? null,
          totalReviews: business.total_reviews ?? null,
          hasWebsite: business.has_website ?? false,
          hasFacebook: business.has_facebook ?? false,
          city: business.city ?? null,
          pipelineStage: "website_created",
          lastViewed: null,
          totalViews: 0,
          notes: null,
          metadata: {
            scores: business.scores ?? { photo_score: 0, facebook_score: 0 }
          }
        };
        this.businesses.set(siteId, newBusiness);
      });

      console.log(`Successfully loaded ${this.businesses.size} businesses from GitHub metadata`);
    } catch (error) {
      console.error('Error initializing businesses:', error);
      throw error;
    }
  }

  async getBusinesses(): Promise<Business[]> {
    return Array.from(this.businesses.values());
  }

  async getBusiness(siteId: string): Promise<Business | undefined> {
    return this.businesses.get(siteId);
  }

  async createBusiness(insertBusiness: InsertBusiness): Promise<Business> {
    const id = this.currentId++;
    const business: Business = {
      ...insertBusiness,
      id,
      pipelineStage: "website_created",
      lastViewed: null,
      totalViews: 0,
      notes: null,
      metadata: {}
    };
    this.businesses.set(business.siteId, business);
    return business;
  }

  async updateBusinessStage(siteId: string, stage: string): Promise<Business> {
    const business = await this.getBusiness(siteId);
    if (!business) throw new Error("Business not found");

    // Update stage
    business.pipelineStage = stage;
    this.businesses.set(siteId, business);

    console.log(`Updated pipeline stage for ${business.name} to ${stage}`);
    return business;
  }

  async updateBusinessNotes(siteId: string, notes: string): Promise<Business> {
    const business = await this.getBusiness(siteId);
    if (!business) throw new Error("Business not found");

    business.notes = notes;
    this.businesses.set(siteId, business);
    return business;
  }

  async recordVisit(siteId: string, duration: number, source: string): Promise<Visit> {
    const visit: Visit = {
      id: this.visitId++,
      siteId,
      timestamp: new Date(),
      duration,
      source
    };

    const business = await this.getBusiness(siteId);
    if (!business) throw new Error("Business not found");

    const businessVisits = this.visits.get(business.id) || [];
    businessVisits.push(visit);
    this.visits.set(business.id, businessVisits);

    // Update business visit stats and pipeline stage 
    const business = await this.getBusiness(siteId);
    if (business) {
      business.lastViewed = visit.timestamp;
      business.totalViews = (business.totalViews || 0) + 1;

      // Update pipeline stage to website_viewed if it's in an earlier stage
      console.log(`Current pipeline stage for ${business.name}: ${business.pipelineStage}`);
      if (business.pipelineStage === "website_created" || business.pipelineStage === "website_sent") {
        business.pipelineStage = "website_viewed";
        console.log(`Updated pipeline stage to website_viewed for business ${business.name}`);
      } else {
        console.log(`No stage update needed for ${business.name} (current stage: ${business.pipelineStage})`);
      }

      this.businesses.set(business.siteId, business);
    }

    console.log(`Recorded visit for business ${businessId}, duration: ${duration}s, source: ${source}`);
    return visit;
  }

  async getVisits(siteId: string): Promise<Visit[]> {
    const business = await this.getBusiness(siteId);
    if (!business) return [];
    return this.visits.get(business.id) || [];
  }
}

export const storage = new MemStorage();
