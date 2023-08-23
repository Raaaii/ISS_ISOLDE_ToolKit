function optimal_theta_lab() {
    fetch("http://localhost:5500/find_optimal_theta", {
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
            B_value: document.querySelector("#B_value").value,
            ro_measured1: document.querySelector("#ro_measured1").value,
            ro_measured2: document.querySelector("#ro_measured2").value,
            z_meas: document.querySelector("#z_meas").value,
        }),
    })
    .then((response) => response.json())
    .then((res) => {
        console.log(res);
        const optimal_thetas = res.join(', '); // Convert the array to a comma-separated string
        document.querySelector("#OptimalThetaContainer").style.display = 'block';
        document.querySelector("#OPtimalTheta").textContent = optimal_thetas;
    });
}
