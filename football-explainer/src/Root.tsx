/**
 * Registers the two compositions you can render:
 *   - TacticsReel      1080 x 1920 (Instagram Reels / TikTok / Shorts)
 *   - TacticsReelFeed  1080 x 1350 (Instagram feed, 4:5)
 * Both use the SAME component; only the size differs.
 * The duration comes from scene.ts so you only edit the length in one place.
 */
import { Composition } from "remotion";
import { TacticsReel } from "./TacticsReel";
import { scene } from "./data/scene";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="TacticsReel"
        component={TacticsReel}
        durationInFrames={900}
        fps={30}
        width={1080}
        height={1920}
        calculateMetadata={() => ({
          durationInFrames: Math.round(scene.durationInSeconds * 30),
        })}
      />
      <Composition
        id="TacticsReelFeed"
        component={TacticsReel}
        durationInFrames={900}
        fps={30}
        width={1080}
        height={1350}
        calculateMetadata={() => ({
          durationInFrames: Math.round(scene.durationInSeconds * 30),
        })}
      />
    </>
  );
};
