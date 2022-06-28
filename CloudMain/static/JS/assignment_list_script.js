// Set the dates to be the NZ date format dd/mm/yyyy
let cDates = document.getElementsByClassName("cDate");

for (let i = 0; i < cDates.length; i++) {
    test = cDates[i].innerHTML;
    yyyy = test.slice(0, 4);
    mm = test.slice(5, 7);
    dd = test.slice(8-10);
    cDates[i].innerHTML = dd + '-' + mm + '-' + yyyy;
}

