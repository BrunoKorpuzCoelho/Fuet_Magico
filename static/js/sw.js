const CACHE_NAME = 'fuet-magico-v1';

// Static assets to pre-cache (app shell)
const PRECACHE_ASSETS = [
    '/static/css/global.css',
    '/static/js/main.js',
    '/static/website/favicon/favicon.svg',
    '/static/website/favicon/web-app-manifest-192x192.png',
    '/static/website/favicon/web-app-manifest-512x512.png',
    '/static/website/favicon/apple-touch-icon.png',
];

// Install: pre-cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(PRECACHE_ASSETS);
        })
    );
    self.skipWaiting();
});

// Activate: remove old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys
                    .filter((key) => key !== CACHE_NAME)
                    .map((key) => caches.delete(key))
            );
        })
    );
    self.clients.claim();
});

// Fetch strategy:
// - Navigation (HTML): network-first → fallback to cache
// - Static assets (CSS/JS/images): cache-first → fallback to network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Only handle same-origin requests
    if (url.origin !== location.origin) return;

    // Skip non-GET requests
    if (request.method !== 'GET') return;

    // Skip Django admin, API, and media endpoints
    if (url.pathname.startsWith('/admin/') ||
        url.pathname.startsWith('/api/') ||
        url.pathname.startsWith('/media/')) {
        return;
    }

    if (request.mode === 'navigate') {
        // Navigation: network-first
        event.respondWith(
            fetch(request)
                .then((response) => {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
                    return response;
                })
                .catch(() => caches.match(request))
        );
    } else if (url.pathname.startsWith('/static/')) {
        // Static assets: cache-first
        event.respondWith(
            caches.match(request).then((cached) => {
                if (cached) return cached;
                return fetch(request).then((response) => {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
                    return response;
                });
            })
        );
    }
});
