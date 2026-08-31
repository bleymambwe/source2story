import { z } from "zod";

export const visualTypeSchema = z.enum([
  "factual_chart",
  "kinetic_type",
  "illustrative",
  "transition",
]);

export const verificationStatusSchema = z.enum([
  "verified",
  "unsupported_claim",
  "value_mismatch",
  "source_conflict",
]);

export const sceneSchema = z.object({
  scene_id: z.string(),
  narration: z.string(),
  visual_type: visualTypeSchema,
  visual_prompt: z.string(),
  value: z.string().optional(),
  unit: z.string().optional(),
  status: verificationStatusSchema.default("verified"),
  detail: z.string().optional(),
  duration_s: z.number().positive().default(5),
});

export const explainerSchema = z.object({
  title: z.string(),
  scenes: z.array(sceneSchema).min(1),
});

export type Scene = z.infer<typeof sceneSchema>;
export type ExplainerProps = z.infer<typeof explainerSchema>;
export type VerificationStatus = z.infer<typeof verificationStatusSchema>;

export const FPS = 30;
