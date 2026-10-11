/* Digital Towers connections graph and timeline filters. No libraries. */
(function(){
"use strict";
function el(t,a,h){var e=document.createElement(t);if(a)for(var k in a){if(k==="class")e.className=a[k];else e.setAttribute(k,a[k]);}if(h!=null)e.innerHTML=h;return e;}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
var LABEL={operational:"Operational",trial:"Trial",planned:"Planned",unverified:"Unverified",decommissioned:"Decommissioned",cancelled:"Cancelled"};
var REMOTE={remote_tower:1,rtc:1,digital_tower:1,remote_afis:1};
var P=new URLSearchParams(location.search);

/* ---------------- timeline filters ---------------- */
var tc=document.getElementById("tlchips");
if(tc){
  var rows=[].slice.call(document.querySelectorAll("li.tl")),sel={},ctry=document.getElementById("tlc"),cnt=document.getElementById("tlcount"),want=P.get("tower")||"";
  if(P.get("type")){sel[P.get("type")]=true;}
  function paintT(){
    [].forEach.call(tc.querySelectorAll("[data-type]"),function(b){b.setAttribute("aria-pressed",sel[b.getAttribute("data-type")]?"true":"false");});
    var any=Object.keys(sel).some(function(k){return sel[k];}),c=ctry.value,n=0;
    rows.forEach(function(r){
      var ok=(!any||sel[r.getAttribute("data-type")])&&(!c||r.getAttribute("data-c")===c)&&(!want||r.getAttribute("data-id")===want);
      r.hidden=!ok;if(ok)n++;});
    [].forEach.call(document.querySelectorAll("ul.tlist"),function(u){var vis=[].some.call(u.children,function(x){return !x.hidden;});u.hidden=!vis;if(u.previousElementSibling)u.previousElementSibling.hidden=!vis;});
    cnt.textContent=n+" of "+rows.length+(want?" for one tower":"");
  }
  tc.addEventListener("click",function(e){var b=e.target.closest("[data-type]");if(!b)return;var k=b.getAttribute("data-type");sel[k]=!sel[k];paintT();});
  ctry.addEventListener("change",paintT);paintT();
}

/* ---------------- connections graph ---------------- */
var cg=document.getElementById("cg");
if(!cg)return;
var TYPE={vendor:"Vendors",provider:"Providers",regulator:"Regulators",program:"Programs"};
var S={a:"vendor",b:"provider",country:"",status:{},remoteOnly:false,selA:null,selB:null},TW=[];
var ca=document.getElementById("ca"),cb=document.getElementById("cb"),cc=document.getElementById("cc"),cstat=document.getElementById("cstat"),ckind=document.getElementById("ckind"),cnt2=document.getElementById("ccount"),det=document.getElementById("cdetail");
Object.keys(LABEL).forEach(function(k){if(k==="cancelled")return;var b=el("button",{class:"chip","aria-pressed":"false","data-s":k,type:"button"},LABEL[k]);b.addEventListener("click",function(){S.status[k]=!S.status[k];b.setAttribute("aria-pressed",S.status[k]?"true":"false");S.selA=S.selB=null;draw();});cstat.appendChild(b);});
function keys(t,type){
  if(type==="vendor")return t.v.map(function(x){return {id:x[0],name:x[1]};});
  if(type==="provider")return t.p?[{id:t.p[0],name:t.p[1]}]:[];
  if(type==="regulator")return t.r?[{id:t.r[0],name:t.r[1]}]:[];
  if(type==="program")return t.g?[{id:t.g[0],name:t.g[1]}]:[];
  return [];}
function okT(t){
  if(S.country&&t.c!==S.country)return false;
  var any=Object.keys(S.status).some(function(k){return S.status[k];});
  if(any&&!(S.status[t.s]||(t.s==="cancelled"&&S.status.decommissioned)))return false;
  if(S.remoteOnly&&!REMOTE[t.k])return false;
  return true;}
function draw(){
  var A={},B={},E={},nT=0;
  TW.forEach(function(t){
    if(!okT(t))return;nT++;
    var ka=keys(t,S.a),kb=keys(t,S.b);
    ka.forEach(function(x){A[x.id]=A[x.id]||{id:x.id,name:x.name,n:0};A[x.id].n++;});
    kb.forEach(function(y){B[y.id]=B[y.id]||{id:y.id,name:y.name,n:0};B[y.id].n++;});
    ka.forEach(function(x){kb.forEach(function(y){var k=x.id+"|"+y.id;E[k]=E[k]||{a:x.id,b:y.id,t:[]};E[k].t.push(t);});});
  });
  var LA=Object.keys(A).map(function(k){return A[k];}).sort(function(p,q){return q.n-p.n||p.name.localeCompare(q.name);});
  var LB=Object.keys(B).map(function(k){return B[k];}).sort(function(p,q){return q.n-p.n||p.name.localeCompare(q.name);});
  var W=Math.max(300,cg.clientWidth||340),narrow=W<560,lw=narrow?Math.floor(W*.36):Math.floor(Math.min(W*.3,260)),rh=narrow?30:32;
  var H=Math.max(LA.length,LB.length)*rh+16,ns="http://www.w3.org/2000/svg";
  cnt2.textContent=nT+" sites match · "+LA.length+" "+TYPE[S.a].toLowerCase()+" · "+LB.length+" "+TYPE[S.b].toLowerCase();
  cg.innerHTML="";
  if(!LA.length||!LB.length){cg.appendChild(el("p",{class:"small mute",style:"padding:18px"},"No sites in the records link these two kinds of party with the current filters."));det.innerHTML='<p class="small mute" style="margin:0">Nothing to list.</p>';return;}
  var svg=document.createElementNS(ns,"svg");svg.setAttribute("viewBox","0 0 "+W+" "+H);svg.setAttribute("width","100%");svg.setAttribute("height",H);svg.setAttribute("aria-hidden","true");
  var yA={},yB={};LA.forEach(function(n,i){yA[n.id]=8+i*rh+rh/2;});LB.forEach(function(n,i){yB[n.id]=8+i*rh+rh/2;});
  var maxE=1;Object.keys(E).forEach(function(k){maxE=Math.max(maxE,E[k].t.length);});
  var gE=document.createElementNS(ns,"g"),gN=document.createElementNS(ns,"g");
  var x1=lw+6,x2=W-lw-6;
  Object.keys(E).forEach(function(k){
    var e=E[k],p=document.createElementNS(ns,"path"),m=(x1+x2)/2;
    p.setAttribute("d","M"+x1+","+yA[e.a]+" C"+m+","+yA[e.a]+" "+m+","+yB[e.b]+" "+x2+","+yB[e.b]);
    p.setAttribute("fill","none");p.setAttribute("stroke","#7aa7ff");p.setAttribute("stroke-linecap","round");
    p.setAttribute("stroke-width",(1.4+Math.sqrt(e.t.length)*2.2).toFixed(1));
    var on=(S.selA===e.a&&S.selB===e.b),dim=(S.selA||S.selB)&&!((!S.selA||S.selA===e.a)&&(!S.selB||S.selB===e.b));
    p.setAttribute("stroke-opacity",on?0.95:(dim?0.07:0.32));p.style.cursor="pointer";
    var t=document.createElementNS(ns,"title");t.textContent=e.t.length+" site"+(e.t.length>1?"s":"");p.appendChild(t);
    p.addEventListener("click",function(){if(S.selA===e.a&&S.selB===e.b){S.selA=S.selB=null;}else{S.selA=e.a;S.selB=e.b;}draw();});
    gE.appendChild(p);});
  function node(n,x,anchor,side){
    var g=document.createElementNS(ns,"g"),y=(side==="a"?yA:yB)[n.id];
    var lim=Math.floor((lw-34)/6.6),lab=n.name.length>lim?n.name.slice(0,lim-1)+"…":n.name;
    var isSel=(side==="a"?S.selA:S.selB)===n.id,dim=(side==="a"?S.selA:S.selB)&&!isSel;
    var r=document.createElementNS(ns,"rect");r.setAttribute("x",side==="a"?0:W-lw);r.setAttribute("y",y-12);r.setAttribute("width",lw);r.setAttribute("height",24);r.setAttribute("rx",12);
    r.setAttribute("fill",isSel?"rgba(91,141,217,.35)":"rgba(255,255,255,.05)");r.setAttribute("stroke",isSel?"#7aa7ff":"rgba(255,255,255,.12)");
    var t=document.createElementNS(ns,"text");t.setAttribute("x",side==="a"?12:W-12);t.setAttribute("y",y+4.5);t.setAttribute("text-anchor",side==="a"?"start":"end");t.setAttribute("font-size","12.5");t.setAttribute("fill","#eef0f4");t.setAttribute("font-family","inherit");t.textContent=lab;
    var c=document.createElementNS(ns,"text");c.setAttribute("x",side==="a"?lw-10:W-lw+10);c.setAttribute("y",y+4.5);c.setAttribute("text-anchor",side==="a"?"end":"start");c.setAttribute("font-size","11");c.setAttribute("fill","#9aa2b1");c.textContent=n.n;
    var tt=document.createElementNS(ns,"title");tt.textContent=n.name+": "+n.n+" sites";g.appendChild(tt);
    g.appendChild(r);g.appendChild(t);g.appendChild(c);g.style.cursor="pointer";if(dim)g.setAttribute("opacity",.4);
    g.setAttribute("tabindex","0");g.setAttribute("role","button");g.setAttribute("aria-label",n.name+", "+n.n+" sites");
    function pick(){if(side==="a")S.selA=(S.selA===n.id?null:n.id);else S.selB=(S.selB===n.id?null:n.id);draw();}
    g.addEventListener("click",pick);g.addEventListener("keydown",function(ev){if(ev.key==="Enter"||ev.key===" "){ev.preventDefault();pick();}});
    return g;}
  LA.forEach(function(n){gN.appendChild(node(n,0,"start","a"));});LB.forEach(function(n){gN.appendChild(node(n,0,"end","b"));});
  svg.appendChild(gE);svg.appendChild(gN);cg.appendChild(svg);
  /* detail list */
  var L=TW.filter(function(t){
    if(!okT(t))return false;
    var ka=keys(t,S.a).map(function(x){return x.id;}),kb=keys(t,S.b).map(function(x){return x.id;});
    if(S.selA&&ka.indexOf(S.selA)<0)return false;if(S.selB&&kb.indexOf(S.selB)<0)return false;
    return !!(S.selA||S.selB);});
  if(!L.length){det.innerHTML='<p class="small mute" style="margin:0">Tap a name or a line above to list the sites it covers.</p>';return;}
  var na=S.selA?(A[S.selA]||{}).name:"",nb=S.selB?(B[S.selB]||{}).name:"";
  det.innerHTML='<h3 style="margin-bottom:10px">'+esc([na,nb].filter(Boolean).join(" and "))+' <span class="faint small">'+L.length+' site'+(L.length>1?"s":"")+'</span></h3><div class="grid g2" style="gap:6px 18px">'+L.map(function(t){return '<a class="mrow" href="/towers/'+esc(t.id)+'/"><span class="pill st-'+t.s+'" style="padding:2px 8px"></span><span><b>'+esc(t.n)+'</b><span class="small mute"> '+esc(t.c)+'</span></span></a>';}).join("")+'</div>';
}
ca.addEventListener("change",function(){S.a=ca.value;if(cb.value===S.a){cb.value=S.a==="provider"?"vendor":"provider";S.b=cb.value;}S.selA=S.selB=null;draw();});
cb.addEventListener("change",function(){S.b=cb.value;if(ca.value===S.b){ca.value=S.b==="vendor"?"provider":"vendor";S.a=ca.value;}S.selA=S.selB=null;draw();});
cc.addEventListener("change",function(){S.country=cc.value;S.selA=S.selB=null;draw();hubFilter();});
ckind.addEventListener("click",function(){S.remoteOnly=!S.remoteOnly;ckind.setAttribute("aria-pressed",S.remoteOnly?"true":"false");S.selA=S.selB=null;draw();});
function hubFilter(){var n=0,tot=0;[].forEach.call(document.querySelectorAll(".hubcard"),function(h){tot++;var ok=!S.country||h.getAttribute("data-c")===S.country;h.hidden=!ok;if(ok)n++;});var hc=document.getElementById("hubcount");if(hc)hc.textContent=n+" of "+tot+" centres shown.";}
var rz;window.addEventListener("resize",function(){clearTimeout(rz);rz=setTimeout(draw,150);});
fetch("/data/graph.json?v="+(window.DT_VER||Date.now())).then(function(r){return r.json();}).then(function(d){
  TW=d.towers;
  if(P.get("a")&&TYPE[P.get("a")]){S.a=P.get("a");ca.value=S.a;}if(P.get("b")&&TYPE[P.get("b")]){S.b=P.get("b");cb.value=S.b;}
  if(P.get("country")){cc.value=P.get("country");S.country=cc.value;}
  var f=P.get("focus");
  if(f){var t=TW.filter(function(x){return x.id===f;})[0];if(t){var ka=keys(t,S.a),kb=keys(t,S.b);S.selA=ka[0]?ka[0].id:null;S.selB=kb[0]?kb[0].id:null;}}
  draw();hubFilter();
  if(f&&(S.selA||S.selB)){var dd=document.getElementById("cdetail");setTimeout(function(){dd.scrollIntoView({block:"nearest"});},200);}
}).catch(function(){cg.innerHTML='<p class="small mute" style="padding:18px">The graph data did not load. The lists below show the same links.</p>';});
})();
