import React from 'react';
import { InlineMath, BlockMath } from 'react-katex';

export const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60).toString().padStart(2, '0');
  const s = (seconds % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
};

export const formatDate = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

export const getScoreColor = (percentage) => {
  if (percentage >= 80) return 'text-green-500';
  if (percentage >= 50) return 'text-yellow-500';
  return 'text-red-500';
};

/**
 * Mobile-Safe LaTeX & Code Parser
 * - Handles code blocks (```...```) with horizontal scroll and dark styling
 * - Handles block math ($$...$$) with responsive scrollable container
 * - Handles inline math ($...$) with touch-safe inline-block container
 */
export const parseLaTeX = (text) => {
  if (!text) return null;

  // 1. Split code blocks (```...```)
  const codeBlocks = text.split(/(```[\s\S]*?```)/g);

  return codeBlocks.map((chunk, cIdx) => {
    if (chunk.startsWith('```') && chunk.endsWith('```')) {
      // Remove opening and closing backticks and optional language identifier
      const lines = chunk.slice(3, -3).trim().split('\n');
      let lang = '';
      if (lines.length > 0 && /^[a-zA-Z0-9_-]+$/.test(lines[0].trim())) {
        lang = lines[0].trim();
        lines.shift();
      }
      const code = lines.join('\n');
      return (
        <div key={`code-${cIdx}`} className="my-3 rounded-xl overflow-hidden border border-slate-700/80 bg-slate-900 shadow-sm">
          {lang && (
            <div className="px-3 py-1 bg-slate-800 text-[11px] font-mono text-slate-400 uppercase tracking-wider border-b border-slate-700">
              {lang}
            </div>
          )}
          <pre className="p-3.5 text-xs sm:text-sm font-mono text-slate-100 overflow-x-auto leading-relaxed whitespace-pre">
            <code>{code}</code>
          </pre>
        </div>
      );
    }

    // 2. Split by $$ block math
    const blocks = chunk.split(/(\$\$[\s\S]*?\$\$)/g);

    return blocks.map((block, bIdx) => {
      if (block.startsWith('$$') && block.endsWith('$$')) {
        const math = block.slice(2, -2).trim();
        return (
          <div key={`block-${cIdx}-${bIdx}`} className="overflow-x-auto max-w-full my-2.5 py-1 text-center scrollbar-thin">
            <BlockMath math={math} errorColor="#ef4444" />
          </div>
        );
      }

      // 3. Split remaining text by $ inline math
      const inlines = block.split(/(\$[^\$]+\$)/g);
      return inlines.map((inline, iIdx) => {
        if (inline.startsWith('$') && inline.endsWith('$')) {
          const math = inline.slice(1, -1).trim();
          return (
            <span key={`inline-${cIdx}-${bIdx}-${iIdx}`} className="inline-block max-w-full overflow-x-auto align-middle px-0.5">
              <InlineMath math={math} errorColor="#ef4444" />
            </span>
          );
        }

        // Render line breaks and text
        return <span key={`text-${cIdx}-${bIdx}-${iIdx}`}>{inline}</span>;
      });
    });
  });
};
