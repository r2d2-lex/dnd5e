    $(document).ready(function(){
        $('#id_name').on('blur', searchspell);
        function searchspell() {
            var fspells = $('#id_name').val();
            $.ajax({
                method : "GET",
                url: '/main/accounts/profile/find-spells/',
                data: {
                    'fspells': fspells
                },
                dataType: 'json',
                success: function (data) {
                console.log(data);
                    if (data.is_taken) {
                        $('#id_findstat').text(data.is_taken);
                        $('#btn').attr('disabled', 'disabled');
                    }
                    else if (data.ok) {
                        $('#id_findstat').text('');
                        $('#btn').removeAttr('disabled');
                    }
                },
                error: function(data){
                    console.log(data);
            }
        })
    }
})