'use strict';

//kartta
const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);


//pelaajan nimi
document.querySelector('#player-form').addEventListener('submit', function(evt){
  evt.preventDefault();
  const nimi = document.querySelector('#player-input').value;
  document.querySelector('#player-modal').classList.add('hide');
  //gameSetup();
})

//Nappi (tarina&ohjeet)
function togglePopup() {
  document.getElementById("popup-1").classList.toggle("active");
  //document.getElementById("map").classList.add('hide');
}


//pelaajan sijainti
const marker = L.marker([51.505299, 0.055278]).addTo(map);
marker.bindPopup(`Tämänhetkinen sijaintisi (lentokentän nimi)`);
marker.openPopup();

//ehdotetut lentokentät
const flyhere = L.marker([52.461101532, 9.685079574580001]).addTo(map);
const suggested = L.divIcon({className: 'suggested-icon'});
flyhere.setIcon(suggested);

const popupContent = document.createElement('div');
const h4 = document.createElement('h4');
h4.innerText = '(lentokentän nimi)';
popupContent.append(h4);
const nappi = document.createElement('button');
//nappi.classList.add('button');
nappi.innerText = 'Lennä';
popupContent.append(nappi);
flyhere.bindPopup(popupContent);

//lentäminen lentokentältä toiselle
nappi.addEventListener('click', function() {
})




//PELIN TAULUJEN TIETOJEN MUOKKAUS
/*
function updateStatus(status) {
  document.querySelector('#player-name').innerHTML = `Player: ${status.name}`;
  document.querySelector('#budjetti').innerHTML = `Player: ${status.name}`;
  document.querySelector('#matka').innerHTML = `Player: ${status.name}`;
}
*/

//PIILOTTAA KOHTEEN
/*
document.querySelector('.goal').addEventListener('click', function (evt) {
  evt.currentTarget.classList.add('hide');
});
*/