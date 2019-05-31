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
    let listGroup = $('#list-group' + postagem_id);
    let listGroupConteudo = listGroup.html();
    let inputPerfilId   = $('input#perfil_id'+postagem_id);
    let inputPostagemId = $('input#postagem_id'+postagem_id);
    let inputConteudo   = $('input#conteudo'+postagem_id);
    $.getJSON($SCRIPT_ROOT + '/novo_comentario', {
        perfil_id   : inputPerfilId.val(),
        postagem_id : inputPostagemId.val(),
        conteudo    : inputConteudo.val()
    }, function(data) {
        inputConteudo.val('');
        let linha = '<button type="button" class="list-group-item list-group-item-action">';
        linha += '<a href="#">@'+data.perfil+'</a> - ' + data.conteudo;
        linha += '</button>';
        listGroup.html(linha + listGroupConteudo);
    });
});

$( ".btnExcluirPostagem" ).click(function() {
    let lengthId    = this.id.length;
    let postagem_id = this.id[lengthId - 1];
    let blocoPostagem = $('#bloco-postagem'+postagem_id);
    bootbox.confirm("Tem certeza que deseja excluir essa postagem?", function(result) { 
        if (result)  {
            $.getJSON($SCRIPT_ROOT + '/excluir_postagem', {
                postagem_id : postagem_id        
            }, function(data) {
                alert(data);
                blocoPostagem.remove();
            }); 
        }
    });   
});