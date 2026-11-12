/**
 * Fonts. @remotion/google-fonts downloads the font files once and makes sure
 * the render waits until they are ready, so text never pops in late.
 */
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";

/** Headline font (ALL CAPS, condensed). Anton only ships weight 400. */
export const anton = loadAnton("normal", {
  weights: ["400"],
  subsets: ["latin"],
}).fontFamily;

/** Small text font. */
export const inter = loadInter("normal", {
  weights: ["400", "600", "800"],
  subsets: ["latin"],
}).fontFamily;
