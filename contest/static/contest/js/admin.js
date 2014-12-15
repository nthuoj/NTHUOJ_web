$('#infoTab a').click(function(e) {
  e.preventDefault()
  $('#infoTab a[href="#problem"]').tab('show')
  $('#infoTab a[href="#contestant"]').tab('show')
  $('#infoTab a[href="#time"]').tab('show')
  $('#infoTab a[href="#coowner"]').tab('show')
  $('#infoTab a[href="#others"]').tab('show')
})