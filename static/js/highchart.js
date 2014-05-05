$('#trend1').click(function () {
    var cur_url = location.href;
    if (cur_url.substring(cur_url.length-1)=='#'){
        cur_url = cur_url.substring(0, cur_url.length-1);
    }
    var items = cur_url.split('/');
    if (isNaN(items[items.length-1])) { // last trend
        var res = items.slice(0, items.length-1);
    }
    else{
        var res = items;
    }

    var url = res.join("/");
    window.location.replace(url+"/trend1");
});
$('#trend2').click(function () {
    var cur_url = location.href;
    if (cur_url.substring(cur_url.length-1)=='#'){
        cur_url = cur_url.substring(0, cur_url.length-1);
    }
    var items = cur_url.split('/');
    if (isNaN(items[items.length-1])) { // last trend
        var res = items.slice(0, items.length-1);
    }
    else{
        var res = items;
    }

    var url = res.join("/");
    window.location.replace(url+"/trend2");
});
$('#trend3').click(function () {
    var cur_url = location.href;
    if (cur_url.substring(cur_url.length-1)=='#'){
        cur_url = cur_url.substring(0, cur_url.length-1);
    }
    var items = cur_url.split('/');
    if (isNaN(items[items.length-1])) { // last trend
        var res = items.slice(0, items.length-1);
    }
    else{
        var res = items;
    }

    var url = res.join("/");
    window.location.replace(url+"/trend3");
});
$('#main_info').click(function () {
    var cur_url = location.href;
    if (cur_url.substring(cur_url.length-1)=='#'){
        cur_url = cur_url.substring(0, cur_url.length-1);
    }
    var items = cur_url.split('/');
    if (isNaN(items[items.length-1])) { // last trend
        var res = items.slice(0, items.length-1);
    }
    else{
        var res = items;
    }

    var url = res.join("/");
    window.location.replace(url);
});



