$(document).ready(function(){
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 1000); // <-- time in milliseconds

    $('input[type=file]').change(function(){
        if($('input[type=file]').val()==''){
            $('button').attr('disabled',true)
        } 
        else{
        $('button').attr('disabled',false);
        }
    })
});