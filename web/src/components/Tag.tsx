import type { ReactNode } from "react";
import styles from "./Tag.module.css";

type Kind = "core" | "concept" | "prod" | "gap" | "neutral";

export function Tag({ kind = "neutral", children }: { kind?: Kind; children: ReactNode }) {
  return <span className={`${styles.root} ${styles[kind]}`}>{children}</span>;
}
