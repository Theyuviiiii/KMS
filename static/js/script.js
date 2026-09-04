(function(){
 const form=document.getElementById('recruitmentForm'); if(!form)return;
 const steps=[...document.querySelectorAll('.step')], bar=document.getElementById('progressBar'), label=document.getElementById('stepLabel'), review=document.getElementById('reviewCard'), success=document.getElementById('successScreen');
 let current=1;
 const fields=['name','roll_no','branch','year','email','phone','domain','reason','experience','portfolio'];
 function show(n){current=n;steps.forEach(s=>s.classList.toggle('active',+s.dataset.step===n));if(bar)bar.style.width=(n/4*100)+'%';if(label)label.textContent='STEP 0'+n;window.scrollTo({top:0,behavior:'smooth'});}
 function validStep(n){const el=steps[n-1];for(const x of el.querySelectorAll('[required]')){if(!x.checkValidity()){x.reportValidity();return false}}return true}
 document.querySelectorAll('.next-btn').forEach(b=>b.addEventListener('click',()=>{if(validStep(current)){if(current===3)buildReview();show(Math.min(4,current+1))}}));
 document.querySelectorAll('.back-btn').forEach(b=>b.addEventListener('click',()=>show(Math.max(1,current-1))));
 function esc(v){return String(v||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
 function buildReview(){const d=new FormData(form);review.innerHTML=fields.map(k=>`<div><b>${esc(k.replace('_',' '))}:</b> ${esc(d.get(k))}</div>`).join('')}
 form.addEventListener('submit',async e=>{e.preventDefault();if(!validStep(4))return;const consent=document.getElementById('consent');if(consent&&!consent.checked){consent.reportValidity();return}const r=await fetch('/apply',{method:'POST',body:new FormData(form)});const data=await r.json().catch(()=>({ok:false,message:'Submission failed.'}));if(!r.ok||!data.ok){alert(data.message||'Submission failed. Please try again.');return}form.style.display='none';success.classList.add('show')});
 const t=document.getElementById('themeToggle');if(t){if(localStorage.getItem('kms-theme')==='dark')document.body.classList.add('dark');const u=()=>t.textContent=document.body.classList.contains('dark')?'☀ Light':'☾ Dark';u();t.onclick=()=>{document.body.classList.toggle('dark');localStorage.setItem('kms-theme',document.body.classList.contains('dark')?'dark':'light');u()}}
})();
