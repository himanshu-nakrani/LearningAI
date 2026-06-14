import type { HTMLAttributes, ReactNode } from "react";
import styles from "./Card.module.css";

type Props = HTMLAttributes<HTMLDivElement> & {
  children: ReactNode;
  /** When true, the card lifts subtly on hover. Default: false. */
  interactive?: boolean;
  /** Tighten padding for nested cards in lists. */
  compact?: boolean;
};

export function Card({ children, interactive, compact, className, ...rest }: Props) {
  const cls = [
    styles.card,
    interactive ? styles.interactive : null,
    compact ? styles.compact : null,
    className,
  ]
    .filter(Boolean)
    .join(" ");
  return (
    <div className={cls} {...rest}>
      {children}
    </div>
  );
}
