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

/*
To add attribute to designated element

Usage: add_attribute(element_id, attribute_to_set, value_attribute_should_be); 
*/
function add_attribute(id, attribute, value) {
    var att = document.createAttribute(attribute);
    att.value = value;
	obj = document.getElementById(id);
    if (obj!=null){
		obj.setAttributeNode(att);
    } 
}

/*
add class="form-control" to designated element.
Simple way to bootstraptify element

Usage: add_form_control(id_of_element_to_bootstraptify)
*/

function add_form_control(id) {
    add_attribute(id, 'class', 'form-control');
}

/*
to hide designated element
Usage: hide(id_of_element_to_hide)
*/

function hide(id){
    add_attribute(id,'type','hidden');
}

/*
to modify html
Usage: modify_html(jquery_selector, html_to_replace)
ex1. 
<a id="sometext">Hello NTHUOJ</a>
modify_html("#sometext","HI");
<a id="sometext">HI</a>

ex2. 
<a class="sometext">Hello NTHUOJ</a>
modify_html(".sometext","HI");
<a id="sometext">HI</a>

ex3. 
<a anything="sometext">Hello NTHUOJ</a>
modify_html("[anything=sometext]","HI");
<a id="sometext">HI</a>

*/

function modify_html(where, innerHTML){
    $(where).html(innerHTML);
}
