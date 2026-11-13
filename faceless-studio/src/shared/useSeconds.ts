import { useCurrentFrame, useVideoConfig } from "remotion";

/** The current time in seconds (frame / fps). */
export const useSeconds = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return frame / fps;
};
