function optimal_theta_lab(){
    fetch("http://localhost:5500/optimal_theta_lab", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            mass3: masses['Particle 3'],
            B: document.querySelector("#B").value,
            ro_measured: document.querySelector("#ro_meas").value,
            v_3: v3,
            initial_theta_lab: document.querySelector("#initial_theta_lab").value,  
            q: document.querySelector("#q").value
        }),
    })
    .then((response) => response.json())
    .then((res) => {
      console.log(res);
      theta_lab = res;
      document.querySelector("#OptimalThetaContainer").style.display = 'block';
      document.querySelector("#OPtimalTheta").innerHTML = theta_lab;
    });
}
