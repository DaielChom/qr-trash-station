var img = 0;

$(".button-collapse").sideNav();

$('#crear_contenedor').on('click', (ev)=>{

  ev.preventDefault();

  $.ajax({
      method: "POST",
      url:"/stations",
      data: $('form').serialize(),
      dataType: 'json',
      success: function(response){ alert("Contenedor Agregado"); location.reload(); },
      error: function(error){alert("Error al crear")}
  });

})

var hoy = new Date()
$("#fecha_report").val(String(hoy.getDate())+"-"+String(hoy.getMonth()+1)+"-"+String(hoy.getFullYear()));


if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(success, error);
  }

else{
  $("#ubicacion").val("Geolocation is not supported by this browser");
  }

$('input[type=file]').change(function (ev) {
  var reader = new FileReader();
  reader.onload = function(){ img = this.result; };
  reader.readAsDataURL(ev.target.files[0]);
});

$('#report').on('click',(ev)=>{
  ev.preventDefault()
  id_estacion = $("#id_form").val()
  ubicacion = $("#ubicacion").val()
  fecha_report = $("#fecha_report").val()
  nombre = $("#nombre").val()
  estado = ""
  data = {'id':id_estacion, 'ubicacion': ubicacion, 'fecha_report': fecha_report, 'nombre': nombre, 'estado': estado, 'img':img}
  console.log(data);

})


function success(position) {
 var latitude  = position.coords.latitude;
 var longitude = position.coords.longitude;

 $("#ubicacion").val('[' + latitude + ', ' + longitude + ']');

};

function error() {
  $("#ubicacion").val("Unable to retrieve your location"); ;
};

$(document).ready(function() {
   $('select').material_select();
 });
