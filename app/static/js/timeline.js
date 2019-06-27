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
    let input_postagem_id   = $('input#postagem_id'+postagem_id);
    let input_conteudo      = $('input#conteudo'+postagem_id);
    $.getJSON($SCRIPT_ROOT + '/novo_comentario', {
        postagem_id : input_postagem_id.val(),
        conteudo    : input_conteudo.val()
    }, function(data) {
        let status = data.status;
        if (data.status == 1) {
            input_conteudo.val('');
            let linha = "";
            linha += '<li id="bloco-comentario-'+ data.comentario +'" class="list-group-item">';
            linha += '<a href="' + $SCRIPT_ROOT + '/perfil/' + data.perfil.id + '">@' + data.perfil.nome_fantasia;
            linha += '</a> - ' + data.conteudo;
            linha += '<button comentario_id="'+ data.comentario +'" type="button" class="btnExcluirComentario btn btn-danger btn-sm"><i class="fas fa-fw fa-trash-alt"></i></button>';
            linha += '</li>';            
            list_group.html(linha + list_group_conteudo);            
        } else {
            bootbox.alert(
                "Ocorreram falhas ao inserir seu comentário, tente novamente."
            );
        }
    });
});

$(document).on( "click", ".btnExcluirComentario", function(event) {
    event.preventDefault();
    let comentario_id = $(this).attr('comentario_id');
    bootbox.confirm("Tem certeza que deseja excluir esse comentário?", function(result) { 
        if (result) {
            $.ajax({
                url: $SCRIPT_ROOT + "/excluir_comentario",
                method: "GET",
                dataType: "json",
                data: { comentario_id: comentario_id },
                success: function(data) {
                    if (data.retorno == 1) {
                        $('#bloco-comentario-'+comentario_id).remove();
                    } else {
                        bootbox.alert(
                            "Ocorreram falhas ao excluir sua postagem, tente novamente."
                        );                        
                    }
                } 
            });
        }
    });
});

$(".btnExcluirPostagem").click(function() {
    let postagem_id    = $(this).attr('postagem_id');
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

$(".btnAvaliarPostagem").click(function() {
    let postagem_id = $(this).attr('postagem_id');

    let mensagem = '<div class="slidecontainer">';
    mensagem    += '<input type="range" min="0" max="100" value="50" class="slider" id="myRange">';
    mensagem    += '</div>';
    mensagem    += '<div>';
    mensagem    += '<button id="btnNota" type="button" class="btn btn-secondary">';
    mensagem    += 'Nota: <span id="span-nota" class="badge badge-light">50</span>';
    mensagem    += '</button>';
    mensagem    += '</div>';

    var dialog = bootbox.dialog({
        title: 'Arraste para avaliar essa postagem (0 - 100)',
        message: mensagem,
        size: 'large',
        buttons: {
            cancel: {
                label: "Cancelar",
                className: 'btn-danger',
                callback: function(){
                    console.log('Avaliação cancelada');
                }
            },
            ok: {
                label: "Avaliar",
                className: 'btn-info',
                callback: function(){
                    console.log('Custom OK clicked');
                    let nota = $('#myRange').val();
                    console.log(nota);

                    $.ajax({
                        url: $SCRIPT_ROOT + "/nova_avaliacao",
                        method: "GET",
                        dataType: "json",
                        data: {
                            postagem_id: postagem_id,
                            nota: nota
                        },
                        success: function(data) {
                            console.log(data.status);
                            if (data.status == 0) {
                                bootbox.alert(
                                    "Ocorreram falhas ao inserir sua avaliação, tente novamente."
                                );
                            }                            
                        }
                    })
                }
            }
        }
    });
});

$(document).on("change","#myRange",function() {
    let nota = $('#myRange').val();
    console.log(nota);
    $('#span-nota').html(nota);
});