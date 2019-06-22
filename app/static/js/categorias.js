function iniciar(sugestao_categoria_id, status) {
    var dialog = bootbox.dialog({
        title: 'Modificando status da sugestão...',
        message: '<p><i class="fa fa-spin fa-spinner"></i> Carregando...</p>'
    });
                
    dialog.init(function() {
        $.ajax({
            url: $SCRIPT_ROOT + "/sugestao_categoria_pendente",
            method: "GET",
            dataType: "json",
            data: {
                sugestao_categoria_id: sugestao_categoria_id,
                status: status
            },
            success: function(data) {
                mensagem = "";
                if (data.retorno == 1) {
                    mensagem = "Operação finalizada com sucesso!";
                    $('#bloco-sugestao-'+sugestao_categoria_id).remove();
                } else {
                    mensagem = "Falha ao realizar a operação!";
                }
                    
                dialog.find('.bootbox-body').html(mensagem);
            }
        });
    });   
}

$('.btn-aceitar-sugestao').click(function() {
    let sugestao_categoria_id = $(this).attr('sugestao_categoria_id');
    iniciar(sugestao_categoria_id, 2);
});

$('.btn-rejeitar-sugestao').click(function() {
    let sugestao_categoria_id = $(this).attr('sugestao_categoria_id');
    iniciar(sugestao_categoria_id, 3);
});