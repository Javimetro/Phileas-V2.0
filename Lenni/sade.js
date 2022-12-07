'use strict'

async function sade (evt) {
  let url = 'http://127.0.0.1:3000/kilometria/';
  const maara = document.querySelector('#tasta').value;
  evt.preventDefault();
  console.log(maara);
  url = url + maara;
  console.log(url);




  const response = await fetch(url);
  const json = await response.json();
  const sade = json.kl_lkm;
  console.log(sade);
  const elementti = document.querySelector('#tahan');
  elementti.innerText = sade;
}






const nappi = document.querySelector('#paina');
nappi.addEventListener('click',sade);