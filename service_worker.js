if ("serviceWorker" in navigator) {

  navigator.serviceWorker.register("service_worker.js").then(function(registration) {
    console.log("Service worker registered successfully!");
  }).catch(function(error) {
    console.log("Service worker failed to be registered with error: ", error);
  });
}

self.addEventListener("install", function(event) {
  event.waitUntil(
    caches.open("our-cache").then(function(cache) {
      cache.addAll(["/"]);
    })
  );
});

self.addEventListener("fetch", function(event) {
  //from now on we will be working in here
  event.respondWith(
    fetch(event.request).then(function(response) {
      return response;
    }).catch(function(error) {
      //We don't really need the error parameter, but if you want to use it you know how to now.
      return caches.match(event.request).then(function(cacheRes) {
        return cacheRes;
      })
    })
  );
});
