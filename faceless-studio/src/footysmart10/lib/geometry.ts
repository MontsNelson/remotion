/**
 * Small maths helpers for curved arrows (quadratic Bézier curves).
 * A curve has a start, a control point that "pulls" the curve, and an end.
 */
type Point = { x: number; y: number };

/** Point on the curve at `p` (0 = start, 1 = end). */
export const bezierPoint = (
  start: Point,
  control: Point,
  end: Point,
  p: number,
): Point => {
  const q = 1 - p;
  return {
    x: q * q * start.x + 2 * q * p * control.x + p * p * end.x,
    y: q * q * start.y + 2 * q * p * control.y + p * p * end.y,
  };
};

/** Direction of travel at `p`, in degrees. Used to rotate the arrowhead. */
export const bezierAngle = (
  start: Point,
  control: Point,
  end: Point,
  p: number,
) => {
  const q = 1 - p;
  const dx = 2 * q * (control.x - start.x) + 2 * p * (end.x - control.x);
  const dy = 2 * q * (control.y - start.y) + 2 * p * (end.y - control.y);
  return (Math.atan2(dy, dx) * 180) / Math.PI;
};

/** Turns 2 or 3 pixel points into an SVG path string. */
export const toPath = (points: Point[]) => {
  if (points.length === 3) {
    const [a, c, b] = points;
    return `M ${a.x} ${a.y} Q ${c.x} ${c.y} ${b.x} ${b.y}`;
  }
  const [a, b] = points;
  return `M ${a.x} ${a.y} L ${b.x} ${b.y}`;
};
