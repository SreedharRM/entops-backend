import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const createApproval = mutation({
  args: { taskId: v.string(), action: v.any(), status: v.string() },
  handler: async ({ db }, { taskId, action, status }) => {
    const createdAt = Date.now();
    const _id = await db.insert("approvals", { taskId, action, status, createdAt });
    return { ok: true, _id };
  },
});

export const approveTask = mutation({
  args: { taskId: v.string() },
  handler: async ({ db }, { taskId }) => {
    const latest = await db
      .query("approvals")
      .withIndex("by_taskId", (q) => q.eq("taskId", taskId))
      .collect();
    if (!latest.length) return { error: "not_found" };
    // Assume last action is the one to approve
    latest.sort((a, b) => b.createdAt - a.createdAt);
    const approval = latest[0];
    await db.insert("approvals", {
      taskId,
      action: approval.action,
      status: "approved",
      createdAt: Date.now(),
    });
    return { taskId, action: approval.action, status: "approved" };
  },
});

export const rejectTask = mutation({
  args: { taskId: v.string() },
  handler: async ({ db }, { taskId }) => {
    const latest = await db
      .query("approvals")
      .withIndex("by_taskId", (q) => q.eq("taskId", taskId))
      .collect();
    if (!latest.length) return { error: "not_found" };
    latest.sort((a, b) => b.createdAt - a.createdAt);
    const approval = latest[0];
    await db.insert("approvals", {
      taskId,
      action: approval.action,
      status: "rejected",
      createdAt: Date.now(),
    });
    return { taskId, action: approval.action, status: "rejected" };
  },
});

import { query } from "./_generated/server";

export const getByTask = query({
  args: { taskId: v.string() },
  handler: async ({ db }, { taskId }) => {
    const items = await db
      .query("approvals")
      .withIndex("by_taskId", (q) => q.eq("taskId", taskId))
      .collect();
    items.sort((a, b) => a.createdAt - b.createdAt);
    return { approvals: items };
  },
});
