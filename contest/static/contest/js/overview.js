var pass = document.getElementsByName("pass");
var not_pass = document.getElementsByName("not_pass");
var pass_ratio = document.getElementsByName("pass_ratio");
var i;
var j;
for (i = 0; i < pass.length; i++) {
    var res = pass_ratio[i].innerHTML.split("/");
    var pass_ppl = parseInt(res[0]);
    var all_ppl = parseInt(res[1]);
    pass[i].style.width = pass_ppl / all_ppl * 100 + '%';
    not_pass[i].style.width = (1 - pass_ppl / all_ppl) * 100 + '%';
}