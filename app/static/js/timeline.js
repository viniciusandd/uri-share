$(".btnComentarPostagem").click(function() {
    let lengthId    = this.id.length;
    let postagem_id = this.id[lengthId - 1];
    console.log(postagem_id);

    $("#formComments" + postagem_id).show(500);
});

$( ".btnExcluirPostagem" ).click(function() {
    alert( "Excluir" );
});