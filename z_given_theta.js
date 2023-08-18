function calculateThetaFromZ(){

    fetch("http://localhost:5500/given_z_find_theta", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
        mass1: masses['Particle 1'],
        mass2: masses['Particle 2'],
        mass3: masses['Particle 3'],
        mass4: masses['Particle 4'],
        v_3: v3,
        T_1: document.querySelector("#T_1").value,  
        z: document.querySelector("#z").value,
        B_value: document.querySelector("#B_value").value
        }),

    })
    .then((response) => response.json())
    .then((res) => {
        console.log(res);
        theta_cm = res;
        document.querySelector("#OptimalThetaContainer").style.display = 'block';
        document.querySelector("#OPtimalTheta").innerHTML = theta_cm;
    });

}