import { generateSW } from "workbox-build";

const buildSW = async () => {
  await generateSW({
    swDest: "dist/service-worker.js",
    globDirectory: "dist",
    globPatterns: ["**/*.{js,css,html,png,svg,json}"]
  });
};

buildSW();
