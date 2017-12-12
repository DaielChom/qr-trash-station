var img = 0;

$(".button-collapse").sideNav();

$('#crear_contenedor').on('click', (ev)=>{
  ev.preventDefault();

  if($("#id_content").hasClass('invalid')){
    alert("No se aceptan caracteres especiales")
  }

  else{

    $.ajax({
        method: "POST",
        url:"/stations",
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

  }



})

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
  console.log("Click Enviar");
  ev.preventDefault();

  if($('#select_state').val() != null && $("#nombre").val() != null && $("#correo")!= null){

    id_estacion = $("#id_form").val()
    ubicacion = $("#ubicacion").val()
    nombre = $("#nombre").val()
    correo = $("#correo").val()
    estado = $('#select_state').val()
    data = {'id':id_estacion, 'ubicacion': ubicacion, 'nombre': nombre, 'correo': correo,'estado': estado, 'img':img}

    $.ajax({
      method:"POST",
      data: data,
      dataType: 'json',
      url: "/rpt",
      success: function(response){alert('Reporte Enviado'); window.location='/'},
      error: function(response){alert('Error al Enviar Reporte. Error: ' + response['responseText'])}
    });


  }

  else{

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

 $('#textarea1').val('New Text');
 $('#textarea1').trigger('autoresize');

 $(document).ready(function() {
   Materialize.updateTextFields();
 });

function sesion() {
  user = $('#user').val()
  pass = $('#pass').val()

  data = {'user':user,'pass':pass}
  $.ajax({
    method:"POST",
    dataType: 'json',
    data: data,
    url: "login",
    success: function(response){
      if(response.acceso == "true"){
        window.location='/gestion'
      }
      else {
      alert("Campos Incorrectos");
      }
     },
    error: function(response){console.log(response);}
  });
}
