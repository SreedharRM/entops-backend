import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

function genId() {
  return (
    Date.now().toString(36) + Math.random().toString(36).slice(2, 10)
  ).toLowerCase();
}

export const createTask = mutation({
  args: {
    type: v.string(),
    data: v.any(),
    status: v.string(),
  },
  handler: async ({ db }, { type, data, status }) => {
    const taskId = genId();
    const createdAt = Date.now();
    await db.insert("tasks", { taskId, type, data, status, createdAt });
    return { taskId };
  },
});

export const updateTaskStatus = mutation({
  args: { taskId: v.string(), status: v.string() },
  handler: async ({ db }, { taskId, status }) => {
    const doc = await db
      .query("tasks")
      .withIndex("by_taskId", (q) => q.eq("taskId", taskId))
      .first();
    if (!doc) return { error: "not_found" };
    await db.patch(doc._id, { status });
    return { taskId, status };
  },
});

export const getTask = query({
  args: { taskId: v.string() },
  handler: async ({ db }, { taskId }) => {
    const doc = await db
      .query("tasks")
      .withIndex("by_taskId", (q) => q.eq("taskId", taskId))
      .first();
    if (!doc) return { error: "not_found" };
    return {
      taskId: doc.taskId,
      type: doc.type,
      data: doc.data,
      status: doc.status,
      createdAt: doc.createdAt,
    };
  },
});

export const listTasks = query({
  handler: async ({ db }) => {
    const docs = await db.query("tasks").collect();
    return docs.map((d) => ({
      taskId: d.taskId,
      type: d.type,
      status: d.status,
      createdAt: d.createdAt,
    }));
  },
});

export const getAllTasks = query({
  handler: async ({ db }) => {
    return await db.query("tasks").collect();
  },
});
