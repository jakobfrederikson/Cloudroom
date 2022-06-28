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
    textArea = editor.querySelector('[id*="editor"]'); // IF '#editor' exists in the elements ID list
    console.log(textArea.nodeName + " LOADED SUCCESSFULLY.")
    test = CodeMirror.fromTextArea(textArea, {
        mode: {
            name: "python",
            version: 5,
            singleLineStringErrors: false
        },
        autoRefresh: true,
        lineNumbers: true,
        indentUnit: 4,
        matchBrackets: true,
        theme: "lucario"
    });

    setTimeout(function() {
        test.refresh();
    })

    // Let user press tab in textArea
    // https://stackoverflow.com/questions/6637341/use-tab-to-indent-in-textarea
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

    // We can potentially run python code with these links here.
    // https://www.geeksforgeeks.org/build-python-code-editor-using-codemirror-and-pyodide/
    // https://pyodide.org/en/stable/
});
