/**
 * The tactic currently being drawn. The reel can be fed a tactic as JSON
 * (props), so every component reads it through useScene() instead of
 * importing scene.ts directly. Without props it falls back to scene.ts.
 */
import { createContext, useContext } from "react";
import { scene as defaultScene, type SceneData } from "./scene";

export const SceneContext = createContext<SceneData>(defaultScene);

export const useScene = () => useContext(SceneContext);
