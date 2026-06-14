import type { ReactNode } from "react";
import styles from "./Chip.module.css";

type Intent = "neutral" | "core" | "advanced" | "reference" | "warning" | "lavender" | "cobalt" | "success";
type Size = "sm" | "md";

type Props = {
  children: ReactNode;
  intent?: Intent;
  size?: Size;
  className?: string;
};

export function Chip({ children, intent = "neutral", size = "sm", className }: Props) {
  const cls = [styles.chip, styles[intent], styles[size], className].filter(Boolean).join(" ");
  return <span className={cls}>{children}</span>;
}
