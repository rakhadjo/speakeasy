document.onkeyup = function(e) {
    e.which = e.which || e.charCode;
    isCtrl = e.ctrlKey
    if (e.which == 77) {
        e.preventDefault();
        alert("Ctrl+o was pressed");
        debugger;
    } else if (e.ctrlKey && e.which ==66) {
        alert("Ctrl+B was pressed");
    } else if (e.ctrlKey && e.altKey && e.which == 89) {
        alert("Ctrl+Alt+Y was pressed");
    } else if (e.ctrlKey && e.shiftKey && e.which == 75) {
        alert("Ctrl+Shift+K was pressed");
    }
}