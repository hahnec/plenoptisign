/**
 *
 * @source: cgi.js
 *
 * @licstart  The following is the entire license notice for the
 *  JavaScript code in this page.
 *
 * Copyright (C) 2019  Christopher Hahne
 *
 *
 * The JavaScript code in this page is free software: you can
 * redistribute it and/or modify it under the terms of the GNU
 * General Public License (GNU GPL) as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option)
 * any later version.  The code is distributed WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU GPL for more details.
 *
 * As additional permission under GNU GPL version 3 section 7, you
 * may distribute non-source (e.g., minimized or compacted) forms of
 * that code without the copy of the GNU GPL normally required by
 * section 4, provided you include this license notice and a URL
 * through which recipients can access the Corresponding Source.
 *
 * @licend  The above is the entire license notice
 * for the JavaScript code in this page.
 *
 */

function run() {
    xmlhttpPost("plenoptisign/plenoptisign/bin/cgi_script.py")
    return true; // return false to cancel form action
}

function xmlhttpPost(strURL) {
    var xmlHttpReq = false;
    var self = this;
    // Mozilla/Safari
    if (window.XMLHttpRequest) {
        self.xmlHttpReq = new XMLHttpRequest();
    }
    // IE
    else if (window.ActiveXObject) {
        self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
    }
    self.xmlHttpReq.open('POST', strURL, true);
    self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    self.xmlHttpReq.onreadystatechange = function() {
        if (self.xmlHttpReq.readyState == 4) {
            updatepage(self.xmlHttpReq.responseText);
        }
    }
    self.xmlHttpReq.send(getquerystring());
}

function getquerystring() {
    var form = document.forms['f1'];
    var pp = form.pp.value;
    var fs = form.fs.value;
    var pm = form.pm.value;
    var dA = form.dA.value;
    var fU = form.fU.value;
    var df = form.df.value;
    var a = form.a.value;
    var M = form.M.value;
    var i = form.i.value;
    var dx = form.dx.value;
    qustr = 'pp=' + encodeURI(pp) + '&' +
            'fs=' + encodeURI(fs) + '&' +
            'pm=' + encodeURI(pm) + '&' +
            'dA=' + encodeURI(dA) + '&' +
            'fU=' + encodeURI(fU) + '&' +
            'df=' + encodeURI(df) + '&' +
            'a=' + encodeURI(a) + '&' +
            'M=' + encodeURI(M) + '&' +
            'i=' + encodeURI(i) + '&' +
            'dx=' + encodeURI(dx) + '&' +
            'refo=' + encodeURI('1') + '&' +
            'tria=' + encodeURI('1'); // NOTE: no '?' before querystring
    return qustr;
}

function updatepage(str){
    document.getElementById("result").innerHTML = str;
}