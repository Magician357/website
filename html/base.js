var elems = document.getElementsByClassName("split");
var n;
for (n=0; n < elems.length; n++){
    var cursplit = elems[n].innerHTML.split(" ");
    var currenthtml = "";
    var a;
    var current;
    var splt;
    for (a=0; a<cursplit.length; a++){
        if (cursplit[a][0] === "_") {
            current=cursplit[a].slice(1);
            splt=current.split(":");
            currenthtml+="<a class=\"intext\" href=\"//"+splt[1]+"\" target=\"_blank\" >"+splt[0]+"&nbsp;</a>";
        } else {
            currenthtml+="<p class=\"splitted\">"+cursplit[a]+"&nbsp;</p>";
        }
    }
    elems[n].innerHTML=currenthtml;
}

/* window.addEventListener('beforeunload', function(){
    document.body.classList.add('is-exiting')
}, false) */

async function enter() {
  var elem=document.getElementById("content");
  elem.classList.add("is-entering");
  elem.style.display = "block";
  await new Promise((resolve, reject) => {
    elem.addEventListener("animationend", resolve);
    elem.addEventListener("animationerror", reject);
    setTimeout(reject, 5000);
  }).catch((err) => {
    console.error(err);
  });
  elem.classList.remove("is-entering");
}

enter();