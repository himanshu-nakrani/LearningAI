import type { ReactNode } from "react";
import styles from "./MetadataRow.module.css";

export type MetadataItem = {
  icon?: ReactNode;
  label: string;
};

type Props = {
  items: MetadataItem[];
  size?: "sm" | "md";
  className?: string;
};

export function MetadataRow({ items, size = "sm", className }: Props) {
  if (!items.length) return null;
  const cls = [styles.row, styles[size], className].filter(Boolean).join(" ");
  return (
    <div className={cls}>
      {items.map((it, i) => (
        <span key={i} className={styles.item}>
          {i > 0 && <span className={styles.sep} aria-hidden>·</span>}
          {it.icon && <span className={styles.icon}>{it.icon}</span>}
          <span>{it.label}</span>
        </span>
      ))}
    </div>
  );
}
