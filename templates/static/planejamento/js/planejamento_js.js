function update_valor_planejamento_categoria(id) {
    valor = document.getElementById('valor-categoria-' + id).value
    console.log(valor)

    fetch("/planejamento/update_valor_categoria/" + id, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",

        },
        body: JSON.stringify({ novo_valor: valor })

    }).then(function (result) {
        return result.json()

    }).then(function (data) {
        console.log(data)

    })

}