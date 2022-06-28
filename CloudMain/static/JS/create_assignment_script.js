// Set the minimum date to be selected for the assignment
let dueDate = document.getElementById("dDate");

let today = new Date();
let dd = String(today.getDate()).padStart(2, '0');
let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
let yyyy = today.getFullYear();
today = yyyy + '-' + mm + '-' + dd;
let max_yyyy = parseInt(yyyy) + 1;
max = max_yyyy + '-12-31';
dueDate.min = today;
dueDate.max = max;