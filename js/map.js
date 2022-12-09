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
    });

async function newGame(evt) {
  evt.preventDefault();
  const nimi = document.querySelector('#player-input').value;
  let newGameUrl = 'http://127.0.0.1:5000/newgame?name=' + nimi;
  console.log(newGameUrl);
  const respons = await fetch(newGameUrl);
  const jso = await respons.json();
  console.log(jso);

  document.querySelector('#player-name').innerText = jso.name;
  document.querySelector('#budjetti').innerText = jso.budget;

  const id = jso.id;
  console.log(id);
  return id;
}

const nappi3 = document.querySelector('#player-form');
nappi3.addEventListener('submit', newGame);

//Nappi (tarina&ohjeet)
function togglePopup() {
  document.getElementById('popup-1').classList.toggle('active');
  //document.getElementById("map").classList.add('hide');
}

//pelaajan sijainti
const marker = L.marker([51.505299, 0.055278]).addTo(map);
marker.bindPopup(`Tämänhetkinen sijaintisi (lentokentän nimi)`);
marker.openPopup();


const url = 'http://127.0.0.1:5000/kilometria?id=1&km=';

async function sade(evt) {
  evt.preventDefault();
  document.querySelector('#kilometritSade').classList.add('hide');

  const maara = document.querySelector('#tasta').value;
  let sadeUrl = url + maara;

  const response = await fetch(sadeUrl);
  const json = await response.json();
  console.log(json);
  const sade = json.km_lkm;
  for (let i = 0; i <= 9; i++) {
    const kord1 = json.vaihtoehdot[i]['latitude_deg'];
    const kord2 = json.vaihtoehdot[i]['longitude_deg'];

    //markerit ehdotetuille lentokentille
    const flyhere = L.marker([kord1, kord2]).addTo(map);
    const suggested = L.divIcon({className: 'suggested-icon'});
    flyhere.setIcon(suggested);
    //markereiden sisällä näkyvä teksti
    const popupContent = document.createElement('div');
    const h4 = document.createElement('h4');
    h4.innerText = json.vaihtoehdot[i]['name'];
    popupContent.append(h4);
    const p = document.createElement('p');
    p.innerHTML = `Etäisyys: ${json.vaihtoehdot[i]['distance']} km`;
    popupContent.append(p);

    const hinta = document.createElement('p');
    hinta.innerHTML = `Hinta: ${json.vaihtoehdot[i]['price']} €`;
    popupContent.append(hinta);
    const ale = document.createElement('p');
    const lati = json.vaihtoehdot[i]['latitude_deg'];
    if (20 <= lati && lati <= 40) {
      ale.innerText = '50% ALE';
    } else if (0 <= lati && lati <= 20) {
      ale.innerText = '70% ALE';
    } else if (60 <= lati && lati <= 80) {
      ale.innerText = '30% kalliimpi hinta';
    } else {
      ale.innerText = 'Normaali hinta';
    }
    popupContent.append(ale);

    const nappi = document.createElement('button');
    //nappi.classList.add('button');
    nappi.innerText = 'Lennä';
    popupContent.append(nappi);
    flyhere.bindPopup(popupContent);
  }

}

const nappi2 = document.querySelector('#paina');
nappi2.addEventListener('click', sade);
