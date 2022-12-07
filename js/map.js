'use strict';

const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);


//pelaajan sijainti
const marker = L.marker([51.505299, 0.055278]).addTo(map);
marker.bindPopup(`AAA`);
marker.openPopup();

//ehdotetut lentokentät
const flyhere = L.marker([53, -3]).addTo(map);
flyhere.bindPopup(`ehdotus`);
const suggested = L.divIcon({ className: 'suggested-icon' });
flyhere.setIcon(suggested);