"use client";
import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from "react";
import styles from "./IconButton.module.css";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  /** Accessible label is required for icon-only buttons. */
  "aria-label": string;
};

export const IconButton = forwardRef<HTMLButtonElement, Props>(function IconButton(
  { className, children, ...rest },
  ref,
) {
  const cls = [styles.btn, className].filter(Boolean).join(" ");
  return (
    <button type="button" className={cls} ref={ref} {...rest}>
      {children}
    </button>
  );
});
