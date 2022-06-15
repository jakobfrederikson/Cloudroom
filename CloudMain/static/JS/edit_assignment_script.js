// Set the minimum date to be selected for the assignment
let dueDate = document.getElementById("dDate");

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
