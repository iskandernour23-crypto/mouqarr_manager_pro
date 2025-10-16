/* eslint-disable no-restricted-globals */
import { precacheAndRoute } from "workbox-precaching";
import { registerRoute } from "workbox-routing";
import { StaleWhileRevalidate } from "workbox-strategies";
import { BackgroundSyncPlugin } from "workbox-background-sync";

precacheAndRoute(self.__WB_MANIFEST || []);

const bgSyncPlugin = new BackgroundSyncPlugin("api-queue", {
  maxRetentionTime: 24 * 60
});

registerRoute(
  ({ url }) => url.pathname.startsWith("/api"),
  new StaleWhileRevalidate({ fetchOptions: { credentials: "include" }, plugins: [bgSyncPlugin] }),
  "GET"
);

registerRoute(
  ({ request }) => ["image", "font"].includes(request.destination),
  new StaleWhileRevalidate()
);
