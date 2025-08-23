import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const addEvent = mutation({
  args: {
    taskId: v.string(),
    status: v.string(),
    details: v.any(),
    timestamp: v.string(),
  },
  handler: async ({ db }, { taskId, status, details, timestamp }) => {
    const createdAt = Date.now();
    const _id = await db.insert("events", {
      taskId,
      status,
      details,
      timestamp,
      createdAt,
    });
    return { ok: true, _id };
  },
});

export const getEvents = query({
  args: { taskId: v.string() },
  handler: async ({ db }, { taskId }) => {
    const items = await db
      .query("events")
      .withIndex("by_taskId", (q) => q.eq("taskId", taskId))
      .collect();
    items.sort((a, b) => a.createdAt - b.createdAt);
    return { events: items };
  },
});
