    setTimeout(() => {
        let alertas = document.querySelectorAll('.alert');
        alertas.forEach(alert => {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
}, 3000);

document.addEventListener("DOMContentLoaded", function() {
    let deleteButtons = document.querySelectorAll(".btn-delete");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault(); // Evita que el enlace o formulario se ejecute inmediatamente

            let deleteUrl = button.getAttribute("href") || button.closest("form").action; // Obtiene la URL de eliminación

            Swal.fire({
                title: "¿Estás seguro?",
                text: "Esta acción no se puede deshacer.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = deleteUrl; // Redirige si se confirma
                }
            });
        });
    });
});
