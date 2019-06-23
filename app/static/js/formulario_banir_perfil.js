$('#btn-banir-perfil').click(function() {
    bootbox.confirm("Tem certeza que deseja banir esse perfil?", function(result) {
        if (result) {
            let perfil_id = $('#selectPerfilId').val();
            let motivo = $('#textAreaMotivo').val();
            $.ajax({
                url: $SCRIPT_ROOT + "/banir_perfil",
                method: "GET",
                dataType: "json",
                data: {
                    perfil_id: perfil_id,
                    motivo: motivo
                 },
                success: function(data) {
                    mensagem = "Falha ao banir o perfil!";
                    if (data.retorno == 1) {
                        mensagem = "O perfil foi banido com sucesso!";
                        // Removendo o perfil banido do select
                        let selectobject=document.getElementById("selectPerfilId");
                        for (var i=0; i<selectobject.length; i++){
                        if (selectobject.options[i].value == perfil_id )
                           selectobject.remove(i);
                        }
                        $('#textAreaMotivo').val("");
                    }
                    bootbox.alert(mensagem);
                }
            });
        }
    });
});