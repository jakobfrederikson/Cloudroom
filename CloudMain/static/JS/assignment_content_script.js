let cDate = document.getElementById("cDate");
let dDate = document.getElementById("dDate");

cDateString = cDate.innerHTML;
yyyy = cDateString.slice(0, 4);
mm = cDateString.slice(5, 7);
dd = cDateString.slice(8-10);
cDate.innerHTML = dd + '-' + mm + '-' + yyyy;

dDateString = dDate.innerHTML;
yyyy = dDateString.slice(0, 4);
mm = dDateString.slice(5, 7);
dd = dDateString.slice(8-10);
dDate.innerHTML = dd + '-' + mm + '-' + yyyy;

// Set up CodeMirror for each question of type: code
let code_questions = document.querySelectorAll(".code-box");

code_questions.forEach(function(editor) {
    textArea = editor.querySelector("#editor");
    console.log(textArea.nodeName)
    test = CodeMirror.fromTextArea(textArea, {
        mode: {
            name: "python",
            version: 5,
            singleLineStringErrors: false
        },
        lineNumbers: true,
        indentUnit: 4,
        matchBrackets: true,
        theme: "yonce"
    });

    // Let user press tab in textArea
    textArea.addEventListener('keydown', function(e) {
        if (e.key == 'Tab') {
            e.preventDefault();
            var start = this.selectionStart;
            var end = this.selectionEnd;

            // set textare value to: text before caret + tab + text after caret
            this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);

            // put caret at right position again
            this.selectionStart = this.selectionEnd = start + 1;
        }
    });
});