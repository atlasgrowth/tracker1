import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertBusinessSchema, PIPELINE_STAGES } from "@shared/schema";
import { z } from "zod";

export async function registerRoutes(app: Express): Promise<Server> {
  // Get all businesses
  app.get("/api/businesses", async (req, res) => {
    const businesses = await storage.getBusinesses();
    res.json(businesses);
  });

  // Get single business
  app.get("/api/businesses/:siteId", async (req, res) => {
    const business = await storage.getBusiness(req.params.siteId);
    if (!business) return res.status(404).json({ message: "Business not found" });
    res.json(business);
  });

  // Create business
  app.post("/api/businesses", async (req, res) => {
    const result = insertBusinessSchema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.errors });
    }
    const business = await storage.createBusiness(result.data);
    res.status(201).json(business);
  });

  // Update business stage
  app.patch("/api/businesses/:siteId/stage", async (req, res) => {
    const schema = z.object({ stage: z.enum(PIPELINE_STAGES) });
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.errors });
    }

    try {
      const business = await storage.updateBusinessStage(
        req.params.siteId,
        result.data.stage
      );
      res.json(business);
    } catch (error) {
      res.status(404).json({ message: "Business not found" });
    }
  });

  // Update business notes
  app.patch("/api/businesses/:siteId/notes", async (req, res) => {
    const schema = z.object({ notes: z.string() });
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.errors });
    }

    try {
      const business = await storage.updateBusinessNotes(
        req.params.siteId,
        result.data.notes
      );
      res.json(business);
    } catch (error) {
      res.status(404).json({ message: "Business not found" });
    }
  });

  // Record visit
  app.post("/api/businesses/:siteId/visits", async (req, res) => {
    const schema = z.object({
      duration: z.number(),
      source: z.string()
    });

    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.errors });
    }

    try {
      const business = await storage.getBusiness(req.params.siteId);
      if (!business) {
        return res.status(404).json({ message: "Business not found" });
      }

      const visit = await storage.recordVisit(
        business.id,
        result.data.duration,
        result.data.source
      );
      res.status(201).json(visit);
    } catch (error) {
      console.error('Error recording visit:', error);
      res.status(500).json({ message: "Failed to record visit" });
    }
  });

  // Get business visits
  app.get("/api/businesses/:siteId/visits", async (req, res) => {
    try {
      const business = await storage.getBusiness(req.params.siteId);
      if (!business) {
        return res.status(404).json({ message: "Business not found" });
      }
      const visits = await storage.getVisits(req.params.siteId);
      res.json(visits);
    } catch (error) {
      console.error('Error fetching visits:', error);
      res.status(500).json({ message: "Failed to fetch visits" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
