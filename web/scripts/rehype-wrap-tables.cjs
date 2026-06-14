/**
 * Tiny MDX/remark plugin: post-processes raw HTML <table> elements in MDX
 * content so they render as valid HTML.
 *
 *  1. Groups bare <tr> children of <table> into <thead> (if the first row is
 *     all <th>) and <tbody> (the rest). Browsers auto-insert <tbody> at parse
 *     time, but React 19's hydration check flags tables whose <tr> isn't
 *     wrapped in the source HTML.
 *
 * MDX represents raw HTML in the source as mdxJsxFlowElement / mdxJsxTextElement
 * nodes (one per element), so this plugin walks those and rewrites their
 * children in place.
 *
 * No external dependencies.
 */
function rehypeWrapTables() {
  return (tree) => {
    fix(tree);
  };
}

function fix(node) {
  if (!node || !Array.isArray(node.children)) return;
  for (const child of node.children) fix(child);
  if (!isJsxElement(node, "table")) return;

  const theadRows = [];
  const tbodyRows = [];
  const passthrough = [];
  let firstRow = true;
  for (const child of node.children) {
    if (isJsxElement(child, "tr")) {
      const isAllTh =
        Array.isArray(child.children) &&
        child.children.length > 0 &&
        child.children.every((c) => isJsxElement(c, "th"));
      if (isAllTh && firstRow) {
        theadRows.push(child);
      } else {
        tbodyRows.push(child);
      }
      firstRow = false;
    } else {
      passthrough.push(child);
    }
  }

  const newChildren = [...passthrough];
  if (theadRows.length) {
    newChildren.push({
      type: "mdxJsxFlowElement",
      name: "thead",
      attributes: [],
      children: theadRows,
    });
  }
  if (tbodyRows.length) {
    newChildren.push({
      type: "mdxJsxFlowElement",
      name: "tbody",
      attributes: [],
      children: tbodyRows,
    });
  }
  node.children = newChildren;
}

/** MDX raw-HTML elements appear as either mdxJsxFlowElement (block) or
 *  mdxJsxTextElement (inline). */
function isJsxElement(node, name) {
  if (!node) return false;
  const isJsx = node.type === "mdxJsxFlowElement" || node.type === "mdxJsxTextElement";
  return isJsx && node.name === name;
}

module.exports = rehypeWrapTables;
