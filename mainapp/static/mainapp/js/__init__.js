miapp = {};

$(function () {
    miapp.dvmain = $("#dvmain");

    Path.map("#/productos/listar").to(miapp.productos.listar);
    Path.map("#/dashboard/").to(miapp.dashboard.detalle);

    Path.rescue(function () {
        window.location = "#/dashboard/";
    });

    Path.root("#/dashboard/");

    Path.listen();
});
