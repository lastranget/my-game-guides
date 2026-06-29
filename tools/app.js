var lastY=window.pageYOffset||0,ticking=false;
function upd(){
  var y=window.pageYOffset||0;
  if(Math.abs(y-lastY)>4){document.body.classList.toggle('hide-chrome', y>lastY && y>60); lastY=y;}
  ticking=false;
}
window.addEventListener('scroll',function(){
  if(!ticking){requestAnimationFrame(upd);ticking=true;}
},{passive:true});
