import type { MDXComponents } from "mdx/types";
import { Callout } from "./src/components/Callout";
import { Ascii } from "./src/components/Ascii";
import { Tag } from "./src/components/Tag";

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
    Callout,
    Ascii,
    Tag,
  };
}
