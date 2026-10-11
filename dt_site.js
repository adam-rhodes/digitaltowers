(function(){
"use strict";
/* directory filter */
var tb=document.getElementById("dirrows");
if(tb){
  var q=document.getElementById("dq"),st=document.getElementById("dstatus"),co=document.getElementById("dcountry"),vn=document.getElementById("dvendor"),n=document.getElementById("dcount");
  var rows=[].slice.call(tb.querySelectorAll("[data-s]"));
  function f(){var s=(q.value||"").trim().toLowerCase(),a=st.value,c=co.value,v=vn.value,k=0;
    rows.forEach(function(r){var ok=(!s||r.getAttribute("data-t").indexOf(s)>=0)&&(!a||r.getAttribute("data-s")===a)&&(!c||r.getAttribute("data-c")===c)&&(!v||r.getAttribute("data-v").indexOf("|"+v+"|")>=0);r.hidden=!ok;if(ok)k++;});
    n.textContent=k+" of "+rows.length;}
  [q,st,co,vn].forEach(function(e){e.addEventListener("input",f);e.addEventListener("change",f);});
  var p=new URLSearchParams(location.search);if(p.get("q")){q.value=p.get("q");}
  if(p.get("status"))st.value=p.get("status"); if(p.get("country"))co.value=p.get("country");
  f();
}
/* home search -> directory */
var hs=document.getElementById("hsearch");
if(hs){hs.addEventListener("submit",function(e){e.preventDefault();var v=document.getElementById("hq").value.trim();location.href="/towers/"+(v?"?q="+encodeURIComponent(v):"");});}
/* news filter */
var nb=document.getElementById("newsfilter");
if(nb){
  var items=[].slice.call(document.querySelectorAll(".nitem"));var cur="";
  nb.addEventListener("click",function(e){var b=e.target.closest("[data-tag]");if(!b)return;var t=b.getAttribute("data-tag");cur=(cur===t)?"":t;
    [].forEach.call(nb.querySelectorAll("[data-tag]"),function(x){x.setAttribute("aria-pressed",x.getAttribute("data-tag")===cur?"true":"false");});
    items.forEach(function(i){i.hidden=cur&&(" "+i.getAttribute("data-tags")+" ").indexOf(" "+cur+" ")<0;});});
}
})();
