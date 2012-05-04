$(function(){
  $('tr').click(function(){
    var href = $(this).find('a').attr('href');
    console.log(href);
    if(/^http/.test(href)){
      window.open(href);
    }
    return false;
  });
});
