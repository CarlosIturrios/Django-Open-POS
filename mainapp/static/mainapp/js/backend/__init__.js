// Objeto para manejar el BACKEND
miapp.backend = {
    version: 0.00001
};

miapp.backend.getCookie = function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// Definir direccion del backend
miapp.backend.url = window.location.origin + "/";

// Funcion hacer peticiones al BackEnd mediante AJAX
miapp.backend.ajax = function (obj) {
    // Si la ruta que mandaron tiene el primer / retirarlo
    if (obj.url.startsWith("/")) {
        obj.url = obj.url.substring(1);
    }
    // Agregar el hostname a la ruta solicitada
    obj.url = miapp.backend.url + obj.url;

    // Agregar Header
    obj.headers = {"X-CSRFToken": miapp.backend.getCookie('csrftoken')};

    // Realizar peticion AJAX mediante Jquery
    return $.ajax(obj);
};
