var img = 0;

$(".button-collapse").sideNav();

$('#crear_contenedor').on('click', (ev)=>{

  ev.preventDefault();

  $.ajax({
      method: "POST",
      url:"/contenedores/stations",
      data: $('form').serialize(),
      dataType: 'json',
      success: function(response){
        var link = document.createElement('a');
        link.href = response['qr'];  // use realtive url
        link.download = response['qr'].substring(12);
        document.body.appendChild(link);
        link.click();
       },
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
  ev.preventDefault();
  if($("#id_form").val().length!=0 && $("#ubicacion").val().length!=0 && $("#fecha_report").val().length!=0 && $("#nombre").val().length!=0 && $('#select_state').val().length!=0 && img!=0){
    id_estacion = $("#id_form").val()
    ubicacion = $("#ubicacion").val()
    fecha_report = $("#fecha_report").val()
    nombre = $("#nombre").val()
    estado = $('#select_state').val()
    data = {'id':id_estacion, 'ubicacion': ubicacion, 'fecha_report': fecha_report, 'nombre': nombre, 'estado': estado, 'img':img}

    $.ajax({
      method:"POST",
      data: data,
      dataType: 'json',
      url: "/contenedores/rpt",
      success: function(response){alert('Reporte Enviado'); window.location='/contenedores/'},
      error: function(response){alert('Error al Enviar Reporte')}
    });


  }

  else{
    console.log("SS");
    alert('Llene todos los campos');
  }

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
