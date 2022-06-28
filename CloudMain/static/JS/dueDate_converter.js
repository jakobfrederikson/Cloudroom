let dDates = document.getElementsByClassName("dDate");

for (let i = 0; i < dDates.length; i++) {
    test = dDates[i].innerHTML;
    yyyy = test.slice(0, 4);
    mm = test.slice(5, 7);
    dd = test.slice(8-10);
    dDates[i].innerHTML = dd + '-' + mm + '-' + yyyy;
}