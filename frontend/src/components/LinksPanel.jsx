import { ExternalLink, Link2 } from "lucide-react";
import { cn } from "../lib/utils";

function extractLinks(htmlContent) {
  if (!htmlContent) return [];
  const doc = new DOMParser().parseFromString(htmlContent, "text/html");
  const anchors = doc.querySelectorAll("a[href]");
  const seen = new Set();
  const links = [];
  for (const a of anchors) {
    const href = a.href?.trim();
    if (!href || href === "#" || href.startsWith("javascript:")) continue;
    if (seen.has(href)) continue;
    seen.add(href);
    links.push({ url: href, text: a.textContent?.trim() || href });
  }
  return links;
}

function extractAllLinks(agents) {
  if (!agents) return [];
  const allLinks = [];
  const seen = new Set();
  for (const [, content] of Object.entries(agents)) {
    if (!content || typeof content !== "string") continue;
    const links = extractLinks(content);
    for (const link of links) {
      if (!seen.has(link.url)) {
        seen.add(link.url);
        allLinks.push(link);
      }
    }
  }
  return allLinks;
}

export default function LinksPanel({ agents }) {
  const links = extractAllLinks(agents);

  if (links.length === 0) return null;

  return (
    <div className="mt-4 p-4 bg-white border border-[var(--color-border)] rounded-xl shadow-sm">
      <div className="flex items-center gap-2 mb-3">
        <Link2 size={14} className="text-[var(--color-accent)]" />
        <h3 className="text-sm font-semibold text-[var(--color-foreground)]">
          Reference Links
        </h3>
        <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-[#f4f4f5] text-[var(--color-muted)] font-medium">
          {links.length}
        </span>
      </div>
      <div className="space-y-1.5 max-h-64 overflow-y-auto">
        {links.map((link, i) => (
          <a
            key={link.url}
            href={link.url}
            target="_blank"
            rel="noopener noreferrer"
            className={cn(
              "flex items-start gap-2 px-2.5 py-2 rounded-lg text-xs transition-colors",
              "hover:bg-[#f4f4f5] group"
            )}
          >
            <span className="text-[var(--color-muted)] font-mono flex-shrink-0 mt-0.5">
              {i + 1}.
            </span>
            <div className="flex-1 min-w-0">
              <div className="text-[var(--color-foreground)] truncate group-hover:text-[var(--color-accent)]">
                {link.text || link.url}
              </div>
              <div className="text-[var(--color-muted)] truncate mt-0.5 text-[10px]">
                {link.url}
              </div>
            </div>
            <ExternalLink
              size={12}
              className="text-[var(--color-muted)] group-hover:text-[var(--color-accent)] flex-shrink-0 mt-0.5 opacity-0 group-hover:opacity-100 transition-opacity"
            />
          </a>
        ))}
      </div>
    </div>
  );
}
