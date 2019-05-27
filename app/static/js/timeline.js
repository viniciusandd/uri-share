$(".btnComentarPostagem").click(function() {
    let lengthId    = this.id.length;
    let postagem_id = this.id[lengthId - 1];
    let formularioComentario = $("#comments" + postagem_id);
    
    if ((formularioComentario).is(':visible')) {
        formularioComentario.hide(500);
    } else {
        formularioComentario.show(500);        
    }    
});

$('.btnEnviarComentario').click(function() {
    let lengthId    = this.id.length;
    let postagem_id = this.id[lengthId - 1];    
    $.getJSON($SCRIPT_ROOT + '/novo_comentario', {
        perfil_id  : $('input[name="perfil_id"]').val(),
        postagem_id: $('input[name="postagem_id"]').val(),
        conteudo   : $('input[name="conteudo'+postagem_id+'"]').val()
    }, function(data) {
        alert(data);
    });
});

$( ".btnExcluirPostagem" ).click(function() {
    alert( "Excluir" );
});