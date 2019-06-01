$(".btnComentarPostagem").click(function() {
    let postagem_id = $(this).attr('postagem_id');
    let div_comentarios = $("#comments" + postagem_id);    
    if ((div_comentarios).is(':visible')) {
        div_comentarios.hide(500);
    } else {
        div_comentarios.show(500);        
    }    
});

$('.btnEnviarComentario').click(function() {
    let postagem_id         = $(this).attr('postagem_id');
    let list_group          = $('#list-group' + postagem_id);
    let list_group_conteudo = list_group.html();
    let input_perfil_id     = $('input#perfil_id'+postagem_id);
    let input_postagem_id   = $('input#postagem_id'+postagem_id);
    let input_conteudo      = $('input#conteudo'+postagem_id);
    $.getJSON($SCRIPT_ROOT + '/novo_comentario', {
        perfil_id   : input_perfil_id.val(),
        postagem_id : input_postagem_id.val(),
        conteudo    : input_conteudo.val()
    }, function(data) {
        let status = data.status;
        if (data.status == 1) {
            input_conteudo.val('');
            let linha = '<button type="button" class="list-group-item list-group-item-action">';
            linha += '<a href="#">@'+data.perfil+'</a> - ' + data.conteudo;
            linha += '</button>';
            list_group.html(linha + list_group_conteudo);            
        } else {
            bootbox.alert(
                "Ocorreram falhas ao inserir seu comentário, tente novamente."
            );
        }
    });
});

$( ".btnExcluirPostagem" ).click(function() {
    let postagem_id    = $(this).attr('postagem_id');
    console.log(postagem_id);
    let bloco_postagem = $('#bloco_postagem'+postagem_id);
    bootbox.confirm("Tem certeza que deseja excluir essa postagem?", function(result) { 
        if (result)  {
            $.getJSON($SCRIPT_ROOT + '/excluir_postagem', {
                postagem_id : postagem_id
            }, function(data) {
                console.log(data.status);
                if (data.status == 1) {
                    bloco_postagem.remove();
                } else {
                    bootbox.alert(
                        "Ocorreram falhas ao excluir sua postagem, tente novamente."
                    );
                }
            });
        }
    });
});