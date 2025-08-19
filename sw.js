// 🛡️ Service Worker для Православного портала (Упрощенная версия)
// Версия: 1.0.0

const CACHE_NAME = 'pravoslavie-portal-v1';

// 📦 Установка Service Worker
self.addEventListener('install', event => {
  console.log('🚀 Service Worker: Installing...');
  event.waitUntil(self.skipWaiting());
});

// 🔄 Активация Service Worker
self.addEventListener('activate', event => {
  console.log('🔄 Service Worker: Activating...');
  event.waitUntil(self.clients.claim());
});

// 🔔 Push-уведомления
self.addEventListener('push', event => {
  console.log('🔔 Push notification received');
  
  const options = {
    body: 'У нас есть что-то новое для вас!',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Посмотреть'
      },
      {
        action: 'close',
        title: 'Закрыть'
      }
    ]
  };
  
  if (event.data) {
    const data = event.data.json();
    options.body = data.body || options.body;
    options.data.url = data.url || '/';
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
  
  const urlToOpen = event.notification.data?.url || '/';
  
  event.waitUntil(
    clients.matchAll({type: 'window'}).then(clientList => {
      for (const client of clientList) {
        if (client.url.includes(self.location.origin) && 'focus' in client) {
          return client.focus().then(() => client.navigate(urlToOpen));
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(urlToOpen);
      }
    })
  );
});

console.log('🛡️ Service Worker loaded successfully!');
