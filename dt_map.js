/* Digital Towers map. MapLibre GL + Protomaps vector tiles (OpenStreetMap data, ODbL), self-hosted. */
(function(){
"use strict";
var COL={operational:"#5ed39a",trial:"#7aa7ff",planned:"#c4b5fd",unverified:"#9aa2b1",decommissioned:"#ff6b6b",cancelled:"#ff6b6b"};
var LABEL={operational:"Operational",trial:"Trial",planned:"Planned",unverified:"Unverified",decommissioned:"Decommissioned",cancelled:"Cancelled"};
function el(t,a,h){var e=document.createElement(t);if(a)for(var k in a){if(k==="class")e.className=a[k];else e.setAttribute(k,a[k]);}if(h!=null)e.innerHTML=h;return e;}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
function host(u){try{return new URL(u).hostname.replace(/^www\./,"");}catch(e){return u;}}

function baseStyle(origin){
  var fl=basemaps.namedFlavor("dark");
  fl.background="#0b0d12";fl.earth="#151922";fl.water="#0a0c11";fl.park_a="#151b22";fl.park_b="#151b22";fl.wood_a="#151b22";fl.wood_b="#151b22";
  fl.scrub_a="#151b22";fl.scrub_b="#151b22";fl.glacier="#1a1f29";fl.sand="#151922";fl.beach="#151922";fl.aerodrome="#1b2230";fl.runway="#3a4458";
  fl.boundaries="#3a4256";fl.city_label="#c9cfdb";fl.state_label="#6b7180";fl.country_label="#9aa2b1";fl.ocean_label="#4a5263";fl.subplace_label="#8a92a2";
  var layers=basemaps.layers("protomaps",fl,{lang:"en"}).filter(function(l){return !(l.layout&&l.layout["icon-image"]);});
  return {version:8,glyphs:origin+"/fonts/{fontstack}/{range}.pbf",
    sources:{protomaps:{type:"vector",url:"pmtiles://"+origin+"/tiles/world.pmtiles",attribution:'<a href="https://openstreetmap.org/copyright">&copy; OpenStreetMap contributors</a> | <a href="https://protomaps.com">Protomaps</a>'}},
    layers:layers};
}
function initProtocol(){
  if(window.__pm)return;var p=new pmtiles.Protocol();maplibregl.addProtocol("pmtiles",p.tile);window.__pm=1;
}
function featuresOf(T){return {type:"FeatureCollection",features:T.map(function(t){return {type:"Feature",id:t.i,geometry:{type:"Point",coordinates:[t.lon,t.lat]},properties:{id:t.id,name:t.name,icao:t.icao||"",status:t.status,kind:t.kind,country:t.country}};})};}
function linesOf(T){var by={};T.forEach(function(t){by[t.id]=t;});var f=[];
  T.forEach(function(t){if(t.controlled_from&&by[t.controlled_from]){var h=by[t.controlled_from];f.push({type:"Feature",geometry:{type:"LineString",coordinates:[[t.lon,t.lat],[h.lon,h.lat]]},properties:{a:t.id,b:h.id,status:t.status}});}});
  return {type:"FeatureCollection",features:f};}

function addLayers(map,T,opts){
  map.addSource("towers",{type:"geojson",data:featuresOf(T)});
  map.addSource("links",{type:"geojson",data:linesOf(T)});
  map.addLayer({id:"links",type:"line",source:"links",paint:{"line-color":"#7aa7ff","line-opacity":opts.allLinks?0.28:0.0,"line-width":1}});
  map.addLayer({id:"links-sel",type:"line",source:"links",filter:["==",["get","a"],"__none"],paint:{"line-color":"#7aa7ff","line-opacity":.9,"line-width":2}});
  var colorExpr=["match",["get","status"],"operational",COL.operational,"trial",COL.trial,"planned",COL.planned,"unverified",COL.unverified,"decommissioned",COL.decommissioned,"cancelled",COL.cancelled,"#9aa2b1"];
  map.addLayer({id:"halo",type:"circle",source:"towers",paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,6,6,12],"circle-color":colorExpr,"circle-opacity":.16,"circle-blur":.6}});
  map.addLayer({id:"pts",type:"circle",source:"towers",paint:{"circle-radius":["interpolate",["linear"],["zoom"],1,3.2,6,6.5,10,8],"circle-color":colorExpr,"circle-stroke-color":["case",["==",["get","kind"],"rtc"],"#ffffff","#0b0d12"],"circle-stroke-width":["case",["==",["get","kind"],"rtc"],2,1]}});
  map.addLayer({id:"lab",type:"symbol",source:"towers",minzoom:4.4,layout:{"text-field":["coalesce",["get","icao"],""],"text-font":["Noto Sans Medium"],"text-size":11,"text-offset":[0,1.15],"text-anchor":"top","text-allow-overlap":false},paint:{"text-color":"#c9cfdb","text-halo-color":"#0b0d12","text-halo-width":1.4}});
  map.addLayer({id:"sel",type:"circle",source:"towers",filter:["==",["get","id"],"__none"],paint:{"circle-radius":11,"circle-color":"rgba(0,0,0,0)","circle-stroke-color":"#ffffff","circle-stroke-width":2}});
}
function select(map,id,T){
  map.setFilter("sel",["==",["get","id"],id||"__none"]);
  var ids=[id||"__none"];
  T.forEach(function(t){ if(id&&t.controlled_from===id) ids.push(t.id); });
  map.setFilter("links-sel",["in",["get","a"],["literal",ids]]);
}

/* ---------- full map page ---------- */
window.DTMap=function(T){
  initProtocol();
  var origin=location.origin;
  var map=new maplibregl.Map({container:"map",style:baseStyle(origin),center:[12,40],zoom:window.innerWidth<820?0.9:1.7,minZoom:0.6,maxZoom:14,attributionControl:{compact:true},dragRotate:false,pitchWithRotate:false});
  map.touchZoomRotate.disableRotation();
  map.addControl(new maplibregl.NavigationControl({showCompass:false}),"top-right");
  var state={q:"",st:{},vendor:"",country:"",links:true,sel:null};
  var by={};T.forEach(function(t,i){t.i=i;by[t.id]=t;});
  var list=document.getElementById("mlist"),detail=document.getElementById("mdetail"),count=document.getElementById("mcount");
  var q=document.getElementById("mq"),sv=document.getElementById("mvendor"),sc=document.getElementById("mcountry"),chips=document.getElementById("mchips");
  Object.keys(LABEL).filter(function(k){return k!=="cancelled";}).forEach(function(k){
    var b=el("button",{class:"chip","aria-pressed":"false","data-s":k,type:"button"},'<i style="display:inline-block;width:8px;height:8px;border-radius:50%;background:'+COL[k]+';margin-right:7px"></i>'+LABEL[k]);
    b.addEventListener("click",function(){state.st[k]=!state.st[k];b.setAttribute("aria-pressed",state.st[k]?"true":"false");render();});
    chips.appendChild(b);
  });
  var vs={},cs={};T.forEach(function(t){t.vendors.forEach(function(v){vs[v]=1;});cs[t.country]=1;});
  Object.keys(vs).sort().forEach(function(v){sv.appendChild(el("option",{value:v},esc(v)));});
  Object.keys(cs).sort().forEach(function(c){sc.appendChild(el("option",{value:c},esc(c)));});
  var P=new URLSearchParams(location.search);if(P.get("country")){sc.value=P.get("country");state.country=sc.value;}if(P.get("vendor")){sv.value=P.get("vendor");state.vendor=sv.value;}
  function match(t){
    if(state.q){var s=(t.name+" "+t.icao+" "+t.country+" "+t.vendors.join(" ")+" "+t.ansp).toLowerCase();if(s.indexOf(state.q)<0)return false;}
    var any=Object.keys(state.st).some(function(k){return state.st[k];});
    if(any){var ok=state.st[t.status]||(t.status==="cancelled"&&state.st.decommissioned);if(!ok)return false;}
    if(state.vendor&&t.vendors.indexOf(state.vendor)<0)return false;
    if(state.country&&t.country!==state.country)return false;
    return true;}
  function render(){
    var m=T.filter(match);count.textContent=m.length+" of "+T.length;
    var ids=m.map(function(t){return t.id;});
    if(map.getLayer("pts")){var f=["in",["get","id"],["literal",ids]];["pts","halo","lab"].forEach(function(l){map.setFilter(l,f);});}
    list.innerHTML="";
    m.slice(0,400).forEach(function(t){
      var b=el("button",{class:"mitem",type:"button"},'<span class="pill st-'+t.status+'" style="padding:2px 8px"></span><span class="n"><b>'+esc(t.name)+'</b><span>'+esc(t.icao||"")+(t.icao?" · ":"")+esc(t.country)+'</span></span>');
      b.addEventListener("click",function(){open(t.id,true);});list.appendChild(b);});
    if(!m.length)list.innerHTML='<p class="mute small" style="padding:14px">No towers match these filters.</p>';
  }
  function open(id,fly){
    var t=by[id];if(!t)return;state.sel=id;select(map,id,T);
    if(fly)map.flyTo({center:[t.lon,t.lat],zoom:Math.max(map.getZoom(),window.innerWidth<820?5.2:5.6),duration:900,padding:window.innerWidth<820?{bottom:window.innerHeight*.5}:{left:380}});
    var facts=t.facts.slice(0,3).map(function(f){return '<li>'+esc(f.t)+'<a class="src" href="'+esc(f.u)+'" rel="noopener" target="_blank">'+esc(host(f.u))+'</a></li>';}).join("");
    var conn=t.connections.slice(0,8).map(function(c){return '<button class="chip" type="button" data-id="'+esc(c.id)+'">'+esc(c.rel)+": "+esc(c.name)+'</button>';}).join(" ");
    detail.innerHTML='<button class="chip" type="button" id="mback">All towers</button><h2>'+esc(t.name)+'</h2><p><span class="pill st-'+t.status+'">'+LABEL[t.status]+'</span> <span class="tag conf-'+t.conf+'">confidence '+t.conf+'</span></p>'
     +'<dl class="kv small" style="margin:12px 0"><dt>ICAO</dt><dd>'+esc(t.icao||"n/a")+'</dd><dt>Country</dt><dd>'+esc(t.country)+'</dd><dt>Vendor</dt><dd>'+esc(t.vendors.join(", ")||"not named in sources")+'</dd><dt>Provider</dt><dd>'+esc(t.ansp||"n/a")+'</dd></dl>'
     +'<ul class="facts small">'+facts+'</ul>'+(conn?'<p class="xs faint" style="margin:14px 0 6px">Connections</p><div style="display:flex;gap:6px;flex-wrap:wrap">'+conn+'</div>':'')
     +'<p style="margin-top:16px"><a class="btn primary" href="/towers/'+esc(t.id)+'/">Open full page</a></p>';
    detail.hidden=false;document.getElementById("mfilters").hidden=true;list.hidden=true;
    document.getElementById("mback").addEventListener("click",close);
    detail.querySelectorAll("[data-id]").forEach(function(b){b.addEventListener("click",function(){open(b.getAttribute("data-id"),true);});});
    history.replaceState(null,"","#"+id);
  }
  function close(){state.sel=null;select(map,null,T);detail.hidden=true;document.getElementById("mfilters").hidden=false;list.hidden=false;history.replaceState(null,"",location.pathname);}
  q.addEventListener("input",function(){state.q=q.value.trim().toLowerCase();render();});
  sv.addEventListener("change",function(){state.vendor=sv.value;render();fit();});
  sc.addEventListener("change",function(){state.country=sc.value;render();fit();});
  var lk=document.getElementById("mlinks");lk.addEventListener("click",function(){state.links=!state.links;lk.setAttribute("aria-pressed",state.links?"true":"false");map.setPaintProperty("links","line-opacity",state.links?0.28:0);});
  document.getElementById("mfit").addEventListener("click",function(){fit();});
  function fit(){var S=T.filter(match);if(!S.length)S=T;var b=new maplibregl.LngLatBounds();S.forEach(function(t){b.extend([t.lon,t.lat]);});map.fitBounds(b,{padding:window.innerWidth<820?{top:40,bottom:window.innerHeight*.5,left:20,right:20}:{top:60,bottom:60,left:400,right:60},duration:800,maxZoom:S.length===T.length?4:7});}
  map.on("load",function(){
    addLayers(map,T,{allLinks:true});render();
    ["pts","halo"].forEach(function(l){map.on("mouseenter",l,function(){map.getCanvas().style.cursor="pointer";});map.on("mouseleave",l,function(){map.getCanvas().style.cursor="";});});
    map.on("click","pts",function(e){open(e.features[0].properties.id,false);});
    map.on("click",function(e){var f=map.queryRenderedFeatures(e.point,{layers:["pts"]});if(!f.length&&state.sel)close();});
    fit();
    var h=location.hash.replace("#","");if(h&&by[h])open(h,true);
  });
  window.__dtmap=map;
};

/* ---------- small map on a tower page ---------- */
window.DTMini=function(id,T){
  initProtocol();var by={};T.forEach(function(t,i){t.i=i;by[t.id]=t;});var me=by[id];if(!me)return;
  var group=[me];if(me.controlled_from&&by[me.controlled_from])group.push(by[me.controlled_from]);
  T.forEach(function(t){if(t.controlled_from===id||(me.controlled_from&&t.controlled_from===me.controlled_from))group.push(t);});
  var map=new maplibregl.Map({container:"minimap",style:baseStyle(location.origin),center:[me.lon,me.lat],zoom:5,minZoom:1,maxZoom:12,attributionControl:{compact:true},cooperativeGestures:true,dragRotate:false});
  map.addControl(new maplibregl.NavigationControl({showCompass:false}),"top-right");
  map.on("load",function(){
    var uniq={};group=group.filter(function(t){if(uniq[t.id])return false;uniq[t.id]=1;return true;});
    addLayers(map,group,{allLinks:true});
    map.setFilter("sel",["==",["get","id"],id]);
    if(group.length>1){var b=new maplibregl.LngLatBounds();group.forEach(function(t){b.extend([t.lon,t.lat]);});map.fitBounds(b,{padding:50,maxZoom:7,duration:0});}
    else map.jumpTo({center:[me.lon,me.lat],zoom:6});
    map.on("click","pts",function(e){location.href="/towers/"+e.features[0].properties.id+"/";});
    map.on("mouseenter","pts",function(){map.getCanvas().style.cursor="pointer";});map.on("mouseleave","pts",function(){map.getCanvas().style.cursor="";});
  });
};
})();
