/*
The MIT License (MIT)

Copyright (c) 2014 NTHUOJ team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
var editor;
var adjustEditorSize;
$(function () {
    editor = CodeMirror.fromTextArea(document.getElementById('code_editor'), {
        mode: 'text/x-c++src',
        theme: 'solarized light',
        keyMap: 'sublime',
        placeholder: 'Code goes here...',
        // line settings
        lineNumbers: true,
        lineWrapping: true,
        styleActiveLine: true,
        // indent settings
        indentUnit: 4,
        indentWithTabs: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        showCursorWhenSelecting: true
    });

    var adjustEditorSize = function (editor) {
        // Adjust editor size according to the line count
        lineCount = editor.lineCount()
        lineHeight = $('.CodeMirror-gutter-wrapper').height()
        editorWidth = $('.CodeMirror').width()
        editorHeight = Math.max(400, Math.min(lineCount*lineHeight + 50, 2000))
        editor.setSize(editorWidth, editorHeight)
    }
    var fire;
    var sublimePatch = function (editor, key) {
        // Fix sublime keybinding can't use Backspace
        if(fire && editor.getCursor().ch == 0 && key == 'Backspace') {
            editor.execCommand('delCharBefore');
            fire = false;
        }
        fire = editor.getCursor().ch == 0;
    }

    // Adjust editor size on load
    adjustEditorSize(editor)

    // Adjust editor size on change
    editor.on('change', adjustEditorSize)

    editor.on('keyHandled', sublimePatch)

    $('#fileinput').bootstrapFileInput();

    $('#fileinput').change(function(evt) {
        //Retrieve the first (and only!) File from the FileList object
        var file = evt.target.files[0];

        if (file) {
            if (file.size > 10000) {
                alert('You can\'t upload file over 10000 bytes.');
            } else {
                var reader = new FileReader();
                reader.onload = function(e) {
                    var contents = e.target.result;
                    try {
                        editor.getDoc().setValue(contents);
                    } catch (e) {

                    }
                };
                reader.readAsText(file);
            }
        } else {
            alert('Failed to load file');
        }
    })
})
