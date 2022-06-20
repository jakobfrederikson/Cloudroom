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
        autoRefresh: true,
        lineNumbers: true,
        indentUnit: 4,
        matchBrackets: true,
        theme: "lucario",
        readOnly: true
    });

    setTimeout(function() {
        test.refresh();
    })
});
