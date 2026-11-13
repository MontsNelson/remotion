/**
 * Registers every video the studio can render, grouped by channel.
 * Each channel has a Reel version (1080x1920) and a feed version
 * (1080x1350). Lengths come from each channel's data file.
 */
import { Composition, Folder } from "remotion";
import { TacticsReel } from "./footysmart10/TacticsReel";
import { scene } from "./footysmart10/data/scene";
import { GtaNewsClip } from "./gta/GtaNewsClip";
import { countdown } from "./gta/data/countdown";
import { RecastReel } from "./multiverse/RecastReel";
import { episodeSeconds } from "./multiverse/data/episode";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Folder name="FootySmart10">
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
      </Folder>
      <Folder name="GTA6">
        <Composition
          id="GtaCountdown"
          component={GtaNewsClip}
          durationInFrames={690}
          fps={30}
          width={1080}
          height={1920}
          calculateMetadata={() => ({
            durationInFrames: Math.round(countdown.durationInSeconds * 30),
          })}
        />
        <Composition
          id="GtaCountdownFeed"
          component={GtaNewsClip}
          durationInFrames={690}
          fps={30}
          width={1080}
          height={1350}
          calculateMetadata={() => ({
            durationInFrames: Math.round(countdown.durationInSeconds * 30),
          })}
        />
      </Folder>
      <Folder name="Multiverse">
        <Composition
          id="RecastReel"
          component={RecastReel}
          durationInFrames={570}
          fps={30}
          width={1080}
          height={1920}
          calculateMetadata={() => ({
            durationInFrames: Math.round(episodeSeconds() * 30),
          })}
        />
        <Composition
          id="RecastReelFeed"
          component={RecastReel}
          durationInFrames={570}
          fps={30}
          width={1080}
          height={1350}
          calculateMetadata={() => ({
            durationInFrames: Math.round(episodeSeconds() * 30),
          })}
        />
      </Folder>
    </>
  );
};
