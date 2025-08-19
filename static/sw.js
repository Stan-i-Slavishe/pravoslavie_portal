// 🛡️ Service Worker для Православного портала
// Версия: 1.0.0

const CACHE_NAME = 'pravoslavie-portal-v1';
const OFFLINE_URL = '/offline/';
const CACHE_VERSION = '1.0.0';

// ⭐ Критически важные ресурсы для кеширования
const CRITICAL_CACHE = [
  '/',
  '/fairy-tales/',
  '/stories/',
  '/books/',
  '/shop/',
  '/offline/',
  '/static/css/bootstrap.min.css',
  '/static/css/all.min.css',
  '/static/js/bootstrap.bundle.min.js',
  '/static/manifest.json'
];

// 🧚 Терапевтические сказки для офлайн доступа
const FAIRY_TALES_CACHE = [
  '/fairy-tales/category/straxi/',
  '/fairy-tales/category/samoocenka/',
  '/fairy-tales/category/otnosheniya/',
  '/fairy-tales/category/povedenie/'
];

// 📚 Страницы книг для офлайн чтения
const BOOKS_CACHE = [
  '/books/category/detskie/',
  '/books/category/duhovnye/',
  '/books/category/semeynye/'
];

// 🎬 Аудио и видео ресурсы (кешируем метаданные)
const MEDIA_CACHE = [
  '/stories/playlists/',
  '/audio/'
];

// 🚀 Установка Service Worker
self.addEventListener('install', event => {
  console.log('🚀 Service Worker: Installing...');
  
  event.waitUntil(
    Promise.all([
      // Кешируем критические ресурсы
      caches.open(CACHE_NAME + '-critical').then(cache => {
        console.log('📦 Caching critical resources...');
        return cache.addAll(CRITICAL_CACHE.map(url => new Request(url, {
          cache: 'reload'
        })));
      }),
      
      // Кешируем сказки для детей
      caches.open(CACHE_NAME + '-fairy-tales').then(cache => {
        console.log('🧚 Caching fairy tales...');
        return cache.addAll(FAIRY_TALES_CACHE);
      }),
      
      // Кешируем книги
      caches.open(CACHE_NAME + '-books').then(cache => {
        console.log('📚 Caching books...');
        return cache.addAll(BOOKS_CACHE);
      })
    ]).then(() => {
      console.log('✅ Service Worker: Installation complete!');
      // Принудительно активируем новый SW
      return self.skipWaiting();
    }).catch(error => {
      console.error('❌ Service Worker: Installation failed:', error);
    })
  );
});

// 🔄 Активация Service Worker
self.addEventListener('activate', event => {
  console.log('🔄 Service Worker: Activating...');
  
  event.waitUntil(
    // Очищаем старые кеши
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName.indexOf(CACHE_NAME) === 0 && cacheName !== CACHE_NAME + '-critical' && 
              cacheName !== CACHE_NAME + '-fairy-tales' && cacheName !== CACHE_NAME + '-books') {
            console.log('🗑️ Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ Service Worker: Activation complete!');
      // Берем контроль над всеми клиентами
      return self.clients.claim();
    })
  );
});

// 🌐 Обработка сетевых запросов
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  
  // Игнорируем запросы к другим доменам и не-GET запросы
  if (url.origin !== location.origin || request.method !== 'GET') {
    return;
  }
  
  // 🎯 Стратегии кеширования для разных типов контента
  
  // 1. 🧚 Терапевтические сказки - Cache First (важно для офлайн)
  if (url.pathname.startsWith('/fairy-tales/')) {
    event.respondWith(cacheFirst(request, CACHE_NAME + '-fairy-tales'));
    return;
  }
  
  // 2. 📚 Книги - Cache First
  if (url.pathname.startsWith('/books/')) {
    event.respondWith(cacheFirst(request, CACHE_NAME + '-books'));
    return;
  }
  
  // 3. 🎬 Видео и аудио метаданные - Network First
  if (url.pathname.startsWith('/stories/') || url.pathname.startsWith('/audio/')) {
    event.respondWith(networkFirst(request, CACHE_NAME + '-critical'));
    return;
  }
  
  // 4. 🛒 Магазин и корзина - только Network (динамические данные)
  if (url.pathname.startsWith('/shop/') || url.pathname.startsWith('/cart/')) {
    event.respondWith(networkOnly(request));
    return;
  }
  
  // 5. 🏠 Главная и критические страницы - Stale While Revalidate
  if (CRITICAL_CACHE.includes(url.pathname)) {
    event.respondWith(staleWhileRevalidate(request, CACHE_NAME + '-critical'));
    return;
  }
  
  // 6. 📷 Статические файлы - Cache First с длинным TTL
  if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/media/')) {
    event.respondWith(cacheFirst(request, CACHE_NAME + '-static', 86400000)); // 24 часа
    return;
  }
  
  // 7. По умолчанию - Network First с фоллбэком на офлайн страницу
  event.respondWith(networkFirstWithOffline(request));
});

// 📦 Cache First стратегия
async function cacheFirst(request, cacheName, maxAge = 3600000) {
  try {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      const cachedDate = new Date(cachedResponse.headers.get('date'));
      const now = new Date();
      
      // Проверяем возраст кеша
      if (now - cachedDate < maxAge) {
        console.log('📦 Cache hit:', request.url);
        return cachedResponse;
      }
    }
    
    // Пытаемся получить с сервера
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      console.log('🌐 Network hit, updating cache:', request.url);
      await cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('📦 Cache fallback:', request.url);
    const cache = await caches.open(cacheName);
    return await cache.match(request) || await cache.match(OFFLINE_URL);
  }
}

// 🌐 Network First стратегия
async function networkFirst(request, cacheName) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      await cache.put(request, networkResponse.clone());
      console.log('🌐 Network first, cached:', request.url);
    }
    
    return networkResponse;
  } catch (error) {
    console.log('📦 Network failed, cache fallback:', request.url);
    const cache = await caches.open(cacheName);
    return await cache.match(request) || await cache.match(OFFLINE_URL);
  }
}

// ⚡ Stale While Revalidate стратегия
async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cachedResponse = await cache.match(request);
  
  // Асинхронно обновляем кеш
  const networkResponsePromise = fetch(request).then(networkResponse => {
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
      console.log('⚡ Background update:', request.url);
    }
    return networkResponse;
  }).catch(() => {
    console.log('⚡ Background update failed:', request.url);
  });
  
  // Возвращаем кешированную версию или ждем сеть
  return cachedResponse || networkResponsePromise || cache.match(OFFLINE_URL);
}

// 🌐 Network Only стратегия
async function networkOnly(request) {
  try {
    return await fetch(request);
  } catch (error) {
    // Для динамических страниц показываем офлайн страницу
    return await caches.match(OFFLINE_URL);
  }
}

// 🌐 Network First с офлайн фоллбэком
async function networkFirstWithOffline(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME + '-critical');
      await cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    const cache = await caches.open(CACHE_NAME + '-critical');
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Показываем специальную офлайн страницу
    return await cache.match(OFFLINE_URL);
  }
}

// 🔔 Background Sync для плейлистов и избранного
self.addEventListener('sync', event => {
  console.log('🔄 Background sync triggered:', event.tag);
  
  if (event.tag === 'playlist-sync') {
    event.waitUntil(syncPlaylists());
  }
  
  if (event.tag === 'favorites-sync') {
    event.waitUntil(syncFavorites());
  }
  
  if (event.tag === 'cart-sync') {
    event.waitUntil(syncCart());
  }
});

// 🎵 Синхронизация плейлистов
async function syncPlaylists() {
  try {
    console.log('🎵 Syncing playlists...');
    
    // Получаем несинхронизированные плейлисты из IndexedDB
    const pendingPlaylists = await getPendingPlaylists();
    
    for (const playlist of pendingPlaylists) {
      try {
        await fetch('/stories/playlists/sync/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': await getCSRFToken()
          },
          body: JSON.stringify(playlist)
        });
        
        // Помечаем как синхронизированный
        await markPlaylistSynced(playlist.id);
        console.log('✅ Playlist synced:', playlist.name);
      } catch (error) {
        console.error('❌ Failed to sync playlist:', playlist.name, error);
      }
    }
  } catch (error) {
    console.error('❌ Playlist sync failed:', error);
  }
}

// ⭐ Синхронизация избранного
async function syncFavorites() {
  try {
    console.log('⭐ Syncing favorites...');
    
    const pendingFavorites = await getPendingFavorites();
    
    for (const favorite of pendingFavorites) {
      try {
        await fetch('/favorites/sync/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': await getCSRFToken()
          },
          body: JSON.stringify(favorite)
        });
        
        await markFavoriteSynced(favorite.id);
        console.log('✅ Favorite synced:', favorite.item_id);
      } catch (error) {
        console.error('❌ Failed to sync favorite:', favorite.item_id, error);
      }
    }
  } catch (error) {
    console.error('❌ Favorites sync failed:', error);
  }
}

// 🛒 Синхронизация корзины
async function syncCart() {
  try {
    console.log('🛒 Syncing cart...');
    
    const pendingCartItems = await getPendingCartItems();
    
    for (const item of pendingCartItems) {
      try {
        await fetch('/shop/cart/sync/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': await getCSRFToken()
          },
          body: JSON.stringify(item)
        });
        
        await markCartItemSynced(item.id);
        console.log('✅ Cart item synced:', item.product_id);
      } catch (error) {
        console.error('❌ Failed to sync cart item:', item.product_id, error);
      }
    }
  } catch (error) {
    console.error('❌ Cart sync failed:', error);
  }
}

// 🔔 Push-уведомления
self.addEventListener('push', event => {
  console.log('🔔 Push notification received');
  
  const options = {
    body: 'У нас есть что-то новое для вас!',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Посмотреть',
        icon: '/static/icons/checkmark.png'
      },
      {
        action: 'close',
        title: 'Закрыть',
        icon: '/static/icons/xmark.png'
      }
    ],
    requireInteraction: false,
    silent: false
  };
  
  if (event.data) {
    const data = event.data.json();
    options.body = data.body || options.body;
    options.data.url = data.url || '/';
    
    // Специальные настройки для разных типов уведомлений
    if (data.type === 'bedtime_story') {
      options.body = '🌙 Время сказки на ночь! Выберите добрую историю для малыша';
      options.data.url = '/fairy-tales/';
      options.requireInteraction = true;
    } else if (data.type === 'orthodox_calendar') {
      options.body = `⛪ ${data.body}`;
      options.data.url = data.url || '/stories/';
    } else if (data.type === 'new_content') {
      options.body = `📚 ${data.body}`;
      options.data.url = data.url || '/';
    }
  }
  
  event.waitUntil(
    self.registration.showNotification('Добрые истории', options)
  );
});

// 👆 Обработка кликов по уведомлениям
self.addEventListener('notificationclick', event => {
  console.log('👆 Notification clicked:', event.action);
  
  event.notification.close();
  
  if (event.action === 'close') {
    return;
  }
  
  // Открываем соответствующую страницу
  const urlToOpen = event.notification.data.url || '/';
  
  event.waitUntil(
    clients.matchAll({
      type: 'window',
      includeUncontrolled: true
    }).then(clientList => {
      // Проверяем, есть ли уже открытая вкладка с нашим сайтом
      for (const client of clientList) {
        if (client.url.includes(self.location.origin) && 'focus' in client) {
          return client.focus().then(() => {
            return client.navigate(urlToOpen);
          });
        }
      }
      
      // Открываем новую вкладку
      if (clients.openWindow) {
        return clients.openWindow(urlToOpen);
      }
    })
  );
});

// 🔧 Вспомогательные функции для работы с IndexedDB
async function getPendingPlaylists() {
  // Здесь будет код для работы с IndexedDB
  return [];
}

async function markPlaylistSynced(id) {
  // Помечаем плейлист как синхронизированный
}

async function getPendingFavorites() {
  return [];
}

async function markFavoriteSynced(id) {
  // Помечаем избранное как синхронизированное
}

async function getPendingCartItems() {
  return [];
}

async function markCartItemSynced(id) {
  // Помечаем элемент корзины как синхронизированный
}

async function getCSRFToken() {
  // Получаем CSRF токен для Django
  try {
    const response = await fetch('/get-csrf-token/');
    const data = await response.json();
    return data.csrfToken;
  } catch (error) {
    return '';
  }
}

console.log('🛡️ Service Worker loaded successfully!');
