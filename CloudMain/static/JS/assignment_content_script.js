let cDate = document.getElementById("cDate");
let dDate = document.getElementById("dDate");

cDateString = cDate.innerHTML;
console.log(cDateString)
yyyy = cDateString.slice(0, 4);
mm = cDateString.slice(5, 7);
dd = cDateString.slice(8-10);
cDate.innerHTML = dd + '-' + mm + '-' + yyyy;

dDateString = dDate.innerHTML;
yyyy = dDateString.slice(0, 4);
mm = dDateString.slice(5, 7);
dd = dDateString.slice(8-10);
dDate.innerHTML = dd + '-' + mm + '-' + yyyy;