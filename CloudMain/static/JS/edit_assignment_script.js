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

// Set max integer value for the assignment weight
let weight = document.getElementById("weight");

weight.addEventListener("keydown", function() {
    if (parseInt(weight.value) > 100)
    {
        alert("The value of a paper cannot be above 100.");
    }
});
