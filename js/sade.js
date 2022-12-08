'use strict';
const url = 'http://127.0.0.1:5000/kilometria?id=1&km=';

async function sade(evt) {
  evt.preventDefault();

  const maara = document.querySelector('#tasta').value;
  console.log(maara);
  let sadeUrl = url + maara;
  console.log(sadeUrl);

  const response = await fetch(sadeUrl);
  const json = await response.json();
  console.log(json);
  const sade = json.km_lkm;
  const vaihtoehdo = json.vaihtoehdot;
  console.log(vaihtoehdo);
  for (let i = 0; i <= 9; i++) {
    const kord1 = json.vaihtoehdot[i][2];
    const kord2 = json.vaihtoehdot[i][3];
    console.log(kord1)
    console.log(kord2)

  }

  const elementti = document.querySelector('#tahan');
  elementti.innerText = sade;
}

const nappi2 = document.querySelector('#paina');
nappi2.addEventListener('click', sade);
