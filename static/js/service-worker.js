const CACHE_NAME = 'umukozi-v2';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/images/icon.png',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
  'https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css'
];

// Install event - cache resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event - Network first for pages, Cache first for statics
self.addEventListener('fetch', event => {
  // Always fetch non-GET requests from network
  if (event.request.method !== 'GET') {
    return;
  }

  const url = new URL(event.request.url);

  // Static assets use Cache First
  if (url.pathname.startsWith('/static/') || url.hostname.includes('fonts') || url.hostname.includes('unpkg')) {
    event.respondWith(
      caches.match(event.request).then(response => {
        if (response) return response;
        return fetch(event.request).then(networkResponse => {
          if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') return networkResponse;
          const cacheCopy = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, cacheCopy));
          return networkResponse;
        });
      })
    );
  } else {
    // Pages / Dynamic Data use Network First
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Update cache with fresh version
          const cacheCopy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, cacheCopy));
          return response;
        })
        .catch(() => {
          return caches.match(event.request);
        })
    );
  }
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
