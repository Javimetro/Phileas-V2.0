'use strict';

//kartta
const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);

const apiUrl = 'http://127.0.0.1:5000/';

//pelaajan nimi
document.querySelector('#player-form').
    addEventListener('submit', function(evt) {
      evt.preventDefault();
      const nimi = document.querySelector('#player-input').value;
      document.querySelector('#player-modal').classList.add('hide');
      togglePopup();
      //gameSetup(`${apiUrl}newgame?player=${playerName}&loc=${startLoc}`);
    });

//Nappi (tarina&ohjeet)
function togglePopup() {
  document.getElementById('popup-1').classList.toggle('active');
  //document.getElementById("map").classList.add('hide');
}

//pelaajan sijainti
const marker = L.marker([51.505299, 0.055278]).addTo(map);
marker.bindPopup(`Tämänhetkinen sijaintisi (lentokentän nimi)`);
marker.openPopup();



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



const url = 'http://127.0.0.1:5000/kilometria?id=1&km=';

async function sade(evt) {
  evt.preventDefault();

  const maara = document.querySelector('#tasta').value;
  //console.log(maara);
  let sadeUrl = url + maara;
  //console.log(sadeUrl);

  const response = await fetch(sadeUrl);
  const json = await response.json();
  //console.log(json);
  const sade = json.km_lkm;
  const vaihtoehdo = json.vaihtoehdot;
  //console.log(vaihtoehdo);
  for (let i = 0; i <= 9; i++) {
    const kord1 = json.vaihtoehdot[i]['latitude_deg'];
    const kord2 = json.vaihtoehdot[i]['longitude_deg'];
    //console.log(kord1);
    //console.log(kord2);

    //ehdotetut lentokentät
    const flyhere = L.marker([kord1, kord2]).addTo(map);
    const suggested = L.divIcon({className: 'suggested-icon'});
    flyhere.setIcon(suggested);

    const popupContent = document.createElement('div');
    const h4 = document.createElement('h4');
    h4.innerText = '(lentokentän nimi)';
    popupContent.append(h4);
    const nappi = document.createElement('button');
    //nappi.classList.add('button');
    nappi.innerText = 'Lenni';
    popupContent.append(nappi);
    flyhere.bindPopup(popupContent);
  }

  const elementti = document.querySelector('#tahan');
  elementti.innerText = sade;
}

const nappi2 = document.querySelector('#paina');
nappi2.addEventListener('click', sade);
