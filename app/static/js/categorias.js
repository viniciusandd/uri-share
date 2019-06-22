function iniciar() {
    var dialog = bootbox.dialog({
        title: 'Cadastrando uma nova categoria',
        message: '<p><i class="fa fa-spin fa-spinner"></i> Carregando...</p>'
    });
                
    dialog.init(function(){
        setTimeout(function(){
            dialog.find('.bootbox-body').html('Categoria cadastrada com sucesso!');
        }, 3000);
    });   
}

$('.btn-aceitar-sugestao').click(function() {
    iniciar();
});

$('.btn-rejeitar-sugestao').click(function() {
    iniciar();
});