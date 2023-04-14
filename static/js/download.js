$(document).on('change', 'input[type=checkbox]', function () {
  $chks = $(document.getElementsByName('download'));

  let num_of_checked = $chks.filter(":checked").length;
  console.log(num_of_checked);
  if (num_of_checked >= 1){
      $('#downloader').removeClass('disabled');
  } else if (num_of_checked == 0){
      $('#downloader').addClass('disabled');
  }
});