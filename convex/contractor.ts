import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

function genId() {
  return (
    Date.now().toString(36) + Math.random().toString(36).slice(2, 10)
  ).toLowerCase();
}

// Create a new contractor
export const createContractor = mutation({
  args: {
    name: v.string(),
    contractorId: v.string(), // external ID (e.g., "EMP-4821")
    jobTitle: v.string(),
    department: v.string(),
    email: v.string(),
    phone: v.string(),
    dateOfJoining: v.string(), // ISO date string
    location: v.string(),
    manager: v.string(),
  },
  handler: async (
    { db },
    {
      name,
      contractorId,
      jobTitle,
      department,
      email,
      phone,
      dateOfJoining,
      location,
      manager,
    }
  ) => {
    const createdAt = Date.now();
    await db.insert("contractors", {
      contractorId,
      name,
      jobTitle,
      department,
      email,
      phone,
      dateOfJoining,
      location,
      manager,
      createdAt,
    });
    return { contractorId };
  },
});

// Update contractor details
export const updateContractor = mutation({
  args: {
    contractorId: v.string(),
    updates: v.object({
      name: v.optional(v.string()),
      jobTitle: v.optional(v.string()),
      department: v.optional(v.string()),
      email: v.optional(v.string()),
      phone: v.optional(v.string()),
      dateOfJoining: v.optional(v.string()),
      location: v.optional(v.string()),
      manager: v.optional(v.string()),
    }),
  },
  handler: async ({ db }, { contractorId, updates }) => {
    const doc = await db
      .query("contractors")
      .withIndex("by_contractorId", (q) => q.eq("contractorId", contractorId))
      .first();
    if (!doc) return { error: "not_found" };
    await db.patch(doc._id, updates);
    return { contractorId, ...updates };
  },
});

// Get a single contractor by ID
export const getContractor = query({
  args: { contractorId: v.string() },
  handler: async ({ db }, { contractorId }) => {
    const doc = await db
      .query("contractors")
      .withIndex("by_contractorId", (q) => q.eq("contractorId", contractorId))
      .first();
    if (!doc) return { error: "not_found" };
    return doc;
  },
});

// List all contractors
export const listContractors = query({
  handler: async ({ db }) => {
    const docs = await db.query("contractors").collect();
    return docs.map((d) => ({
      contractorId: d.contractorId,
      name: d.name,
      jobTitle: d.jobTitle,
      department: d.department,
      location: d.location,
      createdAt: d.createdAt,
    }));
  },
});
