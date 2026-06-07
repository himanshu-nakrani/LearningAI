import type { ReactNode } from "react";
import styles from "./Ascii.module.css";

export function Ascii({ children }: { children: ReactNode }) {
  return <div className={styles.root}>{children}</div>;
}
