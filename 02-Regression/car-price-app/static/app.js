const form=document.getElementById('carForm');
const submitBtn=document.getElementById('submitBtn');
const btnText=submitBtn.querySelector('.btn-text');
const btnSpinner=submitBtn.querySelector('.btn-spinner');
const placeholder=document.getElementById('placeholder');
const resultContent=document.getElementById('resultContent');
const resultError=document.getElementById('resultError');
const priceMain=document.getElementById('priceMain');
const priceLow=document.getElementById('priceLow');
const priceHigh=document.getElementById('priceHigh');
const errorMsg=document.getElementById('errorMsg');
const resetBtn=document.getElementById('resetBtn');
function formatPrice(v){return'$'+Math.round(v).toLocaleString('en-US')}
function showLoading(on){btnText.style.display=on?'none':'inline';btnSpinner.style.display=on?'inline':'none';submitBtn.disabled=on}
function showResult(data){placeholder.style.display='none';resultError.style.display='none';resultContent.style.display='block';priceMain.textContent=formatPrice(data.predicted_price);priceLow.textContent=formatPrice(data.price_low);priceHigh.textContent=formatPrice(data.price_high)}
function showError(msg){placeholder.style.display='none';resultContent.style.display='none';resultError.style.display='block';errorMsg.textContent=msg||'Something went wrong.'}
form.addEventListener('submit',async(e)=>{e.preventDefault();showLoading(true);const formData=new FormData(form);const payload={};formData.forEach((v,k)=>{payload[k]=v});try{const r=await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const data=await r.json();if(data.status==='success'){showResult(data)}else{showError(data.message)}}catch(err){showError('Could not reach the server.')}finally{showLoading(false)}});
resetBtn.addEventListener('click',()=>{resultContent.style.display='none';placeholder.style.display='block';form.reset()});
