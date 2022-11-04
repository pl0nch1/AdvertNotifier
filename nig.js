import fetch from 'node-fetch';
fetch("http://localhost:5000").then((data)=> {data.text().then(console.log)})