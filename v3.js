function calculateV3() {
  fetch("http://localhost:5500/calculate_v3", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      mass1: masses['Particle 1'],
      mass2: masses['Particle 2'],
      mass3: masses['Particle 3'],
      mass4: masses['Particle 4'],
      E_x: document.querySelector("#E_x").value,
      T_1: document.querySelector("#T_1").value,
    }),
  })
    .then((response) => response.json())
    .then((res) => {
      console.log(res);
      v3 = res;
      document.querySelector(".v3Container").style.display = 'block';
      document.querySelector("#v3").innerHTML = v3;
    });
}
