'use strict';
let marker, h4, id;

const map = L.map('map', {tap: false});
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([53, 24], 5);

const apiUrl = 'http://127.0.0.1:5000/';

document.querySelector('#player-form').
    addEventListener('submit', function(evt) {
      evt.preventDefault();
      document.querySelector('#player-modal').classList.add('hide');
      togglePopup();
    });

async function newGame(evt) {
  document.querySelector('#budjetti').innerText = '0';
  document.querySelector('#vuorot').innerText = '0';
  document.querySelector('#raha').innerText = '0';
  document.querySelector('#kilometrit').innerText = '0';

  evt.preventDefault();
  alkuperainenmarker();
  const nimi = document.querySelector('#player-input').value;
  let newGameUrl = `${apiUrl}newgame?name=${nimi}`;
  const respons = await fetch(newGameUrl);
  const jso = await respons.json();

  document.querySelector('#player-name').innerText = jso.name;
  document.querySelector('#budjetti').innerText = jso.budget;

  id = jso.id;
  return jso;
}

const nappi3 = document.querySelector('#player-form');
nappi3.addEventListener('submit', newGame);

function togglePopup() {
  document.getElementById('popup-1').classList.toggle('active');
}

function alkuperainenmarker() {
  marker = L.marker([51.505299, 0.055278]).addTo(map);
  h4 = document.createElement('h4');
  h4.innerText = 'London City Airport';
  marker.bindPopup(h4);
  marker.openPopup();
}

async function sade(evt) {
  const url = `${apiUrl}kilometria?id=${id}&km=`;
  evt.preventDefault();
  document.querySelector('#kilometritSade').classList.add('hide');

  const maara = document.querySelector('#tasta').value;
  let sadeUrl = url + maara;

  const response = await fetch(sadeUrl);
  const json = await response.json();
  const markers = [];

  for (let i = 0; i < json.vaihtoehdot.length; i++) {
    const kord1 = json.vaihtoehdot[i]['latitude_deg'];
    const kord2 = json.vaihtoehdot[i]['longitude_deg'];
    const icao = json.vaihtoehdot[i]['ident'];
    const price = json.vaihtoehdot[i]['price'];

    const flyhere = L.marker([kord1, kord2]).addTo(map);
    const suggested = L.divIcon({className: 'suggested-icon'});
    flyhere.setIcon(suggested);
    markers.push(flyhere);

    let popupContent = document.createElement('div');
    h4 = document.createElement('h4');
    h4.innerText = json.vaihtoehdot[i]['name'];
    popupContent.append(h4);
    const p = document.createElement('p');
    p.innerHTML = `Etäisyys: ${json.vaihtoehdot[i]['distance']} km`;
    popupContent.append(p);

    const ma = document.createElement('p');
    ma.innerHTML = `Maa: ${json.vaihtoehdot[i]['country']} `;
    popupContent.append(ma);

    const sa = document.createElement('p');
    sa.innerHTML = `Sääennuste: ${json.vaihtoehdot[i]['weather_description']} `;
    popupContent.append(sa);

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
    nappi.innerText = 'Lennä';
    popupContent.append(nappi);
    flyhere.bindPopup(popupContent);

    nappi.addEventListener('click', async function() {
      document.querySelector('#tasta').value = '';
      marker.remove(map);

      async function flyto() {
        const flyToUrl = `${apiUrl}flyto?id=${id}&dest=${icao}&price=${price}`;
        const respons = await fetch(flyToUrl);
        const jso = await respons.json();
        const flyHere = jso.location;
        if (jso.gameover) {
          togglePopup3();
          return;
        }

        if (flyHere === 'EGLC') {
          togglePopup2();
        }

        document.querySelector('#budjetti').innerText = jso.budget;
        document.querySelector('#vuorot').innerText = jso.times;
        document.querySelector('#raha').innerText = jso.consumed;
        document.querySelector('#kilometrit').innerText = jso.distance;
      }

      await flyto();

      for (let markkeri of markers) {
        markkeri.remove(map);
      }

      marker = L.marker([kord1, kord2]).addTo(map);
      h4 = document.createElement('h4');
      h4.innerText = json.vaihtoehdot[i]['name'];
      marker.bindPopup(h4);
      marker.openPopup();
      //laittaa syötelaatikon takaisin
      document.querySelector('#kilometritSade').classList.remove('hide');
    });
  }
}

const nappi2 = document.querySelector('#paina');
nappi2.addEventListener('click', sade);

function togglePopup2() {
  document.getElementById('leaderboard').classList.toggle('active');
  const vikanappi1 = document.getElementById('new-game-button');
  vikanappi1.addEventListener('click', function() {
    document.querySelector('#player-input').value = '';
    marker.remove(map);
    document.querySelector('#leaderboard').classList.add('hide');
    document.querySelector('#player-modal').classList.remove('hide');
  });
}

function togglePopup3() {
  document.getElementById('gameover').classList.toggle('active');
  const vikanappi = document.getElementById('new-game-button2');
  vikanappi.addEventListener('click', function() {
    document.querySelector('#player-input').value = '';
    marker.remove(map);
    document.querySelector('#gameover').classList.add('hide');
    document.querySelector('#player-modal').classList.remove('hide');
  });
}