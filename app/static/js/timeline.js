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

$( ".btnExcluirPostagem" ).click(function() {
    alert( "Excluir" );
});