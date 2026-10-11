/* Digital Towers Future state maps and tables. Hypothetical and illustrative. MapLibre GL + Protomaps (OpenStreetMap data, ODbL). */
(function(){
"use strict";
var TC={"1":"#ffb347","2":"#4fd1c5","3":"#f472b6","4":"#9aa2b1","X":"#556070"};
var TL={"1":"Tier 1: Full remote tower service","2":"Tier 2: Part-time remote tower","3":"Tier 3: Remote advisory (AFIS-like)","4":"Tier 4: Surface awareness only","X":"Large hub: augment or keep as is"};
var TD={"1":"Air traffic control from a remote centre for extended hours or around the clock.","2":"Remote air traffic control in busy periods, advisory service the rest of the day.","3":"Remote flight information and advisories. Not air traffic control.","4":"Cameras and surveillance feeds for awareness. No separation service.","X":"Too large for the simple remote model."};
var CL={R:"Remote or digital tower already listed",T:"Staffed tower today",S:"No tower, scheduled passenger service",G:"No tower, traffic above threshold",P:"No tower, infrastructure proxy",I:"No tower, isolated airfield"};
var ST={operational:"#5ed39a",trial:"#7aa7ff",planned:"#c4b5fd",unverified:"#9aa2b1",decommissioned:"#ff6b6b",cancelled:"#ff6b6b"};
function el(t,a,h){var e=document.createElement(t);if(a)for(var k in a){if(k==="class")e.className=a[k];else e.setAttribute(k,a[k]);}if(h!=null)e.innerHTML=h;return e;}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
function num(x){return x==null?"n/a":Math.round(x).toLocaleString("en-US");}
function baseStyle(origin){
  var fl=basemaps.namedFlavor("dark");
  fl.background="#0b0d12";fl.earth="#151922";fl.water="#0a0c11";fl.park_a="#151b22";fl.park_b="#151b22";fl.wood_a="#151b22";fl.wood_b="#151b22";
  fl.scrub_a="#151b22";fl.scrub_b="#151b22";fl.glacier="#1a1f29";fl.sand="#151922";fl.beach="#151922";fl.aerodrome="#1b2230";fl.runway="#3a4458";
  fl.boundaries="#3a4256";fl.city_label="#c9cfdb";fl.state_label="#6b7180";fl.country_label="#9aa2b1";fl.ocean_label="#4a5263";fl.subplace_label="#8a92a2";
  var layers=basemaps.layers("protomaps",fl,{lang:"en"}).filter(function(l){return !(l.layout&&l.layout["icon-image"]);});
  return {version:8,glyphs:origin+"/fonts/{fontstack}/{range}.pbf",sources:{protomaps:{type:"vector",url:"pmtiles://"+origin+"/tiles/world.pmtiles",attribution:'<a href="https://openstreetmap.org/copyright">&copy; OpenStreetMap contributors</a> | <a href="https://protomaps.com">Protomaps</a>'}},layers:layers};
}
function initProtocol(){if(window.__pm)return;var p=new pmtiles.Protocol();maplibregl.addProtocol("pmtiles",p.tile);window.__pm=1;}
function getj(u){return fetch(u).then(function(r){return r.json();});}
var tierColor=["match",["get","tier"],"1",TC["1"],"2",TC["2"],"3",TC["3"],"4",TC["4"],"X",TC.X,"#9aa2b1"];
var isMobile=function(){return window.innerWidth<820;};

/* ---------------- country page ---------------- */
window.DTFutureCountry=function(cc,name){
  initProtocol();
  getj("/data/future/c_"+cc+".json").then(function(D){
    var A=D.airports,C=D.centers;
    // legend
    var lg=document.getElementById("flegend");
    if(lg)lg.innerHTML=["1","2","3","4"].map(function(k){return '<span><i style="background:'+TC[k]+'"></i>'+TL[k]+'</span>';}).join("")+'<span><i class="ring" style="border-color:#5ed39a"></i>Already remote or digital</span><span><i class="ring" style="border-color:#fff"></i>Hypothetical centre</span>';
    // map
    var feats=[],lines=[];
    A.forEach(function(x,i){x.i=i;feats.push({type:"Feature",geometry:{type:"Point",coordinates:[x.lo,x.la]},properties:{i:i,id:x.id,tier:x.tier||"",cls:x.cls,rem:x.rem||""}});
      if(x.c>=0&&C[x.c])lines.push({type:"Feature",geometry:{type:"LineString",coordinates:[[x.lo,x.la],[C[x.c].lo,C[x.c].la]]},properties:{}});});
    var cf=C.map(function(c,i){return {type:"Feature",geometry:{type:"Point",coordinates:[c.lo,c.la]},properties:{i:i,n:c.site}};});
    var map=new maplibregl.Map({container:"fmap",style:baseStyle(location.origin),center:[0,20],zoom:2,minZoom:0.8,maxZoom:12,attributionControl:{compact:true},cooperativeGestures:true,dragRotate:false});
    map.addControl(new maplibregl.NavigationControl({showCompass:false}),"top-right");
    var b=new maplibregl.LngLatBounds(),has=false;
    A.forEach(function(x){if(x.cls!=="N"){b.extend([x.lo,x.la]);has=true;}});C.forEach(function(c){b.extend([c.lo,c.la]);has=true;});
    map.on("load",function(){
      map.addSource("ap",{type:"geojson",data:{type:"FeatureCollection",features:feats}});
      map.addSource("ln",{type:"geojson",data:{type:"FeatureCollection",features:lines}});
      map.addSource("ct",{type:"geojson",data:{type:"FeatureCollection",features:cf}});
      map.addLayer({id:"ln",type:"line",source:"ln",paint:{"line-color":"#ffffff","line-opacity":0.14,"line-width":1}});
      map.addLayer({id:"gap",type:"circle",source:"ap",filter:["all",["in",["get","cls"],["literal",["S","G","P","I"]]]],paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,3,6,6,10,8],"circle-color":tierColor,"circle-opacity":.92,"circle-stroke-color":"#0b0d12","circle-stroke-width":1}});
      map.addLayer({id:"tow",type:"circle",source:"ap",filter:["==",["get","cls"],"T"],paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,3,6,6,10,8],"circle-color":"rgba(0,0,0,0)","circle-stroke-color":tierColor,"circle-stroke-width":2}});
      map.addLayer({id:"rem",type:"circle",source:"ap",filter:["==",["get","cls"],"R"],paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,4,6,7,10,9],"circle-color":"rgba(0,0,0,0)","circle-stroke-color":"#5ed39a","circle-stroke-width":2.5}});
      map.addLayer({id:"ctr",type:"circle",source:"ct",paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,5,6,9,10,11],"circle-color":"#ffb347","circle-stroke-color":"#ffffff","circle-stroke-width":2.5}});
      if(has)map.fitBounds(b,{padding:isMobile()?30:60,maxZoom:7,duration:0});
      var pop=null;
      function show(lng,lat,html){if(pop)pop.remove();pop=new maplibregl.Popup({closeButton:true,maxWidth:"280px"}).setLngLat([lng,lat]).setHTML(html).addTo(map);}
      ["gap","tow","rem"].forEach(function(l){map.on("click",l,function(e){var x=A[e.features[0].properties.i];show(x.lo,x.la,apHTML(x,C));});
        map.on("mouseenter",l,function(){map.getCanvas().style.cursor="pointer";});map.on("mouseleave",l,function(){map.getCanvas().style.cursor="";});});
      map.on("click","ctr",function(e){var c=C[e.features[0].properties.i];show(c.lo,c.la,'<b>'+esc(c.site)+'</b><br>'+esc(c.kind)+'<br>'+c.n+' airports, farthest '+c.maxd+' km<br><i>Hypothetical</i>');});
      window.__fmap=map;
    });
    // table
    var rows=document.getElementById("frows"),q=document.getElementById("fq"),ts=document.getElementById("ftier"),cs=document.getElementById("fcls"),cnt=document.getElementById("fcount"),more=document.getElementById("fmore");
    var shown=50,list=[];
    function filt(){
      var s=q.value.trim().toLowerCase(),t=ts.value,c=cs.value;
      list=A.filter(function(x){
        if(x.cls==="N")return false;
        if(t&&x.tier!==t)return false;
        if(c==="gap"){if(["S","G","P"].indexOf(x.cls)<0||["1","2","3"].indexOf(x.tier)<0)return false;}
        else if(c&&x.cls!==c)return false;
        if(s&&(x.n+" "+x.id+" "+x.m).toLowerCase().indexOf(s)<0)return false;
        return true;});
    }
    function render(){
      filt();cnt.textContent=list.length+" airports";
      rows.innerHTML=list.slice(0,shown).map(function(x){
        var ct=x.c>=0&&C[x.c]?esc(C[x.c].site)+'<div class="xs faint">'+x.dc+' km</div>':'<span class="faint">none</span>';
        var tr=x.tier?'<span class="dot" style="background:'+TC[x.tier]+'"></span>'+(x.tier==="X"?"Hub":"Tier "+x.tier):'<span class="faint">n/a</span>';
        return '<tr data-i="'+x.i+'" class="frow"><td><b>'+esc(x.n)+'</b><div class="xs faint">'+esc(x.id)+(x.m?" · "+esc(x.m):"")+(x.af?" · air-ground service listed":"")+'</div></td><td>'+tr+'</td><td class="small">'+esc(CL[x.cls])+'<div class="xs faint">'+esc(x.rs)+'</div></td><td>'+(x.pax==null?'<span class="faint">n/a</span>':num(x.pax))+'</td><td>'+(x.ops==null?'<span class="faint">n/a</span>':num(x.ops))+'</td><td class="small">'+ct+'</td></tr>';}).join("")||'<tr><td colspan="6" class="mute">No airports match.</td></tr>';
      more.innerHTML=list.length>shown?'<button class="btn" type="button" id="fmorebtn">Show 100 more</button>':"";
      var mb=document.getElementById("fmorebtn");if(mb)mb.onclick=function(){shown+=100;render();};
    }
    [q,ts,cs].forEach(function(e){e.addEventListener("input",function(){shown=50;render();});});
    rows.addEventListener("click",function(e){var tr=e.target.closest("tr[data-i]");if(!tr||!window.__fmap)return;var x=A[+tr.getAttribute("data-i")];window.__fmap.flyTo({center:[x.lo,x.la],zoom:Math.max(window.__fmap.getZoom(),7),duration:700});document.getElementById("fmap").scrollIntoView({block:"center",behavior:"smooth"});});
    render();
  });
};
function apHTML(x,C){
  var t=x.tier?'<br><b style="color:'+TC[x.tier]+'">'+esc(TL[x.tier])+'</b>':"";
  var c=x.c>=0&&C[x.c]?'<br>Suggested centre: '+esc(C[x.c].site)+' ('+x.dc+' km)':"";
  return '<b>'+esc(x.n)+'</b><br>'+esc(x.id)+(x.m?" · "+esc(x.m):"")+t+'<br>'+esc(CL[x.cls])+(x.rem?" ("+esc(x.rem)+")":"")+'<br>Passengers '+num(x.pax)+' · movements '+num(x.ops)+c+'<br><i>Hypothetical. Illustrative.</i>';
}

/* ---------------- world view ---------------- */
window.DTFutureWorld=function(SCOPE,NAMES){
  initProtocol();
  Promise.all([getj("/data/future/world_points.json"),getj("/data/future/world_centers.json"),getj("/data/towers.json")]).then(function(R){
    var P=R[0].rows,CT=R[1].rows,TW=R[2].towers;
    var pf=P.map(function(r,i){return {type:"Feature",geometry:{type:"Point",coordinates:[r[0],r[1]]},properties:{i:i,tier:r[2],cls:r[3],cc:r[4]}};});
    var cf=CT.map(function(r,i){return {type:"Feature",geometry:{type:"Point",coordinates:[r[0],r[1]]},properties:{i:i,cc:r[2]}};});
    var by={};TW.forEach(function(t){by[t.id]=t;});
    var tf=TW.map(function(t,i){return {type:"Feature",geometry:{type:"Point",coordinates:[t.lon,t.lat]},properties:{i:i,id:t.id,status:t.status,kind:t.kind}};});
    var tl=[];TW.forEach(function(t){if(t.controlled_from&&by[t.controlled_from]){var h=by[t.controlled_from];tl.push({type:"Feature",geometry:{type:"LineString",coordinates:[[t.lon,t.lat],[h.lon,h.lat]]},properties:{}});}});
    var map=new maplibregl.Map({container:"fwmap",style:baseStyle(location.origin),center:[10,35],zoom:isMobile()?0.9:1.6,minZoom:0.6,maxZoom:12,attributionControl:{compact:true},dragRotate:false,pitchWithRotate:false});
    map.touchZoomRotate.disableRotation();map.addControl(new maplibregl.NavigationControl({showCompass:false}),"top-right");
    var st={mode:"future",tiers:{"1":1,"2":1,"3":1,"4":1,"X":0},gap:1,tow:1,ctr:1,cc:""};
    var detail=document.getElementById("fdetail"),cnt=document.getElementById("fcount2");
    var tiersEl=document.getElementById("ftiers");
    ["1","2","3","4","X"].forEach(function(k){var b=el("button",{class:"chip",type:"button","aria-pressed":st.tiers[k]?"true":"false"},'<i style="display:inline-block;width:9px;height:9px;border-radius:50%;background:'+TC[k]+';margin-right:7px"></i>'+(k==="X"?"Hubs":"Tier "+k));
      b.addEventListener("click",function(){st.tiers[k]=st.tiers[k]?0:1;b.setAttribute("aria-pressed",st.tiers[k]?"true":"false");apply();});tiersEl.appendChild(b);});
    function tog(id,key){var b=document.getElementById(id);b.addEventListener("click",function(){st[key]=st[key]?0:1;b.setAttribute("aria-pressed",st[key]?"true":"false");apply();});}
    tog("fgap","gap");tog("ftow","tow");tog("fctr","ctr");
    var sel=document.getElementById("fcountry");
    var ccs={};P.forEach(function(r){ccs[r[4]]=1;});Object.keys(ccs).sort(function(a,b){return (NAMES[a]||a).localeCompare(NAMES[b]||b);}).forEach(function(c){sel.appendChild(el("option",{value:c},esc(NAMES[c]||c)));});
    var lg=document.getElementById("flegend2");
    function legend(){lg.innerHTML=st.mode==="future"?["1","2","3","4"].map(function(k){return '<span style="--c:'+TC[k]+'"><i></i>'+TL[k].split(":")[0]+'</span>';}).join("")+'<span class="faint">Hollow ring: towered candidate</span><span class="faint">White ring: hypothetical centre</span>':
      Object.keys(ST).filter(function(k){return k!=="cancelled";}).map(function(k){return '<span style="--c:'+ST[k]+'"><i></i>'+k.charAt(0).toUpperCase()+k.slice(1)+'</span>';}).join("")+'<span class="faint">White ring: remote tower centre</span>';}
    function apply(){
      if(!map.getLayer("fp"))return;
      var ts=Object.keys(st.tiers).filter(function(k){return st.tiers[k];});
      var cl=[];if(st.gap)cl.push("S","G","P","I");
      var f1=["all",["in",["get","tier"],["literal",ts]],["in",["get","cls"],["literal",cl]]];
      var f2=["all",["in",["get","tier"],["literal",ts]],["==",["get","cls"],"T"]];
      if(st.cc){f1.push(["==",["get","cc"],st.cc]);f2.push(["==",["get","cc"],st.cc]);}
      map.setFilter("fp",f1);map.setFilter("ft",st.tow?f2:["==",["get","cc"],"__none"]);
      var f3=st.cc?["==",["get","cc"],st.cc]:null;map.setFilter("fc",st.ctr?f3:["==",["get","cc"],"__none"]);
      var fut=st.mode==="future";
      ["fp","ft","fc","fch"].forEach(function(l){map.setLayoutProperty(l,"visibility",fut?"visible":"none");});
      ["tp","th","tl","tr"].forEach(function(l){map.setLayoutProperty(l,"visibility",fut?"none":"visible");});
      document.getElementById("ffut").hidden=!fut;document.getElementById("fday").hidden=fut;
      document.getElementById("vtoday").setAttribute("aria-pressed",fut?"false":"true");document.getElementById("vfuture").setAttribute("aria-pressed",fut?"true":"false");
      legend();
      if(fut){var n1=0,n2=0;P.forEach(function(r){if(st.cc&&r[4]!==st.cc)return;if(!st.tiers[r[2]])return;if(r[3]==="T"){if(st.tow)n2++;}else if(st.gap)n1++;});
        cnt.textContent=n1.toLocaleString()+" airports without a tower and "+n2.toLocaleString()+" towered candidates shown.";}
      else cnt.textContent=TW.length+" remote and digital sites from the dataset.";
    }
    map.on("load",function(){
      map.addSource("pts",{type:"geojson",data:{type:"FeatureCollection",features:pf}});
      map.addSource("cts",{type:"geojson",data:{type:"FeatureCollection",features:cf}});
      map.addSource("tws",{type:"geojson",data:{type:"FeatureCollection",features:tf}});
      map.addSource("tln",{type:"geojson",data:{type:"FeatureCollection",features:tl}});
      var rad=["interpolate",["linear"],["zoom"],1,2.2,4,4,8,7,11,9];
      map.addLayer({id:"fp",type:"circle",source:"pts",paint:{"circle-radius":rad,"circle-color":tierColor,"circle-opacity":.85,"circle-stroke-color":"#0b0d12","circle-stroke-width":.6}});
      map.addLayer({id:"ft",type:"circle",source:"pts",paint:{"circle-radius":rad,"circle-color":"rgba(0,0,0,0)","circle-stroke-color":tierColor,"circle-stroke-width":1.4}});
      map.addLayer({id:"fch",type:"circle",source:"cts",paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,6,6,10],"circle-color":"rgba(255,179,71,.18)","circle-blur":.6}});
      map.addLayer({id:"fc",type:"circle",source:"cts",paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,3.2,6,6,10,8],"circle-color":"#ffb347","circle-stroke-color":"#ffffff","circle-stroke-width":2}});
      map.addLayer({id:"tl",type:"line",source:"tln",paint:{"line-color":"#7aa7ff","line-opacity":.3,"line-width":1}});
      var sc=["match",["get","status"],"operational",ST.operational,"trial",ST.trial,"planned",ST.planned,"unverified",ST.unverified,"decommissioned",ST.decommissioned,"cancelled",ST.cancelled,"#9aa2b1"];
      map.addLayer({id:"th",type:"circle",source:"tws",paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,6,6,12],"circle-color":sc,"circle-opacity":.16,"circle-blur":.6}});
      map.addLayer({id:"tp",type:"circle",source:"tws",paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,3.2,6,6.5,10,8],"circle-color":sc,"circle-stroke-color":["case",["==",["get","kind"],"rtc"],"#ffffff","#0b0d12"],"circle-stroke-width":["case",["==",["get","kind"],"rtc"],2,1]}});
      map.addLayer({id:"tr",type:"circle",source:"tws",filter:["==",["get","id"],"__none"],paint:{"circle-radius":11,"circle-color":"rgba(0,0,0,0)","circle-stroke-color":"#fff","circle-stroke-width":2}});
      var qs=new URLSearchParams(location.search);if(qs.get("view")==="today")st.mode="today";
      if(qs.get("country")&&ccs[qs.get("country").toUpperCase()]){st.cc=qs.get("country").toUpperCase();sel.value=st.cc;}
      apply();if(st.cc)fitCC();
      ["fp","ft"].forEach(function(l){map.on("click",l,function(e){var r=P[e.features[0].properties.i];showP(r);});
        map.on("mouseenter",l,function(){map.getCanvas().style.cursor="pointer";});map.on("mouseleave",l,function(){map.getCanvas().style.cursor="";});});
      map.on("click","fc",function(e){var r=CT[e.features[0].properties.i];var s=SCOPE[r[2]];
        detail.innerHTML='<h2 style="font-size:18px;margin:0 0 6px">'+esc(r[5])+'</h2><p class="small mute">Hypothetical centre · '+esc(NAMES[r[2]]||r[2])+'</p><p class="small">Serves '+r[3]+' airports in this scenario.</p>'+(s?'<p><a class="btn" href="/future/countries/'+s.s+'/">Country page</a></p>':'')+'<p class="xs faint"><b>Hypothetical. Illustrative.</b></p>';});
      map.on("click","tp",function(e){var t=TW[e.features[0].properties.i];map.setFilter("tr",["==",["get","id"],t.id]);
        detail.innerHTML='<h2 style="font-size:18px;margin:0 0 6px">'+esc(t.name)+'</h2><p class="small"><span class="pill st-'+t.status+'">'+t.status+'</span> '+esc(t.country)+'</p><p class="small mute">'+esc(t.ansp||"")+'</p><p><a class="btn primary" href="/towers/'+esc(t.id)+'/">Open tower page</a></p>';});
      ["tp"].forEach(function(l){map.on("mouseenter",l,function(){map.getCanvas().style.cursor="pointer";});map.on("mouseleave",l,function(){map.getCanvas().style.cursor="";});});
    });
    function showP(r){var s=SCOPE[r[4]];
      detail.innerHTML='<h2 style="font-size:18px;margin:0 0 6px">'+esc(r[5])+'</h2><p class="small mute">'+esc(r[6])+' · '+esc(NAMES[r[4]]||r[4])+'</p><p class="small"><b style="color:'+TC[r[2]]+'">'+esc(TL[r[2]])+'</b><br>'+esc(TD[r[2]])+'</p><p class="small mute">'+esc(CL[r[3]])+'. '+(r[7]?'Tier from a traffic figure.':'Tier from runway, size class and scheduled-service flag only.')+'</p>'+(s?'<p><a class="btn" href="/future/countries/'+s.s+'/">'+esc(s.n)+' page</a></p>':'<p class="xs faint">No country page yet for this country; counts only.</p>')+'<p class="xs faint"><b>Hypothetical. Illustrative.</b></p>';}
    function fitCC(){var b=new maplibregl.LngLatBounds(),n=0;P.forEach(function(r){if(r[4]===st.cc){b.extend([r[0],r[1]]);n++;}});if(n)map.fitBounds(b,{padding:isMobile()?{top:40,bottom:window.innerHeight*.5,left:20,right:20}:{top:40,bottom:40,left:400,right:40},maxZoom:6,duration:800});}
    sel.addEventListener("change",function(){st.cc=sel.value;apply();if(st.cc)fitCC();else map.flyTo({center:[10,35],zoom:isMobile()?0.9:1.6});});
    document.getElementById("vtoday").addEventListener("click",function(){st.mode="today";apply();});
    document.getElementById("vfuture").addEventListener("click",function(){st.mode="future";apply();});
    window.__fwmap=map;
  });
};
})();
