function getBathValue() {
  const bath = document.getElementById("uiBath").value;
  return parseInt(bath);
}

function getBHKValue() {
  const bhk = document.getElementById("uiBHK").value;
  return parseInt(bhk);
}

function onClickedEstimatePrice() {
  const sqft = document.getElementById("uiSqft").value;
  const bhk = getBHKValue();
  const bath = getBathValue();
  const location = document.getElementById("uiLocations").value;
  const estPrice = document.getElementById("uiEstimatedPrice");

  const url = "http://127.0.0.1:5000/predict_home_price";

  const formData = new FormData();
  formData.append("total_sqft", sqft);
  formData.append("location", location);
  formData.append("bhk", bhk);
  formData.append("bath", bath);

  fetch(url, {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    estPrice.innerHTML = "Estimated Price: ₹ " + data.estimated_price + " Lakh";
  })
  .catch(error => {
    console.error("Error:", error);
    estPrice.innerHTML = "Error fetching price.";
  });
}

function onPageLoad() {
  const url = "http://127.0.0.1:5000/get_location_names";
  fetch(url)
  .then(response => response.json())
  .then(data => {
    const locations = data.locations;
    const uiLocations = document.getElementById("uiLocations");
    uiLocations.innerHTML = "";

    locations.forEach(loc => {
      const opt = new Option(loc);
      uiLocations.add(opt);
    });
  });
}

window.onload = onPageLoad;
