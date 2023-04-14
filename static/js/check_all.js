$(document).on('change', 'input[type=checkbox]', function () {
  var $this = $(this), $chks = $(document.querySelectorAll("[data-group='"+ $this.data('group') + "']")), $all = $chks.filter(".chk-all");

  if ($this.hasClass('chk-all')) {
    $chks.prop('checked', $this.prop('checked'));
  } else switch ($chks.filter(":checked").length) {
    case +$all.prop('checked'):
      $all.prop('checked', false).prop('indeterminate', false);
      break;
    case $chks.length - !!$this.prop('checked'):
      $all.prop('checked', true).prop('indeterminate', false);
      break;
    default:
      $all.prop('indeterminate', true);
  }
});