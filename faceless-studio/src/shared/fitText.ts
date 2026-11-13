/**
 * Picks a font size so a single line of Anton text fits the given width.
 * Anton capitals average about half a font-size wide each.
 */
export const fitAntonSize = (text: string, maxSize: number, width: number) =>
  Math.min(maxSize, width / (Math.max(1, text.length) * 0.5));
