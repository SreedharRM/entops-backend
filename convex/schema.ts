import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  tasks: defineTable({
    taskId: v.string(),
    type: v.string(),
    data: v.any(),
    status: v.string(),
    createdAt: v.number(),
  })
    .index("by_taskId", ["taskId"])
    .index("by_status", ["status", "createdAt"]),

  events: defineTable({
    taskId: v.string(),
    status: v.string(),
    details: v.any(),
    timestamp: v.string(),
    createdAt: v.number(),
  }).index("by_taskId", ["taskId", "createdAt"]),

  approvals: defineTable({
    taskId: v.string(),
    action: v.any(),
    status: v.string(), // pending | approved | rejected
    createdAt: v.number(),
  }).index("by_taskId", ["taskId", "createdAt"]),

  contractors: defineTable({
    contractorId: v.string(),  // stable string ID (e.g. "EMP-4821")
    name: v.string(),
    jobTitle: v.string(),
    department: v.string(),
    email: v.string(),
    phone: v.string(),
    dateOfJoining: v.string(), // ISO string recommended
    location: v.string(),
    manager: v.string(),
    createdAt: v.number(),
  }).index("by_contractorId", ["contractorId"])
});
