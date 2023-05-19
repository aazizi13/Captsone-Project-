var d = new Date();
function addHours(date,hour) {
    date.setTime(date.getTime() + hour * 60 * 60 * 1000);
 return date.getHours();
}

today = d.toISOString().split('T')[0]

 for (i = 0; i < 24; ++i){
    $('#hours').append("<option value='" + addHours(d,1) + "'>");
}