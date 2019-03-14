$(document).ready(function(){
  // $('#upload-file-name').text($('#upload-file').get(0).files[0].name);
  // $('#image-preview').attr('alt', $('#upload-file').get(0).files[0].name);
  // $('footer').hide();
  function checkForm(){
    var obj = $('#upload-file').get(0)
    // console.log(obj.value)
    if (!obj.value) {
         alert('Please choose a image file');
         return false;
    }
    var file = obj.files[0];
    if (file.type !== 'image/jpeg' && file.type !== 'image/png' && file.type !== 'image/gif' && file.type !== 'image/bmp') {
       alert('Please choose correct file type!');
       return false;
    }
    return true;
  }
  $('#upload-file').change(function(e) {

    // if (!this.value) {
    //      info.innerHTML = 'Please choose a image file';
    //      return;
    // }
    // console.log("innerHTML"+this.value);
    // var file = this.files[0];
    // if (file.type !== 'image/jpeg' && file.type !== 'image/png' && file.type !== 'image/gif' && file.type !== 'image/bmp') {
    //    alert('Please choose correct file type!');
    //    return;
    // }
    // console.log('this:'+this.value)
    // console.log('target:'+e.target.value)
    // console.log('currentTarget:'+e.target.files[0])
    if (checkForm()){
      $('#upload-file-name').text(this.files[0].name);
      $('#image-preview').attr('alt', this.files[0].name);
      $('#image-pre-div').removeClass('d-none');
      var reader = new FileReader();
      reader.onload = function(e) {
        $('#image-preview').attr('src', e.target.result);
      };
      reader.readAsDataURL(this.files[0]);
    }
  });

  $('#upload-button').click(function(e){
    if (checkForm()){
      $.ajax({
        url: '/search',
        type: 'POST',
        cache: false,
        data: new FormData(document.querySelector("form")),
        processData: false,
        contentType: false
      }).done(function(data) {

        $('#result-div-line').removeClass('d-none');
        $('#results-row').removeClass('d-none');
        $('#results-row').html(data);
        $('footer').show();
      }).fail(function(res) {
        console.log('fail:'+res)
      });
    }
  });
});
