import type { ReactNode } from "react";
import styles from "./Callout.module.css";

type Variant = "tip" | "warn" | "gap";

export function Callout({
  variant = "tip",
  title,
  children,
}: {
  variant?: Variant;
  title?: string;
  children: ReactNode;
}) {
  return (
    <aside className={`${styles.root} ${styles[variant]}`}>
      {title && <strong className={styles.title}>{title}</strong>}
      <div className={styles.body}>{children}</div>
    </aside>
  );
}
