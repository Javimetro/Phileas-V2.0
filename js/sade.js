'use strict'
const url = '#http://127.0.0.1:5000/kilometria?id=1&km=';

async function sade (evt) {
  const maara = document.querySelector('#tasta').value;
  evt.preventDefault();
  console.log(maara);
  let sadeUrl = url + maara;
  console.log(sadeUrl);




  const response = await fetch(sadeUrl);
  const json = await response.json();
  console.log(json)
  const sade = json.kl_lkm;
  console.log(sade);
  const elementti = document.querySelector('#tahan');
  elementti.innerText = sade;
}


const nappi2 = document.querySelector('#paina');
nappi2.addEventListener('click',sade);