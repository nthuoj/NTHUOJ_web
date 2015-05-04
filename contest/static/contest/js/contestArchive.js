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
$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip({
        'placement': 'top'
    });
    $('[data-load-remote]').on('click', function(e) {
        e.preventDefault();
        var $this = $(this);
        var remote = $this.data('load-remote');
        if (remote) {
            $($this.data('remote-target')).load(remote);
        }
    });
    $('[name=infoTab] a').click(function(e) {
        e.preventDefault()
        $('#infoTab a').tab('show')
    });
    var loading = '<h3 style="text-align:center;">Loading...</h3>'
    $('#contestInfo').on('hidden.bs.modal', function(e) {
        $('#contestInfoContent').html(loading);
    });
    $('#register').on('hidden.bs.modal', function(e) {
        $('#registerContent').html(loading);
    });
});

function confirm_delete() {
    return confirm("Are you sure you want to delete?");
}

function confirm_register() {
    var from = $('#public_user_now').html();
    var to = $('#public_user_need').val();
    return confirm("Set Public User from " + from + " to " + to + "?");
}

