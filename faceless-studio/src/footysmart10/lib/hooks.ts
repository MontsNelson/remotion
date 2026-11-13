/** Two tiny hooks every component uses. */
import { useCurrentFrame, useVideoConfig } from "remotion";
import { getLayout } from "./pitch";

/** The pitch layout for the current video size (Reel or feed). */
export const useLayout = () => {
  const { width, height } = useVideoConfig();
  return getLayout(width, height);
};

/** The current time in seconds (frame / fps). */
export const useSeconds = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return frame / fps;
};
