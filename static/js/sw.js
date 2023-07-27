self.addEventListener('install', (e) => {
    e.waitUntil(
      caches.open('ChatApp').then((cache) => cache.addAll([
        '/messenger/mainPage',
      ])),
    );
  });
  
  self.addEventListener('fetch', (e) => {
    console.log(e.request.url);
    e.respondWith(
      caches.match(e.request).then((response) => response || fetch(e.request)),
    );
  });