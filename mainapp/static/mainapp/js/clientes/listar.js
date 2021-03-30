miapp.productos.listar = function (argument) {

    miapp.dvmain.load("/static/mainapp/html/productos/listar.html", function () {
        var dvTitle = $("#dvTitle");
        dvTitle.text('Products');

        var cargar = function () {
            //cargar
        };

        cargar();
    });
};
