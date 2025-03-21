    setTimeout(() => {
        let alertas = document.querySelectorAll('.alert');
        alertas.forEach(alert => {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
}, 3000);
