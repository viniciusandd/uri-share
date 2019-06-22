$('.btn-excluir-sugestao').click(function() {
    let sugestao_categoria_id = $(this).attr('sugestao_categoria_id');
    console.log(sugestao_categoria_id);

    bootbox.confirm("Tem certeza que deseja excluir essa sugestão?", function(result) {
        if (result) {
            $.ajax({
                url: $SCRIPT_ROOT + "/excluir_sugestao_categoria",
                method: "GET",
                dataType: "json",
                data: { sugestao_categoria_id: sugestao_categoria_id },
                success: function(data) {
                    console.log(data);
                    if (data.retorno == 1) {
                        $('#bloco-sugestao-'+sugestao_categoria_id).remove();                        
                    }
                }
            });
        }
    }); 
});