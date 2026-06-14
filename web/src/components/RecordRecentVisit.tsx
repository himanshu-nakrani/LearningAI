"use client";
import { useEffect } from "react";
import { recordRecentVisit } from "./ContinueLearning";
import type { GuideMeta } from "@/lib/guides";

/**
 * Invisible client component that records this guide as the most-recent
 * visit (used by the ContinueLearning card on the homepage).
 */
export function RecordRecentVisit({ guide }: { guide: GuideMeta }) {
  useEffect(() => {
    recordRecentVisit(guide);
  }, [guide]);
  return null;
}
