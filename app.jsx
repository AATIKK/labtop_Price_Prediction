import React, { useState } from "react";

export default function App(){
  const [form, setForm] = useState({
    brand: "", cpu: "", ram_gb: 8, storage_type: "SSD", storage_gb: 256, gpu: "", screen_size_in: 15.6, os: "", age_years: 1, condition: "used"
  });
  const [result, setResult] = useState(null);

  const handle = (e) => {
    const { name, value } = e.target;
    setForm({...form, [name]: value});
  };

  const submit = async (e) => {
    e.preventDefault();
    const res = await fetch("/api/predict", { // proxy to backend in dev or use full URL
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(form)
    });
    const data = await res.json();
    setResult(data.predicted_price_usd);
  };

  return (
    <div style={{padding:20}}>
      <h2>Laptop Price Predictor</h2>
      <form onSubmit={submit}>
        <input name="brand" placeholder="brand" onChange={handle}/>
        <input name="cpu" placeholder="cpu" onChange={handle}/>
        <input name="ram_gb" type="number" onChange={handle} defaultValue={8}/>
        <input name="storage_type" placeholder="SSD/HDD" onChange={handle} defaultValue="SSD"/>
        <input name="storage_gb" type="number" onChange={handle} defaultValue={256}/>
        <button type="submit">Predict</button>
      </form>
      {result && <div>Predicted price: ${result.toFixed(2)}</div>}
    </div>
  );
}
