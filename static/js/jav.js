document.addEventListener("DOMContentLoaded", function () {

    const quantityInput = document.getElementById("quantity");
    const totalHarga = document.getElementById("totalHarga");
    const totalInput = document.getElementById("totalInput");

    const hargaPerMug = 65000;

    function hitungTotal() {
        let qty = parseInt(quantityInput.value) || 0;
        let total = qty * hargaPerMug;


        totalHarga.textContent = total.toLocaleString("id-ID");


        totalInput.value = total;
    }


    hitungTotal();


    quantityInput.addEventListener("input", hitungTotal);

});